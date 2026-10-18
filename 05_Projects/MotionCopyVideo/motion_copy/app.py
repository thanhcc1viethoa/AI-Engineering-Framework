#!/usr/bin/env python3
"""Local web UI for Motion Copy Video.

Serves ui/index.html on http://127.0.0.1:<port> (local machine only) and a
small JSON API around the same prepare / check / assemble functions as the
command line. Uses only the standard library on top of the CLI's own
dependencies.

  python app.py [--projects-dir DIR] [--port 8765] [--no-browser]
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import shutil
import threading
import traceback
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

import assembler
import planner
import qc

UI_FILE = Path(__file__).resolve().parent / "ui" / "index.html"
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
ASSET_KINDS = ("character", "outfit", "accessories", "prop", "background")
SETTING_KEYS = ("name", "subject_in_source", "prop_label", "background_prompt",
                "identity_lock", "end_lock")
PROJECT_NAME = re.compile(r"^[\w\- ]{1,60}$")
CHUNK = 1 << 20

TASK_LABELS = {
    "prepare": "Chia đoạn và tạo job sheet",
    "jobs": "Cập nhật prompt",
    "check": "Kiểm tra các đoạn",
    "approve": "Duyệt đoạn neo",
    "assemble": "Ghép video",
}


class ApiError(Exception):
    def __init__(self, message: str, status: int = HTTPStatus.BAD_REQUEST):
        super().__init__(message)
        self.status = status


class Task:
    """At most one long operation (ffmpeg work) runs at a time."""

    def __init__(self):
        self.lock = threading.Lock()
        self.state = {"running": False, "project": None, "action": None, "message": "", "error": None}

    def start(self, project_name: str, action: str, func) -> None:
        with self.lock:
            if self.state["running"]:
                raise ApiError("Đang chạy một tác vụ khác, vui lòng chờ.", HTTPStatus.CONFLICT)
            self.state = {"running": True, "project": project_name, "action": action,
                          "message": TASK_LABELS[action] + "…", "error": None}
        threading.Thread(target=self._run, args=(func,), daemon=True).start()

    def _run(self, func) -> None:
        try:
            message = func()
            error = None
        except (planner.ConfigError, ValueError, RuntimeError) as exc:
            message, error = "", str(exc)
        except Exception as exc:  # report unexpected failures to the UI, never swallow them
            traceback.print_exc()
            message, error = "", f"Lỗi không mong đợi: {exc}"
        with self.lock:
            self.state.update(running=False, message=message, error=error)

    def snapshot(self) -> dict:
        with self.lock:
            return dict(self.state)


class Workspace:
    def __init__(self, projects_dir: Path):
        self.projects_dir = projects_dir.resolve()
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.task = Task()

    # ---- projects --------------------------------------------------------
    def list_projects(self) -> list[str]:
        return sorted(p.name for p in self.projects_dir.iterdir() if (p / "project.json").is_file())

    def root(self, name: str | None) -> Path:
        if not name or not PROJECT_NAME.match(name):
            raise ApiError("Tên dự án không hợp lệ.")
        root = (self.projects_dir / name).resolve()
        if root.parent != self.projects_dir:
            raise ApiError("Tên dự án không hợp lệ.")
        return root

    def create(self, name: str) -> None:
        root = self.root(name.strip())
        if (root / "project.json").exists():
            raise ApiError("Dự án đã tồn tại.")
        root.mkdir(parents=True, exist_ok=True)
        config = {"name": name.strip(), "sources": [], "subject_in_source": "the cyclist",
                  "prop_label": "bicycle", "background_prompt": "", "identity_lock": "", "end_lock": ""}
        self.save_config(root, config)

    @staticmethod
    def load_config(root: Path) -> dict:
        path = root / "project.json"
        if not path.is_file():
            raise ApiError("Không tìm thấy dự án.", HTTPStatus.NOT_FOUND)
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def save_config(root: Path, config: dict) -> None:
        (root / "project.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- state -----------------------------------------------------------
    def state(self, name: str) -> dict:
        root = self.root(name)
        config = self.load_config(root)
        merged = {**planner.DEFAULTS, **config}
        work = root / "work"

        def url(path: Path) -> str:
            rel = path.relative_to(root).as_posix()
            return f"/files?p={quote(name)}&path={quote(rel)}&v={int(path.stat().st_mtime)}"

        sources = []
        for rel in config.get("sources", []):
            path = root / rel
            if path.is_file():
                sources.append({"name": path.name, "url": url(path)})
        assets = {}
        for kind in ASSET_KINDS:
            folder = planner.asset_dir(root, config, kind)
            files = sorted(p for p in folder.glob("*") if p.suffix.lower() in IMAGE_EXT) if folder.is_dir() else []
            assets[kind] = [{"name": p.name, "url": url(p)} for p in files]

        segments = []
        plan = work / "plan.json"
        jobs_file = work / "flow_jobs.json"
        report_file = work / "qc" / "report.json"
        jobs = {j["id"]: j for j in json.loads(jobs_file.read_text(encoding="utf-8"))} if jobs_file.is_file() else {}
        report = {r["id"]: r for r in json.loads(report_file.read_text(encoding="utf-8"))} if report_file.is_file() else {}
        if plan.is_file():
            for seg in json.loads(plan.read_text(encoding="utf-8"))["segments"]:
                output = next((work / "outputs" / f"{seg['id']}{ext}" for ext in (".mp4", ".mov", ".webm", ".mkv")
                               if (work / "outputs" / f"{seg['id']}{ext}").is_file()), None)
                job = jobs.get(seg["id"], {})
                qc_row = report.get(seg["id"])
                if qc_row and output and qc_row["status"] == "MISSING":
                    qc_row = None  # output added after the last check
                segments.append({
                    "id": seg["id"],
                    "need": round(seg["core"] + seg["overlap"], 2),
                    "upload_url": url(work / seg["file"]),
                    "upload_name": f"{seg['id']}.mp4",
                    "output_url": url(output) if output else None,
                    "prompt": job.get("prompt", ""),
                    "ingredients": [{"name": Path(i).name, "url": url(work / i)}
                                    for i in job.get("ingredients", []) if (work / i).is_file()],
                    "qc": qc_row,
                })

        anchor_id = f"seg_{int(merged.get('anchor_segment', 1)):03d}"
        hero = work / "refs" / "anchor_frame.png"
        sheet = work / "qc" / "contact_sheet.png"
        final = work / "final.mp4"
        outputs_done = bool(segments) and all(s["output_url"] for s in segments)
        anchor_seg = next((s for s in segments if s["id"] == anchor_id), None)
        all_pass = bool(report) and outputs_done and all(r["status"] == "PASS" for r in report.values())
        steps = [
            bool(sources) and bool(assets["character"]),
            bool(segments),
            bool(anchor_seg and anchor_seg["output_url"]),
            hero.is_file(),
            outputs_done,
            all_pass,
            final.is_file(),
        ]
        return {
            "project": name,
            "settings": {k: config.get(k, merged.get(k, "")) for k in SETTING_KEYS},
            "sources": sources,
            "assets": assets,
            "segments": segments,
            "anchor": {"id": anchor_id, "approved": hero.is_file(), "url": url(hero) if hero.is_file() else None},
            "contact_sheet": url(sheet) if sheet.is_file() else None,
            "final": url(final) if final.is_file() else None,
            "steps": steps,
            "task": self.task.snapshot(),
        }

    # ---- mutations -------------------------------------------------------
    def save_settings(self, name: str, values: dict) -> None:
        root = self.root(name)
        config = self.load_config(root)
        for key in SETTING_KEYS:
            if key in values:
                config[key] = str(values[key])
        self.save_config(root, config)

    def upload(self, name: str, kind: str, filename: str, seg: str | None, body, length: int) -> None:
        root = self.root(name)
        config = self.load_config(root)
        ext = Path(filename).suffix.lower()
        if kind in ("source", "output"):
            if ext not in VIDEO_EXT:
                raise ApiError("Chỉ nhận file video (mp4, mov, webm, mkv).")
        elif kind in ASSET_KINDS:
            if ext not in IMAGE_EXT:
                raise ApiError("Chỉ nhận file ảnh (png, jpg, webp, bmp).")
        else:
            raise ApiError("Loại tải lên không hợp lệ.")

        if kind == "output":
            if not seg or not re.fullmatch(r"seg_\d{3}", seg):
                raise ApiError("Thiếu mã đoạn.")
            folder = root / "work" / "outputs"
            for old in folder.glob(f"{seg}.*"):
                old.unlink()
            target = folder / f"{seg}{ext}"
        else:
            folder = root / "source" if kind == "source" else planner.asset_dir(root, config, kind)
            target = folder / safe_filename(filename)
        folder.mkdir(parents=True, exist_ok=True)
        with open(target, "wb") as handle:
            remaining = length
            while remaining > 0:
                chunk = body.read(min(CHUNK, remaining))
                if not chunk:
                    break
                handle.write(chunk)
                remaining -= len(chunk)
        if kind == "source":
            rel = target.relative_to(root).as_posix()
            if rel not in config.setdefault("sources", []):
                config["sources"].append(rel)
                self.save_config(root, config)

    def delete(self, name: str, kind: str, filename: str) -> None:
        root = self.root(name)
        config = self.load_config(root)
        if kind == "source":
            folder = root / "source"
        elif kind in ASSET_KINDS:
            folder = planner.asset_dir(root, config, kind)
        else:
            raise ApiError("Loại không hợp lệ.")
        target = (folder / Path(filename).name).resolve()
        if target.parent != folder.resolve() or not target.is_file():
            raise ApiError("Không tìm thấy file.", HTTPStatus.NOT_FOUND)
        target.unlink()
        if kind == "source":
            rel = target.relative_to(root.resolve()).as_posix()
            config["sources"] = [s for s in config.get("sources", []) if s != rel]
            self.save_config(root, config)

    def run(self, name: str, action: str) -> None:
        root = self.root(name)
        config_path = root / "project.json"
        if action not in TASK_LABELS:
            raise ApiError("Tác vụ không hợp lệ.")

        def job():
            project = planner.Project(config_path)
            if action == "prepare":
                return f"Đã chia thành {len(planner.prepare(project))} đoạn."
            if action == "jobs":
                _, segments = project.load_plan()
                planner.write_job_sheet(project, planner.build_reference_pack(project), segments)
                return "Đã cập nhật prompt."
            if action in ("check", "approve"):
                reports, _ = qc.check(project, approve_anchor=action == "approve")
                counts = {s: sum(r.status == s for r in reports) for s in ("PASS", "CHECK", "MISSING")}
                prefix = "Đã duyệt đoạn neo. " if action == "approve" else ""
                return prefix + f"PASS {counts['PASS']} · CHECK {counts['CHECK']} · Thiếu {counts['MISSING']}"
            return f"Đã ghép: {assembler.assemble(project).name}"

        self.task.start(name, action, job)

    def file_path(self, name: str, rel: str) -> Path:
        root = self.root(name)
        path = (root / rel).resolve()
        if root not in path.parents or not path.is_file():
            raise ApiError("Không tìm thấy file.", HTTPStatus.NOT_FOUND)
        return path


def safe_filename(name: str) -> str:
    base = Path(name).name
    stem = re.sub(r"[^\w\-. ]", "_", Path(base).stem).strip(" .") or "file"
    return stem[:80] + Path(base).suffix.lower()


def make_handler(workspace: Workspace):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):  # keep the console quiet
            pass

        def _query(self) -> dict:
            return {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}

        def _json(self, data, status=HTTPStatus.OK) -> None:
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _body_json(self) -> dict:
            length = int(self.headers.get("Content-Length") or 0)
            return json.loads(self.rfile.read(length) or b"{}") if length else {}

        def _dispatch(self, handler) -> None:
            try:
                handler()
            except ApiError as exc:
                self._json({"error": str(exc)}, exc.status)
            except (ValueError, json.JSONDecodeError) as exc:
                self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def do_GET(self):
            self._dispatch(self._get)

        def do_POST(self):
            self._dispatch(self._post)

        def do_PUT(self):
            self._dispatch(self._put)

        def _get(self):
            route, q = urlparse(self.path).path, self._query()
            if route == "/":
                body = UI_FILE.read_bytes()
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            elif route == "/api/projects":
                self._json({"projects": workspace.list_projects(), "dir": str(workspace.projects_dir)})
            elif route == "/api/state":
                self._json(workspace.state(q.get("p")))
            elif route == "/files":
                self._send_file(workspace.file_path(q.get("p"), q.get("path", "")), "dl" in q)
            else:
                raise ApiError("Not found", HTTPStatus.NOT_FOUND)

        def _post(self):
            route, q = urlparse(self.path).path, self._query()
            if route == "/api/projects":
                workspace.create(self._body_json().get("name", ""))
            elif route == "/api/settings":
                workspace.save_settings(q.get("p"), self._body_json())
            elif route == "/api/delete":
                workspace.delete(q.get("p"), q.get("kind", ""), q.get("name", ""))
            elif route == "/api/run":
                workspace.run(q.get("p"), q.get("action", ""))
            else:
                raise ApiError("Not found", HTTPStatus.NOT_FOUND)
            self._json({"ok": True})

        def _put(self):
            if urlparse(self.path).path != "/api/upload":
                raise ApiError("Not found", HTTPStatus.NOT_FOUND)
            q = self._query()
            workspace.upload(q.get("p"), q.get("kind", ""), q.get("name", ""), q.get("seg"),
                             self.rfile, int(self.headers.get("Content-Length") or 0))
            self._json({"ok": True})

        def _send_file(self, path: Path, download: bool) -> None:
            """Serve a file with HTTP Range support so <video> can seek."""
            size = path.stat().st_size
            start, end = 0, size - 1
            match = re.match(r"bytes=(\d*)-(\d*)", self.headers.get("Range", ""))
            if match and (match.group(1) or match.group(2)):
                if match.group(1):
                    start = int(match.group(1))
                    end = int(match.group(2)) if match.group(2) else size - 1
                else:
                    start = max(size - int(match.group(2)), 0)
                end = min(end, size - 1)
                if start > end:
                    self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.end_headers()
                    return
                self.send_response(HTTPStatus.PARTIAL_CONTENT)
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            else:
                self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", mimetypes.guess_type(path.name)[0] or "application/octet-stream")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(end - start + 1))
            if download:
                self.send_header("Content-Disposition", f"attachment; filename*=UTF-8''{quote(path.name)}")
            self.end_headers()
            with open(path, "rb") as handle:
                handle.seek(start)
                remaining = end - start + 1
                while remaining > 0:
                    chunk = handle.read(min(CHUNK, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--projects-dir", type=Path, default=Path.home() / "Videos" / "MotionCopy")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    if shutil.which("ffmpeg") is None:
        print("Cảnh báo: chưa tìm thấy ffmpeg trong PATH — các bước xử lý video sẽ báo lỗi.")
    workspace = Workspace(args.projects_dir)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(workspace))
    url = f"http://127.0.0.1:{args.port}/"
    print(f"Motion Copy Video UI: {url}\nThư mục dự án: {workspace.projects_dir}\nNhấn Ctrl+C để dừng.")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

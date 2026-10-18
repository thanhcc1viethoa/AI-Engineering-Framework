#!/usr/bin/env python3
"""End-to-end test of the web UI's API (no browser, no Flow account needed).

Starts app.py's server on a free local port with a temporary projects folder,
uploads synthetic media through the same endpoints the page uses, runs every
step and checks the reported state.
"""

from __future__ import annotations

import json
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlencode

import app
import smoke_test

BASE = ""


def call(method: str, path: str, data=None, raw: bytes | None = None) -> dict:
    body = raw if raw is not None else (json.dumps(data).encode() if data is not None else None)
    request = urllib.request.Request(BASE + path, data=body, method=method)
    if data is not None:
        request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())


def wait(project: str) -> dict:
    for _ in range(600):
        state = call("GET", "/api/state?" + urlencode({"p": project}))
        if not state["task"]["running"]:
            if state["task"]["error"]:
                raise AssertionError(state["task"]["error"])
            return state
        time.sleep(0.3)
    raise AssertionError("task timed out")


def put(project: str, kind: str, path: Path, seg: str | None = None) -> None:
    query = {"p": project, "kind": kind, "name": path.name, **({"seg": seg} if seg else {})}
    call("PUT", "/api/upload?" + urlencode(query), raw=path.read_bytes())


def main() -> int:
    global BASE
    with tempfile.TemporaryDirectory() as tmp:
        media = Path(tmp) / "media"
        media.mkdir()
        smoke_test.make_sources(media)
        server = ThreadingHTTPServer(("127.0.0.1", 0), app.make_handler(app.Workspace(Path(tmp) / "projects")))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        BASE = f"http://127.0.0.1:{server.server_address[1]}"

        name = "thử nghiệm 01"
        call("POST", "/api/projects", {"name": name})
        assert call("GET", "/api/projects")["projects"] == [name]
        for clip in ("clip1.mp4", "clip2.mp4"):
            put(name, "source", media / "nguồn" / clip)
        for kind in ("character", "outfit", "prop"):
            for image in sorted((media / "assets" / kind).iterdir()):
                put(name, kind, image)
        call("POST", "/api/settings?" + urlencode({"p": name}), {
            "subject_in_source": "the cyclist", "identity_lock": "IDENTITY LOCK", "end_lock": "END LOCK"})

        # Rejections: path traversal and wrong file type.
        for bad in ("/api/state?p=..", "/files?" + urlencode({"p": name, "path": "../../etc/passwd"})):
            try:
                call("GET", bad)
                raise AssertionError(f"expected rejection for {bad}")
            except urllib.error.HTTPError as exc:
                assert exc.code in (400, 404), exc.code
        try:
            call("PUT", "/api/upload?" + urlencode({"p": name, "kind": "prop", "name": "x.exe"}), raw=b"x")
            raise AssertionError("expected rejection for .exe")
        except urllib.error.HTTPError as exc:
            assert exc.code == 400

        state = call("GET", "/api/state?" + urlencode({"p": name}))
        assert state["steps"][0] and len(state["sources"]) == 2 and len(state["assets"]["outfit"]) == 2

        call("POST", "/api/run?" + urlencode({"p": name, "action": "prepare"}))
        state = wait(name)
        # Default 8 s pieces: clip1 = 6 s shot + 3 s shot, clip2 = 4 s -> 3 segments.
        assert len(state["segments"]) == 3 and state["segments"][0]["prompt"].startswith("IDENTITY LOCK")

        # Fake Flow, then upload through the segment cards' endpoint.
        root = Path(tmp) / "projects" / name
        smoke_test.fake_flow(app.planner.Project(root / "project.json"))
        outputs = root / "work" / "outputs"
        staged = Path(tmp) / "flow_downloads"
        staged.mkdir()
        for clip in sorted(outputs.iterdir()):
            clip.rename(staged / f"Flow download {clip.stem}.mp4")
        put(name, "output", staged / "Flow download seg_001.mp4", "seg_001")
        state = call("GET", "/api/state?" + urlencode({"p": name}))
        assert state["steps"][2] and not state["steps"][3]

        call("POST", "/api/run?" + urlencode({"p": name, "action": "approve"}))
        state = wait(name)
        assert state["anchor"]["approved"] and len(state["segments"][1]["ingredients"]) == 4

        for clip in sorted(staged.iterdir())[1:]:
            put(name, "output", clip, clip.stem.split()[-1])
        call("POST", "/api/run?" + urlencode({"p": name, "action": "check"}))
        state = wait(name)
        assert state["contact_sheet"] and all(s["qc"] for s in state["segments"])

        call("POST", "/api/run?" + urlencode({"p": name, "action": "assemble"}))
        state = wait(name)
        assert state["final"] and state["steps"][6]

        # Range request, as used by the <video> player.
        request = urllib.request.Request(BASE + state["final"], headers={"Range": "bytes=0-99"})
        with urllib.request.urlopen(request) as response:
            assert response.status == 206 and len(response.read()) == 100

        server.shutdown()
        print("App smoke test passed:", state["task"]["message"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

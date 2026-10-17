"""ffmpeg / ffprobe helpers.

All video I/O goes through the ffmpeg command line (not cv2.VideoCapture) so
that Windows paths with Vietnamese characters work reliably.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import cv2
import numpy as np


class VideoOpsError(RuntimeError):
    """Raised when ffmpeg/ffprobe fails or a video cannot be read."""


def require_tools() -> None:
    missing = [tool for tool in ("ffmpeg", "ffprobe") if shutil.which(tool) is None]
    if missing:
        raise VideoOpsError(
            f"Missing required tool(s): {', '.join(missing)}. Install ffmpeg and add it to PATH."
        )


def _run(args: list[str], capture_stdout: bool = False) -> subprocess.CompletedProcess:
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE if capture_stdout else subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        tail = result.stderr.decode("utf-8", "replace").strip().splitlines()[-5:]
        raise VideoOpsError(f"{args[0]} failed: " + " | ".join(tail))
    return result


def probe(path: Path) -> dict:
    """Return duration (s), fps, width, height and whether an audio stream exists."""
    result = _run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_stdout=True,
    )
    data = json.loads(result.stdout)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    if video is None:
        raise VideoOpsError(f"No video stream in {path}")
    num, _, den = video.get("r_frame_rate", "30/1").partition("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 30.0
    duration = float(data.get("format", {}).get("duration") or video.get("duration") or 0)
    if duration <= 0:
        raise VideoOpsError(f"Cannot determine duration of {path}")
    return {
        "duration": duration,
        "fps": fps,
        "width": int(video["width"]),
        "height": int(video["height"]),
        "has_audio": any(s.get("codec_type") == "audio" for s in data.get("streams", [])),
    }


def detect_scene_cuts(path: Path, threshold: float) -> list[float]:
    """Timestamps (s) of hard cuts, using ffmpeg's scene-change score."""
    result = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
            "-vf", f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise VideoOpsError(f"Scene detection failed for {path}")
    log = result.stderr.decode("utf-8", "replace")
    return [float(t) for t in re.findall(r"pts_time:([0-9.]+)", log)]


def cut_segment(src: Path, start: float, duration: float, dst: Path) -> None:
    """Frame-accurate re-encoded cut, video only (audio comes from the source at assembly)."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    _run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", str(src),
        "-t", f"{duration:.3f}", "-an", "-c:v", "libx264", "-crf", "16",
        "-preset", "fast", "-pix_fmt", "yuv420p", str(dst),
    ])


def grab_frame(path: Path, t: float) -> np.ndarray:
    """Decode one frame at time t (s) as a BGR array."""
    result = _run(
        [
            "ffmpeg", "-v", "error", "-ss", f"{max(t, 0):.3f}", "-i", str(path),
            "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-",
        ],
        capture_stdout=True,
    )
    frame = cv2.imdecode(np.frombuffer(result.stdout, np.uint8), cv2.IMREAD_COLOR)
    if frame is None:
        raise VideoOpsError(f"Could not decode frame at {t:.2f}s from {path}")
    return frame


def sample_frames(path: Path, duration: float, count: int) -> list[np.ndarray]:
    """Evenly spaced frames, avoiding the very first/last frame."""
    return [grab_frame(path, duration * (i + 1) / (count + 1)) for i in range(count)]


def last_frame_time(duration: float, fps: float) -> float:
    return max(duration - 1.5 / max(fps, 1.0), 0.0)


def normalize_clip(
    src: Path,
    dst: Path,
    *,
    need: float,
    width: int,
    height: int,
    fps: float,
    fit: str,
    stretch: float,
    color_lut: str | None,
) -> None:
    """Retime, resize and colour-correct one generated clip onto the common timeline."""
    filters = []
    if stretch != 1.0:
        filters.append(f"setpts=PTS*{stretch:.6f}")
    filters.append(f"fps={fps:g}")
    if fit == "pad":
        filters.append(f"scale={width}:{height}:force_original_aspect_ratio=decrease")
        filters.append(f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black")
    else:
        filters.append(f"scale={width}:{height}:force_original_aspect_ratio=increase")
        filters.append(f"crop={width}:{height}")
    filters.append("setsar=1")
    if color_lut:
        filters.append(color_lut)
    filters.append("format=yuv420p")
    dst.parent.mkdir(parents=True, exist_ok=True)
    _run([
        "ffmpeg", "-y", "-v", "error", "-i", str(src), "-an", "-vf", ",".join(filters),
        "-t", f"{need:.3f}", "-c:v", "libx264", "-crf", "16", "-preset", "fast", str(dst),
    ])


def run_ffmpeg(args: list[str]) -> None:
    _run(["ffmpeg", "-y", "-v", "error", *args])

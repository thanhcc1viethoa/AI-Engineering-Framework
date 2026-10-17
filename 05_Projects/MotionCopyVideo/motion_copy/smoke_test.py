#!/usr/bin/env python3
"""End-to-end smoke test with synthetic videos (no Flow account needed).

Builds two source videos (one with a hard cut and audio, one silent),
runs prepare, fakes the Flow step by re-encoding each segment at another
size/length/colour, then runs check and assemble and verifies the result.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

import image_ops
import motion_copy
import planner
import video_ops


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def make_sources(root: Path) -> None:
    src = root / "nguồn"  # non-ASCII on purpose
    src.mkdir()
    # 6 s moving pattern + 3 s different scene, with a tone -> one hard cut at 6 s.
    ffmpeg("-f", "lavfi", "-i", "testsrc2=size=360x640:rate=30:duration=6",
           "-f", "lavfi", "-i", "mandelbrot=size=360x640:rate=30",
           "-f", "lavfi", "-i", "sine=frequency=440:duration=9",
           "-filter_complex", "[1:v]trim=0:3,setpts=PTS-STARTPTS[b];[0:v][b]concat=n=2:v=1:a=0[v]",
           "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
           str(src / "clip1.mp4"))
    # 4 s silent clip.
    ffmpeg("-f", "lavfi", "-i", "testsrc=size=360x640:rate=25:duration=4",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", str(src / "clip2.mp4"))
    for category, colour in (("character", (40, 80, 200)), ("outfit", (200, 60, 60)),
                             ("prop", (60, 160, 60))):
        for n in range(2 if category == "outfit" else 1):
            image = np.full((400, 300, 3), colour, np.uint8)
            cv2.circle(image, (150, 200), 60 + 20 * n, (255, 255, 255), -1)
            image_ops.write_image(root / "assets" / category / f"ảnh_{n}.png", image)


def fake_flow(project: planner.Project) -> None:
    """Stand-in for Flow: different resolution, ~5 % shorter, slightly warmer colours."""
    for job in json.loads((project.work / "flow_jobs.json").read_text(encoding="utf-8")):
        ffmpeg("-i", str(project.work / job["upload"]),
               "-vf", "setpts=PTS*0.95,scale=720:1280,eq=gamma_r=1.05",
               "-c:v", "libx264", "-pix_fmt", "yuv420p",
               str(project.work / "outputs" / f"{job['id']}.mp4"))


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        make_sources(root)
        config = root / "project.json"
        config.write_text(json.dumps({
            "name": "smoke",
            "sources": ["nguồn/clip1.mp4", "nguồn/clip2.mp4"],
            "identity_lock": "IDENTITY LOCK",
            "end_lock": "END LOCK",
            "subject_in_source": "the cyclist",
            "background_prompt": "a quiet street at dawn",
            "segmenting": {"max_segment_seconds": 4, "overlap_seconds": 0.5},
            "output": {"width": 360, "height": 640, "fps": 30},
        }), encoding="utf-8")

        assert motion_copy.main(["prepare", str(config)]) == 0
        project = planner.Project(config)
        _, segments = project.load_plan()
        # clip1: 6 s shot -> 2 pieces (overlapping), 3 s shot -> 1; clip2: 4 s -> 2 pieces.
        assert [s.overlap > 0 for s in segments] == [True, False, False, True, False], segments
        jobs = json.loads((project.work / "flow_jobs.json").read_text(encoding="utf-8"))
        assert jobs[0]["prompt"].startswith("IDENTITY LOCK") and "bicycle in ingredient 3" in jobs[0]["prompt"]

        fake_flow(project)
        assert motion_copy.main(["check", str(config), "--approve-anchor"]) in (0, 1)
        assert project.hero_path.is_file()
        jobs = json.loads((project.work / "flow_jobs.json").read_text(encoding="utf-8"))
        assert "Continuity" in jobs[1]["prompt"] and len(jobs[1]["ingredients"]) == 4
        assert (project.work / "qc" / "contact_sheet.png").is_file()

        assert motion_copy.main(["assemble", str(config)]) == 0
        final = video_ops.probe(project.work / "final.mp4")
        assert (final["width"], final["height"]) == (360, 640), final
        assert abs(final["duration"] - 13.0) < 0.15, final
        assert final["has_audio"], final
        print((project.work / "qc" / "report.md").read_text(encoding="utf-8"))
        print(f"Smoke test passed: final video {final['duration']:.2f}s, {final['width']}x{final['height']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

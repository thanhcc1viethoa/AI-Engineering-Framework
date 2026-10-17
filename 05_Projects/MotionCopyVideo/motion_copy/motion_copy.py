#!/usr/bin/env python3
"""Motion Copy Video — Google Flow helper for long, consistent character videos.

  prepare  <project.json>                     split sources, build reference pack + Flow job sheet
  jobs     <project.json>                     rebuild the job sheet (after changing prompts/assets)
  check    <project.json> [--approve-anchor]  QC the downloaded Flow clips, write report + contact sheet
  assemble <project.json> [--output FILE]     join all clips into one video with the original audio
  lastframe <video> <image>                   export the last frame (for Flow "Frames to video")

Exit codes: 0 = done / all clips pass, 1 = clips need attention, 2 = error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import assembler
import image_ops
import planner
import qc
import video_ops


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="motion_copy", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("prepare", "jobs", "check", "assemble"):
        cmd = sub.add_parser(name)
        cmd.add_argument("project", type=Path)
        if name == "check":
            cmd.add_argument("--approve-anchor", action="store_true",
                             help="you inspected the anchor clip and accept it as the continuity reference")
        if name == "assemble":
            cmd.add_argument("--output", type=Path)
    last = sub.add_parser("lastframe")
    last.add_argument("video", type=Path)
    last.add_argument("image", type=Path)
    args = parser.parse_args(argv)

    try:
        if args.command == "lastframe":
            info = video_ops.probe(args.video)
            frame = video_ops.grab_frame(args.video, video_ops.last_frame_time(info["duration"], info["fps"]))
            image_ops.write_image(args.image, frame)
            print(f"Last frame written to {args.image}")
            return 0

        project = planner.Project(args.project)
        if args.command == "prepare":
            segments = planner.prepare(project)
            print(f"{len(segments)} segments ready. Next: follow {project.work / 'flow_jobs.md'}")
        elif args.command == "jobs":
            _, segments = project.load_plan()
            sheet = planner.write_job_sheet(project, planner.build_reference_pack(project), segments)
            print(f"Job sheet updated: {sheet}")
        elif args.command == "check":
            reports, path = qc.check(project, approve_anchor=args.approve_anchor)
            for r in reports:
                print(f"  {r.segment.id}: {r.status}" + (f" — {'; '.join(r.issues)}" if r.issues else ""))
            print(f"Report: {path}")
            return 0 if all(r.status == "PASS" for r in reports) else 1
        elif args.command == "assemble":
            output = assembler.assemble(project, args.output)
            print(f"Final video: {output}")
        return 0
    except (planner.ConfigError, video_ops.VideoOpsError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

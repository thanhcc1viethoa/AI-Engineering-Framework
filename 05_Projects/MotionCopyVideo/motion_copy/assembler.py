"""Join the generated clips into one long video on the source timeline."""

from __future__ import annotations

from pathlib import Path

import image_ops
import planner
import qc
import video_ops


def assemble(project: planner.Project, output: Path | None = None) -> Path:
    video_ops.require_tools()
    sources, segments = project.load_plan()
    out_cfg = project.cfg["output"]
    anchor_id = f"seg_{int(project.cfg['anchor_segment']):03d}"

    missing = [s.id for s in segments if project.output_for(s) is None]
    if missing:
        raise planner.ConfigError("Missing Flow outputs in work/outputs: " + ", ".join(missing))

    clips = {s.id: project.output_for(s) for s in segments}
    infos = {sid: video_ops.probe(path) for sid, path in clips.items()}

    anchor_stats = None
    if out_cfg["color_match"]:
        anchor = anchor_id if anchor_id in clips else segments[0].id
        anchor_stats = image_ops.colour_stats(
            video_ops.sample_frames(clips[anchor], infos[anchor]["duration"], qc.SAMPLES)
        )

    normalized = []
    for segment in segments:
        info = infos[segment.id]
        stretch = qc.stretch_for(segment.need, info["duration"])
        if stretch > float(out_cfg["max_stretch"]):
            raise planner.ConfigError(
                f"{segment.id} is {info['duration']:.2f}s but {segment.need:.2f}s is needed; "
                "regenerate it longer in Flow."
            )
        lut = None
        if anchor_stats is not None and segment.id != anchor_id:
            stats = image_ops.colour_stats(
                video_ops.sample_frames(clips[segment.id], info["duration"], qc.SAMPLES)
            )
            lut = image_ops.colour_match_lut(stats, anchor_stats)
        target = project.work / "normalized" / f"{segment.id}.mp4"
        video_ops.normalize_clip(
            clips[segment.id], target, need=segment.need,
            width=int(out_cfg["width"]), height=int(out_cfg["height"]), fps=float(out_cfg["fps"]),
            fit=out_cfg["fit"], stretch=stretch, color_lut=lut,
        )
        normalized.append(target)

    output = output or project.work / "final.mp4"
    args, graph, video_label = build_join_graph(segments, normalized)
    total = sum(s.core for s in segments)

    if out_cfg["audio"] == "source":
        audio_parts = []
        for i, source in enumerate(sources):
            if source["has_audio"]:
                args += ["-i", str(project.sources[i])]
                index = len(args) // 2 - 1
                audio_parts.append(
                    f"[{index}:a]atrim=0:{source['duration']:.3f},asetpts=PTS-STARTPTS,"
                    "aresample=48000,aformat=channel_layouts=stereo"
                )
            else:
                audio_parts.append(
                    f"anullsrc=r=48000:cl=stereo,atrim=0:{source['duration']:.3f},asetpts=PTS-STARTPTS"
                )
        for i, part in enumerate(audio_parts):
            graph.append(f"{part}[a{i}]")
        graph.append("".join(f"[a{i}]" for i in range(len(audio_parts)))
                     + f"concat=n={len(audio_parts)}:v=0:a=1[aout]")
        maps = ["-map", video_label, "-map", "[aout]", "-c:a", "aac", "-b:a", "192k"]
    else:
        maps = ["-map", video_label]

    output.parent.mkdir(parents=True, exist_ok=True)
    video_ops.run_ffmpeg([
        *args, "-filter_complex", ";".join(graph), *maps,
        "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output),
    ])
    return output


def build_join_graph(segments: list[planner.Segment], clips: list[Path]) -> tuple[list[str], list[str], str]:
    """Cross-fade over the shared overlap inside a shot; hard cut at real scene cuts.

    Each clip lasts core + overlap, and the cross-fade consumes the overlap,
    so the result is exactly as long as the sources and every original cut
    lands on its original timestamp (keeping the rhythm and the audio in sync).
    """
    args, graph = [], []
    for i, clip in enumerate(clips):
        args += ["-i", str(clip)]
        graph.append(f"[{i}:v]settb=AVTB,setpts=PTS-STARTPTS[v{i}]")
    current, length = "[v0]", segments[0].need
    for i in range(1, len(clips)):
        previous = segments[i - 1]
        label = f"[j{i}]"
        if previous.overlap > 0:
            offset = length - previous.overlap
            graph.append(
                f"{current}[v{i}]xfade=transition=fade:duration={previous.overlap:.3f}:"
                f"offset={offset:.3f}{label}"
            )
            length = offset + segments[i].need
        else:
            graph.append(f"{current}[v{i}]concat=n=2:v=1:a=0{label}")
            length += segments[i].need
        current = label
    if len(clips) == 1:
        graph.append("[v0]null[vout]")
    else:
        graph.append(f"{current}null[vout]")
    return args, graph, "[vout]"

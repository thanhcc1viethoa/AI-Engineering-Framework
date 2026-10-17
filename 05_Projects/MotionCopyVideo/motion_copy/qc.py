"""Consistency check of the clips generated in Flow.

The metrics are colour/continuity heuristics, not identity recognition:
they catch outfit or bike colour drift and visible jumps at joins. Face,
mole, watch side and bike shape are judged by a person on the contact sheet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import image_ops
import planner
import video_ops

SAMPLES = 5


@dataclass
class ClipReport:
    segment: planner.Segment
    output: Path | None = None
    duration: float = 0.0
    stretch: float = 1.0
    similarity: float | None = None
    source_similarity: float | None = None
    seam: float | None = None
    issues: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        if self.output is None:
            return "MISSING"
        return "CHECK" if self.issues else "PASS"


def stretch_for(need: float, duration: float) -> float:
    """Slow-down factor applied at assembly; 1.0 when the clip is long enough (it is trimmed)."""
    return need / duration if duration < need else 1.0


def check(project: planner.Project, approve_anchor: bool = False) -> tuple[list[ClipReport], Path]:
    video_ops.require_tools()
    _, segments = project.load_plan()
    qc_cfg, out_cfg = project.cfg["qc"], project.cfg["output"]
    anchor_id = f"seg_{int(project.cfg['anchor_segment']):03d}"
    reports = [ClipReport(segment=s, output=project.output_for(s)) for s in segments]

    signatures, source_signatures, sheet_rows = {}, {}, []
    for report in reports:
        segment = report.segment
        source_clip = project.work / segment.file
        source_frames = video_ops.sample_frames(source_clip, segment.need, SAMPLES)
        source_signatures[segment.id] = image_ops.colour_signature(source_frames)
        if report.output is None:
            continue
        info = video_ops.probe(report.output)
        report.duration = info["duration"]
        report.stretch = stretch_for(segment.need, info["duration"])
        if report.stretch > float(out_cfg["max_stretch"]):
            report.issues.append(
                f"too short: {info['duration']:.2f}s for {segment.need:.2f}s needed"
            )
        frames = video_ops.sample_frames(report.output, info["duration"], SAMPLES)
        signatures[segment.id] = image_ops.colour_signature(frames)
        end = video_ops.grab_frame(report.output, video_ops.last_frame_time(info["duration"], info["fps"]))
        sheet_rows.append((segment.id, [source_frames[SAMPLES // 2], frames[0], frames[SAMPLES // 2], end]))

    if anchor_id in signatures:
        for report in reports:
            sid = report.segment.id
            if sid not in signatures or sid == anchor_id:
                continue
            report.similarity = image_ops.signature_similarity(signatures[sid], signatures[anchor_id])
            report.source_similarity = image_ops.signature_similarity(
                source_signatures[sid], source_signatures[anchor_id]
            )
            # Only flag drift the source itself does not explain (e.g. a new scene).
            if report.similarity < float(qc_cfg["consistency_min"]) and \
                    report.similarity < report.source_similarity - 0.1:
                report.issues.append("colours drift from the anchor clip (outfit / prop / skin?)")

    for current, following in zip(reports, reports[1:]):
        seg = current.segment
        if seg.overlap <= 0 or current.output is None or following.output is None:
            continue
        mid = seg.overlap / 2
        a = video_ops.grab_frame(current.output, (seg.core + mid) / current.stretch)
        b = video_ops.grab_frame(following.output, mid / following.stretch)
        current.seam = image_ops.frame_difference(a, b)
        if current.seam > float(qc_cfg["seam_max"]):
            current.issues.append(f"visible jump into {following.segment.id} (overlap frames differ)")

    qc_dir = project.work / "qc"
    refs = [image_ops.read_image(p) for p in sorted((project.work / "refs").glob("*.png"))]
    if sheet_rows:
        rows = ([("refs", refs)] if refs else []) + sheet_rows
        image_ops.write_image(qc_dir / "contact_sheet.png", image_ops.contact_sheet(rows))

    anchor_report = next((r for r in reports if r.segment.id == anchor_id), None)
    if approve_anchor:
        if anchor_report is None or anchor_report.output is None:
            raise planner.ConfigError(f"Cannot approve anchor: {anchor_id} has no output yet.")
        frame = video_ops.grab_frame(anchor_report.output, anchor_report.duration / 2)
        image_ops.write_image(project.hero_path, frame)
        planner.write_job_sheet(project, planner.build_reference_pack(project), segments)

    report_path = qc_dir / "report.md"
    qc_dir.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(project, reports, anchor_id), encoding="utf-8")
    return reports, report_path


def _fmt(value: float | None, digits: int = 2) -> str:
    return "–" if value is None else f"{value:.{digits}f}"


def render_report(project: planner.Project, reports: list[ClipReport], anchor_id: str) -> str:
    lines = [
        "# QC report", "",
        f"Anchor segment: `{anchor_id}`"
        + (" (approved, anchor frame exported)" if project.hero_path.is_file() else " (not approved yet)"),
        "",
        "Open `work/qc/contact_sheet.png`: row `refs` = your references; each segment row = "
        "source mid frame, output start, mid, end. Check face, hair, outfit, accessories, "
        f"{project.cfg['prop_label']} shape against the refs.", "",
        "| Segment | Status | Duration out/need (s) | Colour vs anchor out/source | Seam to next | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in reports:
        seg = r.segment
        lines.append(
            f"| {seg.id} | {r.status} | {_fmt(r.duration)}/{seg.need:.2f} | "
            f"{_fmt(r.similarity)}/{_fmt(r.source_similarity)} | {_fmt(r.seam, 3)} | "
            f"{'; '.join(r.issues) or ''} |"
        )
    flagged = [r for r in reports if r.status == "CHECK"]
    if flagged:
        lines += ["", "## Regenerate only these segments", ""]
        for r in flagged:
            lines.append(
                f"- **{r.segment.id}**: same upload, same ingredients, same prompt from `flow_jobs.md`, "
                f"plus: \"Fix only: {'; '.join(r.issues)}. Everything else must stay as in the prompt.\""
            )
    missing = [r.segment.id for r in reports if r.status == "MISSING"]
    if missing:
        lines += ["", "Missing outputs: " + ", ".join(f"`{m}`" for m in missing)]
    return "\n".join(lines) + "\n"

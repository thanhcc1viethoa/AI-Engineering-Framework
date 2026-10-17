"""Project config, segment plan, reference pack and Flow job sheet."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from image_ops import build_board, list_images, write_image
import video_ops

# Ingredient categories in the fixed order they are attached in Flow.
# The order never changes between segments: same references, same numbering.
CATEGORIES = ("character", "outfit", "accessories", "prop", "background")

DEFAULTS = {
    "subject_in_source": "the main person",
    "prop_label": "bicycle",
    "background_prompt": "",
    "identity_lock": "",
    "end_lock": "",
    "anchor_segment": 1,
    "max_ingredients": 5,
    "segmenting": {
        "max_segment_seconds": 8.0,
        "overlap_seconds": 0.5,
        "scene_threshold": 0.4,
        "min_segment_seconds": 1.0,
    },
    "output": {
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "fit": "crop",
        "color_match": True,
        "audio": "source",
        "max_stretch": 1.15,
    },
    "qc": {"consistency_min": 0.6, "seam_max": 0.12},
}


class ConfigError(ValueError):
    """Raised for a missing or invalid project.json value."""


@dataclass
class Segment:
    id: str
    source_index: int
    start: float
    core: float      # seconds this segment owns on the final timeline
    overlap: float   # extra seconds shared with the next segment (cross-faded)
    file: str        # source cut to upload to Flow, relative to work/

    @property
    def need(self) -> float:
        return self.core + self.overlap


class Project:
    def __init__(self, config_path: Path):
        self.config_path = config_path.resolve()
        self.root = self.config_path.parent
        self.work = self.root / "work"
        try:
            raw = json.loads(self.config_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ConfigError(f"Cannot read {config_path}: {exc}") from exc
        self.cfg = {**DEFAULTS, **raw}
        for section in ("segmenting", "output", "qc"):
            self.cfg[section] = {**DEFAULTS[section], **raw.get(section, {})}
        self.sources = [self.root / s for s in self.cfg.get("sources", [])]
        if not self.sources:
            raise ConfigError('"sources" must list at least one video.')
        for source in self.sources:
            if not source.is_file():
                raise ConfigError(f"Source video not found: {source}")
        seg = self.cfg["segmenting"]
        if not 0 <= seg["overlap_seconds"] < seg["max_segment_seconds"] / 2:
            raise ConfigError("overlap_seconds must be >= 0 and < max_segment_seconds / 2.")
        if self.cfg["output"]["fit"] not in ("crop", "pad"):
            raise ConfigError('output.fit must be "crop" or "pad".')
        if self.cfg["output"]["audio"] not in ("source", "none"):
            raise ConfigError('output.audio must be "source" or "none".')

    # ---- paths -----------------------------------------------------------
    def asset_dir(self, category: str) -> Path:
        return self.root / self.cfg.get("assets", {}).get(category, f"assets/{category}")

    @property
    def plan_path(self) -> Path:
        return self.work / "plan.json"

    @property
    def hero_path(self) -> Path:
        return self.work / "refs" / "anchor_frame.png"

    def output_for(self, segment: Segment) -> Path | None:
        for ext in (".mp4", ".mov", ".webm", ".mkv"):
            candidate = self.work / "outputs" / f"{segment.id}{ext}"
            if candidate.is_file():
                return candidate
        return None

    # ---- plan --------------------------------------------------------------
    def load_plan(self) -> tuple[list[dict], list[Segment]]:
        if not self.plan_path.is_file():
            raise ConfigError('No plan yet. Run "prepare" first.')
        data = json.loads(self.plan_path.read_text(encoding="utf-8"))
        return data["sources"], [Segment(**s) for s in data["segments"]]


def split_shots(duration: float, cuts: list[float], min_len: float) -> list[tuple[float, float]]:
    """Shots between hard cuts; shots shorter than min_len merge into the previous one."""
    edges = [0.0] + [c for c in cuts if 0 < c < duration] + [duration]
    shots: list[list[float]] = []
    for start, end in zip(edges, edges[1:]):
        if shots and end - start < min_len:
            shots[-1][1] = end
        else:
            shots.append([start, end])
    if len(shots) > 1 and shots[0][1] - shots[0][0] < min_len:
        shots[1][0] = shots[0][0]
        shots.pop(0)
    return [(s, e) for s, e in shots]


def plan_segments(
    source_index: int, duration: float, cuts: list[float], seg_cfg: dict, start_number: int
) -> list[Segment]:
    """Cut every shot into Flow-sized pieces.

    Technique from the sliding-window generators (Wan2GP/VACE, MimicMotion's
    progressive fusion): pieces inside one continuous shot overlap a little so
    the joins can be cross-faded instead of jumping. Pieces at a real scene
    cut do not overlap, because a hard cut is the original rhythm.
    """
    overlap = float(seg_cfg["overlap_seconds"])
    max_core = float(seg_cfg["max_segment_seconds"]) - overlap
    segments: list[Segment] = []
    for shot_start, shot_end in split_shots(duration, cuts, float(seg_cfg["min_segment_seconds"])):
        length = shot_end - shot_start
        pieces = max(1, math.ceil(length / max_core - 1e-6))
        core = length / pieces
        for p in range(pieces):
            number = start_number + len(segments)
            segments.append(Segment(
                id=f"seg_{number:03d}",
                source_index=source_index,
                start=round(shot_start + p * core, 3),
                core=round(core, 3),
                overlap=overlap if p < pieces - 1 else 0.0,
                file=f"segments/seg_{number:03d}.mp4",
            ))
    return segments


def build_reference_pack(project: Project) -> list[tuple[str, Path]]:
    """One board image per non-empty category, in the fixed ingredient order."""
    pack = []
    for category in CATEGORIES:
        images = list_images(project.asset_dir(category))
        if not images:
            continue
        target = project.work / "refs" / f"{len(pack) + 1}_{category}.png"
        write_image(target, build_board(images))
        pack.append((category, target))
    if not pack or pack[0][0] != "character":
        raise ConfigError(f"No character images found in {project.asset_dir('character')}.")
    return pack


def prepare(project: Project) -> list[Segment]:
    video_ops.require_tools()
    seg_cfg = project.cfg["segmenting"]
    sources, segments = [], []
    for index, source in enumerate(project.sources):
        info = video_ops.probe(source)
        cuts = video_ops.detect_scene_cuts(source, float(seg_cfg["scene_threshold"]))
        sources.append({"path": str(source), **info, "cuts": cuts})
        segments += plan_segments(index, info["duration"], cuts, seg_cfg, len(segments) + 1)
    for segment in segments:
        video_ops.cut_segment(
            project.sources[segment.source_index], segment.start, segment.need,
            project.work / segment.file,
        )
    project.work.mkdir(parents=True, exist_ok=True)
    project.plan_path.write_text(
        json.dumps({"sources": sources, "segments": [asdict(s) for s in segments]}, indent=2),
        encoding="utf-8",
    )
    (project.work / "outputs").mkdir(exist_ok=True)
    write_job_sheet(project, build_reference_pack(project), segments)
    return segments


# ---- Flow job sheet ---------------------------------------------------------

def segment_prompt(project: Project, pack: list[tuple[str, Path]], use_anchor: bool) -> str:
    cfg = project.cfg
    number = {category: i + 1 for i, (category, _) in enumerate(pack)}
    if use_anchor:
        number["anchor"] = len(pack) + 1
    lines = []
    if cfg["identity_lock"]:
        lines.append(cfg["identity_lock"].strip())
    wear = f"Replace {cfg['subject_in_source']} in the uploaded video with the character in ingredient {number['character']}"
    if "outfit" in number:
        wear += f", wearing exactly the outfit in ingredient {number['outfit']}"
    if "accessories" in number:
        wear += f", with exactly the accessories in ingredient {number['accessories']}"
    if "prop" in number:
        wear += f", using exactly the {cfg['prop_label']} in ingredient {number['prop']} (same model, frame shape and colours)"
    lines.append(wear + ".")
    if cfg["background_prompt"] or "background" in number:
        where = cfg["background_prompt"] or f"the place in ingredient {number['background']}"
        lines.append(f"Change the background to {where}, with the same camera motion.")
    elif use_anchor and list_images(project.asset_dir("background")):
        lines.append(f"Use the same background as ingredient {number['anchor']}, with the same camera motion.")
    else:
        lines.append("Keep the original background, lighting and camera motion.")
    lines.append(
        "Keep the exact body movement, timing, rhythm, gestures and facial expressions of the "
        "uploaded video, frame by frame. Do not add or remove actions. No text, no logos, no subtitles."
    )
    if use_anchor:
        lines.append(
            f"Continuity: ingredient {number['anchor']} is an approved frame of this same video. Match its "
            f"face, hair, outfit colours, accessories and {cfg['prop_label']} exactly."
        )
    if cfg["end_lock"]:
        lines.append(cfg["end_lock"].strip())
    return "\n".join(lines)


def write_job_sheet(project: Project, pack: list[tuple[str, Path]], segments: list[Segment]) -> Path:
    anchor_id = f"seg_{int(project.cfg['anchor_segment']):03d}"
    anchor_ready = project.hero_path.is_file()
    jobs, md = [], [
        "# Flow job sheet", "",
        f"Project: `{project.cfg.get('name', project.root.name)}` — {len(segments)} segments.", "",
        "For each segment: open Google Flow, upload the segment video, attach the ingredients in the "
        "order listed, paste the prompt, generate, then download the result as "
        "`work/outputs/<segment id>.mp4`.", "",
        f"Do **{anchor_id}** first. When you accept it, run `check --approve-anchor`: an anchor "
        "frame is exported and this sheet is rebuilt so every other segment gets it as a "
        "continuity ingredient.", "",
    ]
    limit = int(project.cfg["max_ingredients"])
    for segment in segments:
        use_anchor = anchor_ready and segment.id != anchor_id
        # The anchor frame already shows the new background, so it takes the
        # background board's slot and the ingredient count stays within Flow's limit.
        refs = [(c, p) for c, p in pack if not (use_anchor and c == "background")]
        ingredients = [p.relative_to(project.work).as_posix() for _, p in refs]
        if use_anchor:
            ingredients.append(project.hero_path.relative_to(project.work).as_posix())
        if len(ingredients) > limit:
            raise ConfigError(
                f"{segment.id} needs {len(ingredients)} ingredients but max_ingredients is {limit}. "
                "Merge two asset folders (e.g. accessories into outfit)."
            )
        prompt = segment_prompt(project, refs, use_anchor)
        jobs.append({"id": segment.id, "upload": segment.file, "ingredients": ingredients,
                     "prompt": prompt, "target_seconds": round(segment.need, 3)})
        md += [
            f"## {segment.id}", "",
            f"- Upload: `{segment.file}` ({segment.need:.2f} s)",
            "- Ingredients: " + ", ".join(f"{i + 1}. `{name}`" for i, name in enumerate(ingredients)),
            "", "```", prompt, "```", "",
        ]
    (project.work / "flow_jobs.json").write_text(json.dumps(jobs, indent=2, ensure_ascii=False), encoding="utf-8")
    sheet = project.work / "flow_jobs.md"
    sheet.write_text("\n".join(md), encoding="utf-8")
    return sheet

"""Python Automation Agent — Requirement.md FR-009.

Runs only a fixed, whitelisted set of actions — never an arbitrary shell
command or string of code — per Requirement.md FR-027 ("block arbitrary
command execution"). Add new automation capabilities by registering a new
named action here.
"""

import shutil
from pathlib import Path

_REGISTRY = {}


def register(name: str):
    def decorator(fn):
        _REGISTRY[name] = fn
        return fn

    return decorator


@register("list_directory")
def _list_directory(payload: dict) -> dict:
    path = Path(payload["path"])
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Not a directory: {path}")
    return {"entries": sorted(p.name for p in path.iterdir())}


@register("copy_file")
def _copy_file(payload: dict) -> dict:
    source = Path(payload["source"])
    destination = Path(payload["destination"])
    if not source.exists():
        raise ValueError(f"Source does not exist: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return {"output_path": str(destination)}


@register("zip_directory")
def _zip_directory(payload: dict) -> dict:
    source_dir = Path(payload["source_dir"])
    dest_archive = Path(payload["dest_archive"])
    if not source_dir.exists() or not source_dir.is_dir():
        raise ValueError(f"Not a directory: {source_dir}")
    dest_archive.parent.mkdir(parents=True, exist_ok=True)
    archive_path = shutil.make_archive(str(dest_archive.with_suffix("")), "zip", root_dir=str(source_dir))
    return {"output_path": archive_path}


def run_automation(payload: dict) -> dict:
    action = payload.get("action")
    if action not in _REGISTRY:
        raise ValueError(f"Unknown automation action '{action}'. Allowed: {sorted(_REGISTRY)}")
    return _REGISTRY[action](payload)

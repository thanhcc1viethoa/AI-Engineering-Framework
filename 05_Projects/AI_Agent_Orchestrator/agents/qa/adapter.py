"""QA Agent — Requirement.md FR-010.

Checks a real, already-recorded task outcome. Never guesses a verdict for a
task it cannot inspect.
"""

from pathlib import Path
from typing import Optional


def check_task_output(target_task) -> dict:
    """``target_task`` is a ``models.Task`` (or ``None`` if not found)."""
    if target_task is None:
        return {"passed": False, "reason": "target task not found"}

    if target_task.status != "COMPLETED":
        return {"passed": False, "reason": f"target task status is {target_task.status}, not COMPLETED"}

    if target_task.error_message:
        return {"passed": False, "reason": f"target task recorded an error: {target_task.error_message}"}

    output_path: Optional[str] = target_task.output_path
    if output_path and not Path(output_path).exists():
        return {"passed": False, "reason": f"declared output_path does not exist: {output_path}"}

    return {"passed": True, "reason": "task completed with no recorded error and output_path (if any) exists"}

"""Antigravity CLI adapter — Requirement.md FR-007.

UNVERIFIED (Requirement.md AS-001): the exact non-interactive flag/argument
syntax below (`run --non-interactive --prompt ...`) has not been confirmed
against a real Antigravity CLI installation, because this adapter was written
in a cloud container with no Antigravity CLI available. Before relying on
this in production, run `agy --help` on the target Windows machine and
correct the `command` list in `run_coding_task` if the real syntax differs.
"""

import subprocess
import time
from pathlib import Path


class AntigravityError(Exception):
    pass


def check_cli_available(cli_path: str) -> bool:
    try:
        result = subprocess.run([cli_path, "--version"], capture_output=True, timeout=10)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def run_coding_task(cli_path: str, project_dir: Path, instructions: str, timeout_seconds: int) -> dict:
    """Invoke the Antigravity CLI non-interactively, scoped to project_dir only."""
    project_dir.mkdir(parents=True, exist_ok=True)
    command = [cli_path, "run", "--non-interactive", "--prompt", instructions]

    started = time.monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError as exc:
        raise AntigravityError(f"Antigravity CLI not found at '{cli_path}'") from exc
    except subprocess.TimeoutExpired as exc:
        raise AntigravityError(f"Antigravity CLI timed out after {timeout_seconds}s") from exc

    duration = time.monotonic() - started
    if result.returncode != 0:
        raise AntigravityError(
            f"Antigravity CLI exited with code {result.returncode}: {result.stderr.strip()[:2000]}"
        )

    return {
        "stdout": result.stdout[-5000:],
        "duration_seconds": duration,
        "output_path": str(project_dir),
    }

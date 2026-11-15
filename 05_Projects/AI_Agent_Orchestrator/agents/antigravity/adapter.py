"""Antigravity CLI adapter — Requirement.md FR-007 / AS-001.

Google Antigravity ships three separate surfaces that share one underlying
agent harness (per public reporting, not Google's own docs — see caveats
below): the original Antigravity IDE, the Antigravity CLI (`agy`), and, since
Antigravity 2.0 (announced I/O 2026), a standalone Antigravity Desktop app —
a GUI/voice "agent command center" for a human to drive directly (parallel
subagents, scheduled background tasks), not something built to be scripted
by another backend. **This adapter integrates the CLI, not the Desktop app**,
because the CLI is the documented, scriptable, non-interactive surface; the
Desktop app has no documented API for a third party to call.

Headless CLI syntax below (`agy --print "<prompt>" --print-timeout ...`) is
taken from Google's own headless-mode docs page (antigravity.google/docs/cli/
headless.md) as summarized by third-party sources — this cloud container's
network policy blocks fetching that page directly, and no `agy` binary is
available here to run `agy --help` against, so **this is still one level
short of hands-on verification (AS-001 is not fully resolved)**. Confirm with
`agy --help` on the real Windows machine before depending on this in
production, and correct `run_coding_task` below if it differs.

Known open risks from that same research, not yet confirmed fixed or current:
* Several reports describe `agy --print`/`agy -p` hanging, or silently
  dropping stdout, when its output is piped/redirected rather than a real
  terminal (a non-TTY) — exactly the situation `subprocess.run(capture_output=
  True)` below creates. If tasks sent to this adapter hang or return empty
  output on the real machine, this is the first thing to check.
* The exact mechanism for non-interactive authentication (a one-time
  interactive `agy` login first, vs. an environment variable such as
  `ANTIGRAVITY_TOKEN`) was not confirmed from an authoritative source.
"""

import shlex
import subprocess
import time
from pathlib import Path
from typing import Optional


class AntigravityError(Exception):
    pass


def check_cli_available(cli_path: str) -> bool:
    try:
        result = subprocess.run([cli_path, "--version"], capture_output=True, timeout=10)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def run_coding_task(
    cli_path: str,
    project_dir: Path,
    instructions: str,
    timeout_seconds: int,
    test_command: Optional[str] = None,
) -> dict:
    """Invoke the Antigravity CLI's headless mode, scoped to project_dir only.

    If this hangs or returns empty stdout on the real machine, see the
    non-TTY caveat in this module's docstring before assuming it is a bug in
    this adapter.

    `test_command` (optional, e.g. "pytest" or "npm test"): run in
    project_dir after the coding step succeeds, per the Antigravity Agent
    subsystem spec's requirement that a task record real test results, not
    just Antigravity's own claim of success. If omitted, `test_result` is
    None — nothing about test coverage is assumed or fabricated.

    `files` in the return value is every file present under project_dir
    after the run (not a git-style diff — project_dir has no git repo by
    default), so it also includes files from an earlier attempt in the same
    project_dir (exception retries and review-rejection retries reuse it).
    """
    project_dir.mkdir(parents=True, exist_ok=True)
    command = [cli_path, "--print", instructions, "--print-timeout", f"{timeout_seconds}s"]

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
    if not result.stdout.strip():
        raise AntigravityError(
            "Antigravity CLI exited 0 but produced no output — this matches a reported "
            "non-TTY stdout issue with `agy --print`, not necessarily a real failure; "
            "check the project directory for actual changes before treating this as failed."
        )

    files = sorted(str(p.relative_to(project_dir)) for p in project_dir.rglob("*") if p.is_file())

    test_result = _run_test_command(test_command, project_dir, timeout_seconds) if test_command else None

    return {
        "stdout": result.stdout[-5000:],
        "duration_seconds": duration,
        "output_path": str(project_dir),
        "files": files,
        "test_command": test_command,
        "test_result": test_result,
    }


def _run_test_command(test_command: str, project_dir: Path, timeout_seconds: int) -> dict:
    """Runs a simple space-separated command (shlex/POSIX splitting — complex
    Windows-specific quoting in test_command is not handled)."""
    try:
        result = subprocess.run(
            shlex.split(test_command),
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return {
            "exit_code": result.returncode,
            "passed": result.returncode == 0,
            "output": (result.stdout + result.stderr)[-3000:],
        }
    except FileNotFoundError as exc:
        return {"exit_code": None, "passed": False, "output": f"Test command not found: {exc}"}
    except subprocess.TimeoutExpired:
        return {"exit_code": None, "passed": False, "output": f"Test command timed out after {timeout_seconds}s"}

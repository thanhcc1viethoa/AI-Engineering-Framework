"""Report Generator — Requirement.md FR-020.

Aggregates verified state from the database for Claude's final report and for
the dashboard Overview page / health_check.ps1. Never fabricates a count.
"""

import time

from db import get_connection

_START_TIME = time.monotonic()


def get_system_status() -> dict:
    conn = get_connection()
    try:
        agents_total = conn.execute("SELECT COUNT(*) AS c FROM agents").fetchone()["c"]
        agents_active = conn.execute(
            "SELECT COUNT(*) AS c FROM agents WHERE status = 'BUSY'"
        ).fetchone()["c"]
        tasks_running = conn.execute(
            "SELECT COUNT(*) AS c FROM tasks WHERE status = 'RUNNING'"
        ).fetchone()["c"]
        tasks_completed = conn.execute(
            "SELECT COUNT(*) AS c FROM tasks WHERE status = 'COMPLETED'"
        ).fetchone()["c"]
        tasks_failed = conn.execute(
            "SELECT COUNT(*) AS c FROM tasks WHERE status = 'FAILED'"
        ).fetchone()["c"]
        videos_created = conn.execute(
            "SELECT COUNT(*) AS c FROM tasks WHERE assigned_agent = 'muse' AND status = 'COMPLETED'"
        ).fetchone()["c"]
    finally:
        conn.close()

    return {
        "agents_total": agents_total,
        "agents_active": agents_active,
        "tasks_running": tasks_running,
        "tasks_completed": tasks_completed,
        "tasks_failed": tasks_failed,
        "videos_created": videos_created,
        "uptime_seconds": time.monotonic() - _START_TIME,
    }

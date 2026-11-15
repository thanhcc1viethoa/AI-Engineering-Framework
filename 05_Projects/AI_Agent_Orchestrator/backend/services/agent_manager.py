"""Agent Manager — Requirement.md FR-004."""

import json
import sqlite3
from datetime import datetime, timezone
from typing import Optional

from db import get_connection
from models import Agent, AgentStatus


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _row_to_agent(row: sqlite3.Row) -> Agent:
    return Agent(
        agent_id=row["agent_id"],
        name=row["name"],
        type=row["type"],
        status=row["status"],
        capabilities=json.loads(row["capabilities"]) if row["capabilities"] else [],
        current_task=row["current_task"],
        last_active=row["last_active"],
        error_log=row["error_log"],
    )


def list_agents() -> list[Agent]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM agents ORDER BY agent_id").fetchall()
    finally:
        conn.close()
    return [_row_to_agent(r) for r in rows]


def get_agent(agent_id: str) -> Optional[Agent]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM agents WHERE agent_id = ?", (agent_id,)).fetchone()
    finally:
        conn.close()
    return _row_to_agent(row) if row else None


def get_agent_by_type(agent_type: str) -> Optional[Agent]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM agents WHERE type = ?", (agent_type,)).fetchone()
    finally:
        conn.close()
    return _row_to_agent(row) if row else None


def set_agent_status(
    agent_id: str, status: AgentStatus, current_task: Optional[str] = None
) -> Optional[Agent]:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE agents SET status = ?, current_task = ?, last_active = ? WHERE agent_id = ?",
            (status.value, current_task, _now(), agent_id),
        )
        conn.commit()
    finally:
        conn.close()
    return get_agent(agent_id)


def log_agent_error(agent_id: str, message: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE agents SET error_log = ?, last_active = ? WHERE agent_id = ?",
            (message, _now(), agent_id),
        )
        conn.commit()
    finally:
        conn.close()

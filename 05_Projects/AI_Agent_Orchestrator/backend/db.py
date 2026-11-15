"""SQLite connection and schema migration.

Schema matches Antigravity_Build_Guide.md section 6.1 and Requirement.md FR-003/FR-004.
"""

import sqlite3
from pathlib import Path

from config import SQLITE_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    task_id         TEXT PRIMARY KEY,
    task_name       TEXT NOT NULL,
    description     TEXT,
    assigned_agent  TEXT NOT NULL,
    priority        TEXT NOT NULL DEFAULT 'Medium',
    status          TEXT NOT NULL DEFAULT 'PENDING',
    payload         TEXT,
    result          TEXT,
    error_message   TEXT,
    output_path     TEXT,
    workflow_id     TEXT,
    created_at      TEXT NOT NULL,
    started_at      TEXT,
    completed_at    TEXT
);

CREATE TABLE IF NOT EXISTS agents (
    agent_id        TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    type            TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'IDLE',
    capabilities    TEXT,
    current_task    TEXT,
    last_active     TEXT,
    error_log       TEXT
);

CREATE TABLE IF NOT EXISTS workflows (
    workflow_id     TEXT PRIMARY KEY,
    workflow_name   TEXT NOT NULL,
    goal            TEXT NOT NULL,
    task_ids        TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'PENDING',
    created_at      TEXT NOT NULL,
    completed_at    TEXT
);
"""

DEFAULT_AGENTS = [
    ("agent-claude", "Claude Manager", "claude"),
    ("agent-antigravity", "Antigravity Agent", "antigravity"),
    ("agent-muse", "Muse Agent", "muse"),
    ("agent-python", "Python Agent", "python"),
    ("agent-qa", "QA Agent", "qa"),
    ("agent-publisher", "Publisher Agent", "publisher"),
]


def get_connection() -> sqlite3.Connection:
    Path(SQLITE_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        for agent_id, name, agent_type in DEFAULT_AGENTS:
            conn.execute(
                """
                INSERT OR IGNORE INTO agents (agent_id, name, type, status, capabilities)
                VALUES (?, ?, ?, 'IDLE', '[]')
                """,
                (agent_id, name, agent_type),
            )
        conn.commit()
    finally:
        conn.close()

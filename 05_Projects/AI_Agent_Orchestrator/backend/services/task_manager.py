"""Task Manager — Requirement.md FR-003."""

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Optional

from db import get_connection
from models import Task, TaskCreate, TaskStatus


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _row_to_task(row: sqlite3.Row) -> Task:
    return Task(
        task_id=row["task_id"],
        task_name=row["task_name"],
        description=row["description"],
        assigned_agent=row["assigned_agent"],
        priority=row["priority"],
        status=row["status"],
        payload=json.loads(row["payload"]) if row["payload"] else {},
        result=json.loads(row["result"]) if row["result"] else None,
        error_message=row["error_message"],
        output_path=row["output_path"],
        workflow_id=row["workflow_id"],
        created_at=row["created_at"],
        started_at=row["started_at"],
        completed_at=row["completed_at"],
    )


def create_task(data: TaskCreate) -> Task:
    task_id = f"task-{uuid.uuid4().hex[:12]}"
    created_at = _now()
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO tasks
                (task_id, task_name, description, assigned_agent, priority,
                 status, payload, workflow_id, created_at)
            VALUES (?, ?, ?, ?, ?, 'QUEUED', ?, ?, ?)
            """,
            (
                task_id,
                data.task_name,
                data.description,
                data.assigned_agent.value,
                data.priority.value,
                json.dumps(data.payload),
                data.workflow_id,
                created_at,
            ),
        )
        conn.commit()
    finally:
        conn.close()
    return get_task(task_id)  # type: ignore[return-value]


def get_task(task_id: str) -> Optional[Task]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
    finally:
        conn.close()
    return _row_to_task(row) if row else None


def list_tasks(
    status: Optional[str] = None, assigned_agent: Optional[str] = None, limit: int = 50
) -> list[Task]:
    query = "SELECT * FROM tasks WHERE 1=1"
    params: list[str] = []
    if status:
        query += " AND status = ?"
        params.append(status)
    if assigned_agent:
        query += " AND assigned_agent = ?"
        params.append(assigned_agent)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(str(limit))

    conn = get_connection()
    try:
        rows = conn.execute(query, params).fetchall()
    finally:
        conn.close()
    return [_row_to_task(r) for r in rows]


def update_task_status(
    task_id: str,
    status: TaskStatus,
    result: Optional[dict] = None,
    error_message: Optional[str] = None,
    output_path: Optional[str] = None,
) -> Optional[Task]:
    conn = get_connection()
    try:
        fields = ["status = ?"]
        params: list = [status.value]

        if status == TaskStatus.RUNNING:
            fields.append("started_at = ?")
            params.append(_now())
        if status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED):
            fields.append("completed_at = ?")
            params.append(_now())
        if result is not None:
            fields.append("result = ?")
            params.append(json.dumps(result))
        if error_message is not None:
            fields.append("error_message = ?")
            params.append(error_message)
        if output_path is not None:
            fields.append("output_path = ?")
            params.append(output_path)

        params.append(task_id)
        conn.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE task_id = ?", params)
        conn.commit()
    finally:
        conn.close()
    return get_task(task_id)


def cancel_task(task_id: str) -> Optional[Task]:
    task = get_task(task_id)
    if task is None:
        return None
    if task.status not in (TaskStatus.PENDING.value, TaskStatus.QUEUED.value, TaskStatus.RUNNING.value):
        return task
    return update_task_status(task_id, TaskStatus.CANCELLED)

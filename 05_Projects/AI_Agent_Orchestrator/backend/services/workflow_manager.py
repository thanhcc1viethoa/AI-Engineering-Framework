"""Workflow Manager — Requirement.md FR-005.

Decomposing a goal into steps is Claude's job (FR-020 — the reasoning lives in
the managing agent, not duplicated here). This module only stores and runs the
task graph it is given; `steps` is therefore required.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from db import get_connection
from models import Workflow, WorkflowCreate
from services import task_manager


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_workflow(data: WorkflowCreate) -> Workflow:
    if not data.steps:
        raise ValueError(
            "execute_workflow requires at least one step; this Orchestrator does not "
            "invent its own task decomposition (see Requirement.md FR-020)."
        )

    workflow_id = f"wf-{uuid.uuid4().hex[:12]}"
    created_at = _now()

    task_ids = []
    for step in data.steps:
        step_with_workflow = step.model_copy(update={"workflow_id": workflow_id})
        task = task_manager.create_task(step_with_workflow)
        task_ids.append(task.task_id)

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO workflows (workflow_id, workflow_name, goal, task_ids, status, created_at)
            VALUES (?, ?, ?, ?, 'PENDING', ?)
            """,
            (workflow_id, data.workflow_name, data.goal, ",".join(task_ids), created_at),
        )
        conn.commit()
    finally:
        conn.close()

    return get_workflow(workflow_id)  # type: ignore[return-value]


def get_workflow(workflow_id: str) -> Optional[Workflow]:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM workflows WHERE workflow_id = ?", (workflow_id,)
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        return None
    task_ids = row["task_ids"].split(",") if row["task_ids"] else []
    return Workflow(
        workflow_id=row["workflow_id"],
        workflow_name=row["workflow_name"],
        goal=row["goal"],
        task_ids=task_ids,
        status=row["status"],
        created_at=row["created_at"],
        completed_at=row["completed_at"],
    )


def refresh_workflow_status(workflow_id: str) -> Optional[Workflow]:
    """Recompute a workflow's status from its tasks' current statuses."""
    workflow = get_workflow(workflow_id)
    if workflow is None:
        return None

    statuses = [task_manager.get_task(tid).status for tid in workflow.task_ids if task_manager.get_task(tid)]
    if not statuses:
        return workflow

    if any(s == "FAILED" for s in statuses):
        new_status = "FAILED"
    elif all(s == "COMPLETED" for s in statuses):
        new_status = "COMPLETED"
    elif any(s == "CANCELLED" for s in statuses) and all(s in ("COMPLETED", "CANCELLED") for s in statuses):
        new_status = "CANCELLED"
    else:
        new_status = "RUNNING"

    conn = get_connection()
    try:
        completed_at = _now() if new_status in ("COMPLETED", "FAILED", "CANCELLED") else None
        conn.execute(
            "UPDATE workflows SET status = ?, completed_at = COALESCE(?, completed_at) WHERE workflow_id = ?",
            (new_status, completed_at, workflow_id),
        )
        conn.commit()
    finally:
        conn.close()
    return get_workflow(workflow_id)

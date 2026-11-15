"""Task endpoints — Antigravity_Build_Guide.md section 6.3."""

from typing import Literal, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

import config
from auth import require_auth
from models import Task, TaskCreate, TaskStatus
from services import dispatcher, task_manager

router = APIRouter(prefix="/tasks", tags=["tasks"], dependencies=[Depends(require_auth)])


class ReviewDecision(BaseModel):
    decision: Literal["approve", "reject"]
    feedback: Optional[str] = None


@router.post("", response_model=Task)
async def submit_task(data: TaskCreate, background_tasks: BackgroundTasks) -> Task:
    task = task_manager.create_task(data)
    # BackgroundTasks (not asyncio.create_task) — a bare create_task can be
    # cancelled when the request's async context tears down under some ASGI
    # test/server setups; BackgroundTasks is the supported way to run work
    # after the response is sent.
    background_tasks.add_task(dispatcher.dispatch_task, task.task_id)
    return task


@router.get("", response_model=list[Task])
async def list_tasks(status: Optional[str] = None, assigned_agent: Optional[str] = None, limit: int = 50) -> list[Task]:
    return task_manager.list_tasks(status=status, assigned_agent=assigned_agent, limit=limit)


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str) -> Task:
    task = task_manager.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", response_model=Task)
async def cancel_task(task_id: str) -> Task:
    task = task_manager.cancel_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/{task_id}/review", response_model=Task)
async def review_task(task_id: str, data: ReviewDecision, background_tasks: BackgroundTasks) -> Task:
    """Antigravity Agent subsystem rule: a coding task sits in REVIEW until
    Claude approves it (-> COMPLETED) or rejects it with feedback, which
    re-dispatches the same task_id/project_dir with that feedback appended,
    bounded by MAX_FIX_RETRIES. Muse4AI's own REVIEW (needs_review) has no
    programmatic resolution — the user must check it inside the Muse4AI app."""
    task = task_manager.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != TaskStatus.REVIEW.value:
        raise HTTPException(status_code=409, detail=f"Task is {task.status}, not REVIEW")
    if task.assigned_agent != "antigravity":
        raise HTTPException(
            status_code=400,
            detail=f"Only antigravity tasks can be reviewed via this endpoint (this task is '{task.assigned_agent}')",
        )

    if data.decision == "approve":
        return task_manager.update_task_status(task_id, TaskStatus.COMPLETED)

    attempts = int(task.payload.get("_review_attempts", 0)) + 1
    if attempts > config.MAX_FIX_RETRIES:
        return task_manager.update_task_status(
            task_id,
            TaskStatus.FAILED,
            error_message=f"Rejected in review {attempts} times, exceeding MAX_FIX_RETRIES ({config.MAX_FIX_RETRIES})",
        )

    original_instructions = task.payload.get("instructions") or task.description or task.task_name
    new_payload = dict(task.payload)
    new_payload["_review_attempts"] = attempts
    new_payload["instructions"] = (
        f"{original_instructions}\n\n--- Review feedback (attempt {attempts}) ---\n"
        f"{data.feedback or '(no specific feedback given)'}"
    )
    task_manager.update_task_payload(task_id, new_payload)
    updated = task_manager.update_task_status(task_id, TaskStatus.ASSIGNED)
    background_tasks.add_task(dispatcher.dispatch_task, task_id)
    return updated

"""Task endpoints — Antigravity_Build_Guide.md section 6.3."""

from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from auth import require_auth
from models import Task, TaskCreate
from services import dispatcher, task_manager

router = APIRouter(prefix="/tasks", tags=["tasks"], dependencies=[Depends(require_auth)])


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

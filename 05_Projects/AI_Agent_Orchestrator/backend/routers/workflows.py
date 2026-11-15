from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from auth import require_auth
from models import Workflow, WorkflowCreate
from services import dispatcher, workflow_manager

router = APIRouter(prefix="/workflows", tags=["workflows"], dependencies=[Depends(require_auth)])


@router.post("", response_model=Workflow)
async def execute_workflow(data: WorkflowCreate, background_tasks: BackgroundTasks) -> Workflow:
    try:
        workflow = workflow_manager.create_workflow(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    # All steps are dispatched together (bounded by MAX_CONCURRENT_TASKS) —
    # this covers FR-005's "parallel execution for independent tasks" case.
    # TaskCreate has no dependency field yet, so strictly sequential,
    # dependent steps are not modeled here; that needs a schema addition in
    # Architecture.md before it can be implemented correctly.
    for task_id in workflow.task_ids:
        background_tasks.add_task(dispatcher.dispatch_task, task_id)
    return workflow


@router.get("/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: str) -> Workflow:
    workflow = workflow_manager.refresh_workflow_status(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

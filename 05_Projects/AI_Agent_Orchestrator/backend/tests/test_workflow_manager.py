import pytest

from models import AssignedAgent, TaskCreate, WorkflowCreate
from services import workflow_manager


def test_create_workflow_requires_steps():
    with pytest.raises(ValueError):
        workflow_manager.create_workflow(WorkflowCreate(workflow_name="w", goal="g", steps=None))


def test_create_workflow_with_steps():
    workflow = workflow_manager.create_workflow(
        WorkflowCreate(
            workflow_name="w1",
            goal="demo goal",
            steps=[TaskCreate(task_name="s1", assigned_agent=AssignedAgent.PYTHON, payload={})],
        )
    )
    assert len(workflow.task_ids) == 1
    assert workflow.status == "PENDING"

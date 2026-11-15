from models import AssignedAgent, TaskCreate
from services import task_manager


def test_create_and_get_task():
    task = task_manager.create_task(
        TaskCreate(task_name="t1", assigned_agent=AssignedAgent.PYTHON, payload={})
    )
    assert task.status == "ASSIGNED"
    fetched = task_manager.get_task(task.task_id)
    assert fetched is not None
    assert fetched.task_id == task.task_id


def test_list_tasks_filters_by_agent():
    task_manager.create_task(TaskCreate(task_name="a", assigned_agent=AssignedAgent.PYTHON, payload={}))
    task_manager.create_task(TaskCreate(task_name="b", assigned_agent=AssignedAgent.MUSE, payload={}))

    python_tasks = task_manager.list_tasks(assigned_agent="python")
    assert len(python_tasks) == 1
    assert python_tasks[0].assigned_agent == "python"


def test_cancel_task():
    task = task_manager.create_task(TaskCreate(task_name="c", assigned_agent=AssignedAgent.PYTHON, payload={}))
    cancelled = task_manager.cancel_task(task.task_id)
    assert cancelled is not None
    assert cancelled.status == "CANCELLED"


def test_cancel_completed_task_is_noop():
    task = task_manager.create_task(TaskCreate(task_name="d", assigned_agent=AssignedAgent.PYTHON, payload={}))
    task_manager.update_task_status(task.task_id, task_manager.TaskStatus.COMPLETED)
    result = task_manager.cancel_task(task.task_id)
    assert result.status == "COMPLETED"

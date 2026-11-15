import asyncio
from unittest.mock import MagicMock

from models import AssignedAgent, TaskCreate
from services import dispatcher, task_manager


async def test_python_task_completes():
    task = task_manager.create_task(
        TaskCreate(
            task_name="list",
            assigned_agent=AssignedAgent.PYTHON,
            payload={"action": "list_directory", "path": "/tmp"},
        )
    )
    await asyncio.wait_for(dispatcher.dispatch_task(task.task_id), timeout=10)

    result = task_manager.get_task(task.task_id)
    assert result.status == "COMPLETED"
    assert "entries" in result.result


async def test_antigravity_task_fails_cleanly_without_hanging():
    """Regression test: a retry used to recurse while still holding the
    concurrency semaphore, deadlocking forever since asyncio.Semaphore is not
    reentrant. The surrounding asyncio.wait_for would fail this test if the
    deadlock reappears."""
    task = task_manager.create_task(
        TaskCreate(
            task_name="code",
            assigned_agent=AssignedAgent.ANTIGRAVITY,
            payload={"instructions": "noop"},
        )
    )
    await asyncio.wait_for(dispatcher.dispatch_task(task.task_id), timeout=10)

    result = task_manager.get_task(task.task_id)
    assert result.status == "FAILED"
    assert "AS-001" in result.error_message


async def test_antigravity_success_goes_to_review_not_completed(monkeypatch):
    """Antigravity Agent subsystem rule: a coding task is never
    auto-COMPLETED — it lands in REVIEW with files/test_result for Claude to
    inspect via review_task."""
    monkeypatch.setattr(dispatcher, "check_cli_available", MagicMock(return_value=True))
    monkeypatch.setattr(
        dispatcher,
        "run_coding_task",
        MagicMock(
            return_value={
                "stdout": "done",
                "duration_seconds": 1.2,
                "output_path": "/tmp/fake-project",
                "files": ["hello.py"],
                "test_command": "pytest",
                "test_result": {"exit_code": 0, "passed": True, "output": "1 passed"},
            }
        ),
    )

    task = task_manager.create_task(
        TaskCreate(
            task_name="code",
            assigned_agent=AssignedAgent.ANTIGRAVITY,
            payload={"instructions": "write hello.py", "test_command": "pytest"},
        )
    )
    await asyncio.wait_for(dispatcher.dispatch_task(task.task_id), timeout=10)

    result = task_manager.get_task(task.task_id)
    assert result.status == "REVIEW"
    assert result.result["files"] == ["hello.py"]
    assert result.result["test_result"]["passed"] is True


async def test_muse_task_fails_cleanly_when_unconfigured():
    task = task_manager.create_task(
        TaskCreate(task_name="video", assigned_agent=AssignedAgent.MUSE, payload={"prompt": "a cat"})
    )
    await asyncio.wait_for(dispatcher.dispatch_task(task.task_id), timeout=10)

    result = task_manager.get_task(task.task_id)
    assert result.status == "FAILED"
    assert "AS-002" in result.error_message


async def test_qa_agent_passes_a_genuinely_completed_task():
    target = task_manager.create_task(
        TaskCreate(
            task_name="target",
            assigned_agent=AssignedAgent.PYTHON,
            payload={"action": "list_directory", "path": "/tmp"},
        )
    )
    await dispatcher.dispatch_task(target.task_id)

    qa_task = task_manager.create_task(
        TaskCreate(
            task_name="qa",
            assigned_agent=AssignedAgent.QA,
            payload={"target_task_id": target.task_id},
        )
    )
    await dispatcher.dispatch_task(qa_task.task_id)

    result = task_manager.get_task(qa_task.task_id)
    assert result.status == "COMPLETED"
    assert result.result["passed"] is True


async def test_qa_agent_fails_a_task_that_never_ran():
    qa_task = task_manager.create_task(
        TaskCreate(
            task_name="qa-missing",
            assigned_agent=AssignedAgent.QA,
            payload={"target_task_id": "task-does-not-exist"},
        )
    )
    await dispatcher.dispatch_task(qa_task.task_id)

    result = task_manager.get_task(qa_task.task_id)
    assert result.status == "FAILED"
    assert "not found" in result.error_message

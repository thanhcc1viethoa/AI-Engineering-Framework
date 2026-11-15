"""Dispatcher-level tests for the Muse4AI flow, against the real documented
status vocabulary (queued/running/succeeded/failed/needs_review/cancelled —
see agents/muse/adapter.py). These monkeypatch the adapter functions that
`dispatcher` imported by name, so no real Muse4AI instance or network call is
involved; agents/muse/test_adapter.py separately verifies the HTTP-level
request/response handling against mocked httpx."""

from unittest.mock import MagicMock

from models import AssignedAgent, TaskCreate
from services import dispatcher, task_manager


def _submit_muse_task(prompt="a cat on a sofa"):
    return task_manager.create_task(
        TaskCreate(task_name="video", assigned_agent=AssignedAgent.MUSE, payload={"prompt": prompt})
    )


async def test_muse_task_completes_and_downloads_output(monkeypatch):
    job_queued = {"id": "job_1", "status": "queued", "outputs": []}
    job_succeeded = {
        "id": "job_1",
        "status": "succeeded",
        "outputs": [{"asset_id": "asset_1", "mime": "video/mp4", "download_url": "https://signed/x"}],
    }

    monkeypatch.setattr(dispatcher, "submit_video", MagicMock(return_value=job_queued))
    monkeypatch.setattr(dispatcher, "get_job", MagicMock(return_value=job_succeeded))
    monkeypatch.setattr(dispatcher, "download_output", MagicMock(return_value="/fake/output/asset_1.mp4"))

    task = _submit_muse_task()
    await dispatcher.dispatch_task(task.task_id)

    result = task_manager.get_task(task.task_id)
    assert result.status == "COMPLETED"
    assert result.output_path == "/fake/output/asset_1.mp4"
    assert result.result["job_id"] == "job_1"


async def test_muse_task_needs_review_is_waiting_not_failed(monkeypatch):
    job = {"id": "job_2", "status": "needs_review", "outputs": []}
    monkeypatch.setattr(dispatcher, "submit_video", MagicMock(return_value=job))
    monkeypatch.setattr(dispatcher, "get_job", MagicMock(return_value=job))

    task = _submit_muse_task()
    await dispatcher.dispatch_task(task.task_id)

    result = task_manager.get_task(task.task_id)
    assert result.status == "WAITING"
    assert result.result["needs_review"] is True


async def test_muse_task_failed_status_records_error_message(monkeypatch):
    job_queued = {"id": "job_3", "status": "queued", "outputs": []}
    job_failed = {"id": "job_3", "status": "failed", "outputs": [], "error": {"code": "PROVIDER_ERROR", "message": "Muse reported a technical failure"}}

    monkeypatch.setattr(dispatcher, "submit_video", MagicMock(return_value=job_queued))
    monkeypatch.setattr(dispatcher, "get_job", MagicMock(return_value=job_failed))

    task = _submit_muse_task()
    await dispatcher.dispatch_task(task.task_id)

    result = task_manager.get_task(task.task_id)
    assert result.status == "FAILED"
    assert "technical failure" in result.error_message


async def test_duplicate_muse_prompt_is_blocked_while_one_is_running(monkeypatch):
    monkeypatch.setattr(dispatcher, "submit_video", MagicMock(return_value={"id": "job_4", "status": "running", "outputs": []}))
    monkeypatch.setattr(dispatcher, "get_job", MagicMock(return_value={"id": "job_4", "status": "running", "outputs": []}))

    first = _submit_muse_task(prompt="same prompt")
    task_manager.update_task_status(first.task_id, task_manager.TaskStatus.RUNNING)

    second = _submit_muse_task(prompt="same prompt")
    await dispatcher.dispatch_task(second.task_id)

    result = task_manager.get_task(second.task_id)
    assert result.status == "FAILED"
    assert "Duplicate video request blocked" in result.error_message

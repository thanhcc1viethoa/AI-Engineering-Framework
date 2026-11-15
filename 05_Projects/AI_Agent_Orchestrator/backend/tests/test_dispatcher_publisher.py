"""Dispatcher-level tests for the Publisher Agent (youtube/tiktok/instagram
routed by payload.platform). Monkeypatches the adapter functions dispatcher
imported by name — agents/publisher/test_*.py separately verify the
HTTP-level request/response handling against mocked httpx."""

from unittest.mock import MagicMock

from models import AssignedAgent, TaskCreate
from services import dispatcher, task_manager


def _submit_publisher_task(payload):
    return task_manager.create_task(
        TaskCreate(task_name="publish", assigned_agent=AssignedAgent.PUBLISHER, payload=payload)
    )


async def test_youtube_publish_completes(monkeypatch):
    monkeypatch.setattr(
        dispatcher, "youtube_upload_video", MagicMock(return_value={"video_id": "v1", "url": "https://youtu.be/v1"})
    )

    task = _submit_publisher_task({"platform": "youtube", "video_path": "/tmp/x.mp4", "caption": "hi"})
    await dispatcher.dispatch_task(task.task_id)

    result = task_manager.get_task(task.task_id)
    assert result.status == "COMPLETED"
    assert result.result["video_id"] == "v1"


async def test_tiktok_publish_completes(monkeypatch):
    monkeypatch.setattr(dispatcher, "time", MagicMock(sleep=lambda seconds: None))
    monkeypatch.setattr(dispatcher.config, "TIKTOK_ACCESS_TOKEN", "tok1")
    monkeypatch.setattr(dispatcher, "tiktok_post_video", MagicMock(return_value="pub1"))
    monkeypatch.setattr(dispatcher, "tiktok_get_publish_status", MagicMock(return_value={"status": "PUBLISH_COMPLETE"}))

    task = _submit_publisher_task({"platform": "tiktok", "video_path": "/tmp/x.mp4", "caption": "hi"})
    await dispatcher.dispatch_task(task.task_id)

    result = task_manager.get_task(task.task_id)
    assert result.status == "COMPLETED"
    assert result.result["publish_id"] == "pub1"


async def test_tiktok_publish_fails_on_failed_status(monkeypatch):
    monkeypatch.setattr(dispatcher, "time", MagicMock(sleep=lambda seconds: None))
    monkeypatch.setattr(dispatcher.config, "TIKTOK_ACCESS_TOKEN", "tok1")
    monkeypatch.setattr(dispatcher, "tiktok_post_video", MagicMock(return_value="pub1"))
    monkeypatch.setattr(
        dispatcher, "tiktok_get_publish_status", MagicMock(return_value={"status": "FAILED", "fail_reason": "bad video"})
    )

    task = _submit_publisher_task({"platform": "tiktok", "video_path": "/tmp/x.mp4", "caption": "hi"})
    await dispatcher.dispatch_task(task.task_id)

    result = task_manager.get_task(task.task_id)
    assert result.status == "FAILED"
    assert "bad video" in result.error_message


async def test_tiktok_requires_configured_token():
    task = _submit_publisher_task({"platform": "tiktok", "video_path": "/tmp/x.mp4", "caption": "hi"})
    await dispatcher.dispatch_task(task.task_id)

    result = task_manager.get_task(task.task_id)
    assert result.status == "FAILED"
    assert "not configured" in result.error_message


async def test_instagram_publish_completes(monkeypatch):
    monkeypatch.setattr(dispatcher, "time", MagicMock(sleep=lambda seconds: None))
    monkeypatch.setattr(dispatcher.config, "INSTAGRAM_ACCESS_TOKEN", "tok1")
    monkeypatch.setattr(dispatcher.config, "INSTAGRAM_IG_USER_ID", "ig1")
    monkeypatch.setattr(dispatcher, "instagram_create_reel_container", MagicMock(return_value="creation1"))
    monkeypatch.setattr(dispatcher, "instagram_get_container_status", MagicMock(return_value="FINISHED"))
    monkeypatch.setattr(dispatcher, "instagram_publish_container", MagicMock(return_value="media1"))

    task = _submit_publisher_task({"platform": "instagram", "video_url": "https://example.com/v.mp4", "caption": "hi"})
    await dispatcher.dispatch_task(task.task_id)

    result = task_manager.get_task(task.task_id)
    assert result.status == "COMPLETED"
    assert result.result["media_id"] == "media1"


async def test_instagram_requires_video_url_not_a_local_path(monkeypatch):
    monkeypatch.setattr(dispatcher.config, "INSTAGRAM_ACCESS_TOKEN", "tok1")
    monkeypatch.setattr(dispatcher.config, "INSTAGRAM_IG_USER_ID", "ig1")

    task = _submit_publisher_task({"platform": "instagram", "caption": "hi"})
    await dispatcher.dispatch_task(task.task_id)

    result = task_manager.get_task(task.task_id)
    assert result.status == "FAILED"
    assert "video_url" in result.error_message


async def test_unknown_platform_fails_cleanly():
    task = _submit_publisher_task({"platform": "snapchat", "caption": "hi"})
    await dispatcher.dispatch_task(task.task_id)

    result = task_manager.get_task(task.task_id)
    assert result.status == "FAILED"
    assert "Unknown or missing payload.platform" in result.error_message

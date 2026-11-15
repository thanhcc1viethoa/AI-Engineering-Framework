"""Tests for POST /tasks/{id}/review — the Antigravity Agent subsystem's
REVIEW gate (approve -> COMPLETED, reject -> re-dispatched with feedback,
bounded by MAX_FIX_RETRIES)."""

import time
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

import config
from main import app
from models import AssignedAgent, TaskCreate
from services import dispatcher, task_manager

client = TestClient(app)


def _auth_headers():
    response = client.post("/auth/login", json={"password": "test-password"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _submit_and_wait_for_review(monkeypatch, instructions="write hello.py"):
    monkeypatch.setattr(dispatcher, "check_cli_available", MagicMock(return_value=True))
    monkeypatch.setattr(
        dispatcher,
        "run_coding_task",
        MagicMock(
            return_value={
                "stdout": "done",
                "duration_seconds": 1.0,
                "output_path": "/tmp/fake-project",
                "files": ["hello.py"],
                "test_command": None,
                "test_result": None,
            }
        ),
    )
    response = client.post(
        "/tasks",
        headers=_auth_headers(),
        json={"task_name": "code", "assigned_agent": "antigravity", "payload": {"instructions": instructions}},
    )
    task_id = response.json()["task_id"]

    deadline = time.time() + 5
    status = None
    while time.time() < deadline:
        status = client.get(f"/tasks/{task_id}", headers=_auth_headers()).json()["status"]
        if status != "RUNNING" and status != "ASSIGNED":
            break
        time.sleep(0.1)
    assert status == "REVIEW", f"expected REVIEW, got {status}"
    return task_id


def test_approve_marks_task_completed(monkeypatch):
    task_id = _submit_and_wait_for_review(monkeypatch)

    response = client.post(f"/tasks/{task_id}/review", headers=_auth_headers(), json={"decision": "approve"})
    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"


def test_reject_with_feedback_redispatches_with_appended_instructions(monkeypatch):
    task_id = _submit_and_wait_for_review(monkeypatch, instructions="write hello.py")

    response = client.post(
        f"/tasks/{task_id}/review",
        headers=_auth_headers(),
        json={"decision": "reject", "feedback": "add type hints"},
    )
    assert response.status_code == 200

    deadline = time.time() + 5
    status = None
    while time.time() < deadline:
        task = client.get(f"/tasks/{task_id}", headers=_auth_headers()).json()
        status = task["status"]
        if status != "RUNNING" and status != "ASSIGNED":
            break
        time.sleep(0.1)
    assert status == "REVIEW"
    assert "add type hints" in task["payload"]["instructions"]
    assert task["payload"]["_review_attempts"] == 1


def test_reject_fails_task_after_exceeding_max_fix_retries(monkeypatch):
    task_id = _submit_and_wait_for_review(monkeypatch)

    for _ in range(config.MAX_FIX_RETRIES):
        client.post(f"/tasks/{task_id}/review", headers=_auth_headers(), json={"decision": "reject", "feedback": "no"})
        deadline = time.time() + 5
        while time.time() < deadline:
            status = client.get(f"/tasks/{task_id}", headers=_auth_headers()).json()["status"]
            if status != "RUNNING" and status != "ASSIGNED":
                break
            time.sleep(0.1)

    final = client.post(f"/tasks/{task_id}/review", headers=_auth_headers(), json={"decision": "reject", "feedback": "no"})
    assert final.status_code == 200
    assert final.json()["status"] == "FAILED"


def test_review_rejects_non_review_task():
    task = task_manager.create_task(
        TaskCreate(task_name="t", assigned_agent=AssignedAgent.PYTHON, payload={"action": "list_directory", "path": "/tmp"})
    )
    response = client.post(f"/tasks/{task.task_id}/review", headers=_auth_headers(), json={"decision": "approve"})
    assert response.status_code == 409


def test_review_rejects_non_antigravity_task(monkeypatch):
    monkeypatch.setattr(dispatcher.config, "TIKTOK_ACCESS_TOKEN", "")
    task = task_manager.create_task(
        TaskCreate(task_name="t", assigned_agent=AssignedAgent.MUSE, payload={"prompt": "x"})
    )
    task_manager.update_task_status(task.task_id, task_manager.TaskStatus.REVIEW, result={"needs_review": True})

    response = client.post(f"/tasks/{task.task_id}/review", headers=_auth_headers(), json={"decision": "approve"})
    assert response.status_code == 400

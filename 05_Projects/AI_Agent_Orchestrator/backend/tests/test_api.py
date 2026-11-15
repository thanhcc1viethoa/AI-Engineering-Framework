import time

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture()
def auth_headers():
    """DASHBOARD_PASSWORD/DASHBOARD_JWT_SECRET come from the
    dashboard_auth_configured conftest fixture ('test-password' / 'test-secret')."""
    response = client.post("/auth/login", json={"password": "test-password"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_login_rejects_wrong_password():
    response = client.post("/auth/login", json={"password": "wrong"})
    assert response.status_code == 401


def test_protected_route_requires_auth():
    response = client.get("/agents")
    assert response.status_code == 401


def test_system_status_endpoint_is_unauthenticated():
    response = client.get("/system/status")
    assert response.status_code == 200
    assert "agents_total" in response.json()


def test_list_agents_endpoint_returns_seeded_agents(auth_headers):
    response = client.get("/agents", headers=auth_headers)
    assert response.status_code == 200
    types = {a["type"] for a in response.json()}
    assert {"claude", "antigravity", "muse", "python", "qa"} <= types


def test_submit_task_runs_to_completion_via_api(auth_headers):
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "task_name": "api test",
            "assigned_agent": "python",
            "payload": {"action": "list_directory", "path": "/tmp"},
        },
    )
    assert response.status_code == 200
    task_id = response.json()["task_id"]

    status = None
    deadline = time.time() + 5
    while time.time() < deadline:
        poll = client.get(f"/tasks/{task_id}", headers=auth_headers)
        status = poll.json()["status"]
        if status in ("COMPLETED", "FAILED"):
            break
        time.sleep(0.2)

    assert status == "COMPLETED"


def test_get_unknown_task_returns_404(auth_headers):
    response = client.get("/tasks/does-not-exist", headers=auth_headers)
    assert response.status_code == 404

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def _auth_headers():
    response = client.post("/auth/login", json={"password": "test-password"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_system_config_hides_secrets():
    response = client.get("/system/config", headers=_auth_headers())
    assert response.status_code == 200
    body = response.json()
    assert "muse4ai_api_key_set" in body
    assert "muse4ai_api_key" not in body
    assert "dashboard_password" not in body


def test_system_logs_returns_list_even_when_empty():
    response = client.get("/system/logs", headers=_auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json()["lines"], list)


def test_system_config_requires_auth():
    response = client.get("/system/config")
    assert response.status_code == 401

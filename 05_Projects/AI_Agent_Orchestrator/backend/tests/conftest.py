import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

import config
import db


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    """Every test gets its own fresh SQLite file so tests never share state."""
    monkeypatch.setattr(db, "SQLITE_PATH", str(tmp_path / "test.db"))
    db.init_db()
    yield


@pytest.fixture(autouse=True)
def dashboard_auth_configured(monkeypatch):
    """Give the test suite a known dashboard password/secret, since FR-025
    protected routes return 503 (not configured) without them."""
    monkeypatch.setattr(config, "DASHBOARD_PASSWORD", "test-password")
    monkeypatch.setattr(config, "DASHBOARD_JWT_SECRET", "test-secret")
    yield


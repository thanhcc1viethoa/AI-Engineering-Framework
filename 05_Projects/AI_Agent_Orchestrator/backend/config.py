"""Central configuration loaded from environment variables.

Defaults here match config/.env.example. No secret has a hardcoded value — see
Requirement.md FR-026.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / "config" / ".env")

HOST = os.getenv("ORCHESTRATOR_HOST", "127.0.0.1")
PORT = int(os.getenv("ORCHESTRATOR_PORT", "8000"))
MCP_PORT = int(os.getenv("MCP_PORT", "8765"))

SQLITE_PATH = str(_PROJECT_ROOT / "database" / os.getenv("SQLITE_FILENAME", "orchestrator.db"))

# Muse4AI (https://muse4ai.andrewbabo.com) runs locally on the same Windows
# PC, alongside this Orchestrator — hence the 127.0.0.1 default.
MUSE4AI_API_KEY = os.getenv("MUSE4AI_API_KEY", "")
MUSE4AI_BASE_URL = os.getenv("MUSE4AI_BASE_URL", "http://127.0.0.1:47821/v1")

ANTIGRAVITY_CLI_PATH = os.getenv("ANTIGRAVITY_CLI_PATH", "agy")

DASHBOARD_JWT_SECRET = os.getenv("DASHBOARD_JWT_SECRET", "")
DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD", "")
DASHBOARD_TOKEN_TTL_SECONDS = int(os.getenv("DASHBOARD_TOKEN_TTL_SECONDS", "43200"))  # 12h

MAX_CONCURRENT_TASKS = int(os.getenv("MAX_CONCURRENT_TASKS", "3"))
MAX_TASK_TIMEOUT_SECONDS = int(os.getenv("MAX_TASK_TIMEOUT_SECONDS", "1800"))
MAX_FIX_RETRIES = int(os.getenv("MAX_FIX_RETRIES", "3"))

LOG_DIR = _PROJECT_ROOT / "logs"
OUTPUT_DIR = _PROJECT_ROOT / "output"
PROJECTS_DIR = _PROJECT_ROOT / "projects"

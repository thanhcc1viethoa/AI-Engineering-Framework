"""System status + WebSocket push — Requirement.md FR-019."""

import asyncio
from collections import deque

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

import config
from auth import require_auth
from models import SystemStatus
from services import report_generator

router = APIRouter(tags=["system"])

WS_PUSH_INTERVAL_SECONDS = 2


@router.get("/system/status", response_model=SystemStatus)
async def get_system_status() -> SystemStatus:
    return SystemStatus(**report_generator.get_system_status())


@router.get("/system/config", dependencies=[Depends(require_auth)])
async def get_system_config() -> dict:
    """Requirement.md FR-018 — read-only view of non-secret configuration.

    Never returns DASHBOARD_PASSWORD, DASHBOARD_JWT_SECRET, or MUSE4AI_API_KEY
    (FR-026). Values come from config/.env and only take effect on restart —
    this endpoint does not write them (see scripts/README or Settings page).
    """
    return {
        "orchestrator_host": config.HOST,
        "orchestrator_port": config.PORT,
        "mcp_port": config.MCP_PORT,
        "antigravity_cli_path": config.ANTIGRAVITY_CLI_PATH,
        "muse4ai_base_url": config.MUSE4AI_BASE_URL,
        "muse4ai_api_key_set": bool(config.MUSE4AI_API_KEY),
        "max_concurrent_tasks": config.MAX_CONCURRENT_TASKS,
        "max_task_timeout_seconds": config.MAX_TASK_TIMEOUT_SECONDS,
        "max_fix_retries": config.MAX_FIX_RETRIES,
        "projects_dir": str(config.PROJECTS_DIR),
        "output_dir": str(config.OUTPUT_DIR),
    }


@router.get("/system/logs", dependencies=[Depends(require_auth)])
async def get_system_logs(lines: int = 200) -> dict:
    """Requirement.md FR-017 — tail the Orchestrator log for the dashboard."""
    log_path = config.LOG_DIR / "orchestrator.log"
    if not log_path.exists():
        return {"lines": []}
    lines = max(1, min(lines, 2000))
    with open(log_path, encoding="utf-8", errors="replace") as f:
        tail = deque(f, maxlen=lines)
    return {"lines": [line.rstrip("\n") for line in tail]}


@router.websocket("/ws")
async def system_status_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(report_generator.get_system_status())
            await asyncio.sleep(WS_PUSH_INTERVAL_SECONDS)
    except WebSocketDisconnect:
        return

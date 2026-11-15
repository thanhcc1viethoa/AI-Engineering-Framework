"""MCP Server — Requirement.md FR-006/FR-011.

Exposes exactly the 14 tools defined in Antigravity_Build_Guide.md section 7
(the original 11, publish_video/get_publish_status for the Publisher Agent,
and review_task for the Antigravity Agent subsystem's REVIEW gate) to Claude
Desktop. Every tool is a thin, honest wrapper over the Orchestrator REST API
(backend/) — it calls a real endpoint and returns its real response, never a
fabricated result.

Run with: python main.py   (stdio transport, matches the claude_desktop_config.json
entry documented in Antigravity_Build_Guide.md section 10.)
"""

import os
from pathlib import Path
from typing import Literal, Optional

import httpx
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / "config" / ".env")

_HOST = os.getenv("ORCHESTRATOR_HOST", "127.0.0.1")
_PORT = os.getenv("ORCHESTRATOR_PORT", "8000")
ORCHESTRATOR_BASE_URL = f"http://{_HOST}:{_PORT}"

mcp = MCPServer(
    name="ai-agent-orchestrator",
    version="0.1.0",
    instructions=(
        "Submit and track tasks run by the Antigravity coding agent, the Muse4AI video "
        "agent, a Python automation agent, and a QA agent, through the AI Orchestrator "
        "backend. Never report a task as finished without checking its real status first."
    ),
)

_DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD", "")
_client = httpx.Client(base_url=ORCHESTRATOR_BASE_URL, timeout=30)
_token: Optional[str] = None


def _login() -> Optional[str]:
    if not _DASHBOARD_PASSWORD:
        return None
    response = _client.post("/auth/login", json={"password": _DASHBOARD_PASSWORD})
    response.raise_for_status()
    return response.json()["access_token"]


def _call(method: str, path: str, **kwargs) -> dict:
    global _token
    if "/auth/" not in path and "/system/status" not in path:
        if _token is None:
            try:
                _token = _login()
            except httpx.HTTPError as exc:
                return {"error": f"Could not authenticate with the Orchestrator: {exc}"}
        kwargs.setdefault("headers", {})
        if _token:
            kwargs["headers"]["Authorization"] = f"Bearer {_token}"

    try:
        response = _client.request(method, path, **kwargs)
        if response.status_code == 401:
            # Token expired or orchestrator restarted — log in once more.
            _token = _login()
            if _token:
                kwargs["headers"]["Authorization"] = f"Bearer {_token}"
                response = _client.request(method, path, **kwargs)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        return {"error": f"Orchestrator returned {exc.response.status_code}: {exc.response.text[:500]}"}
    except httpx.RequestError as exc:
        return {
            "error": (
                f"Could not reach the Orchestrator at {ORCHESTRATOR_BASE_URL} ({exc}). "
                "Is backend/main.py running?"
            )
        }


@mcp.tool(description="Submit a new task for a specific agent (antigravity, muse, python, qa, or publisher) to execute.")
def submit_task(
    task_name: str,
    assigned_agent: Literal["antigravity", "muse", "python", "qa", "publisher"],
    description: Optional[str] = None,
    priority: Literal["Critical", "High", "Medium", "Low", "Optional"] = "Medium",
    payload: Optional[dict] = None,
) -> dict:
    return _call(
        "POST",
        "/tasks",
        json={
            "task_name": task_name,
            "description": description,
            "assigned_agent": assigned_agent,
            "priority": priority,
            "payload": payload or {},
        },
    )


@mcp.tool(description="Get a task's current lifecycle status (PENDING/ASSIGNED/RUNNING/REVIEW/COMPLETED/FAILED/CANCELLED) and timestamps.")
def get_task_status(task_id: str) -> dict:
    task = _call("GET", f"/tasks/{task_id}")
    if "error" in task:
        return task
    return {
        "task_id": task["task_id"],
        "status": task["status"],
        "started_at": task["started_at"],
        "completed_at": task["completed_at"],
    }


@mcp.tool(
    description=(
        "Get a task's full result, output path, and error message (if any). Only trust a "
        "COMPLETED status as truly done — a REVIEW status means the task finished running but "
        "is awaiting a decision via review_task (Antigravity) or a manual check (Muse4AI)."
    )
)
def get_task_result(task_id: str) -> dict:
    task = _call("GET", f"/tasks/{task_id}")
    if "error" in task:
        return task
    return {
        "task_id": task["task_id"],
        "status": task["status"],
        "result": task["result"],
        "error_message": task["error_message"],
        "output_path": task["output_path"],
    }


@mcp.tool(description="List tasks, optionally filtered by status and/or assigned agent.")
def list_tasks(
    status: Optional[
        Literal["PENDING", "ASSIGNED", "RUNNING", "REVIEW", "COMPLETED", "FAILED", "CANCELLED"]
    ] = None,
    assigned_agent: Optional[Literal["antigravity", "muse", "python", "qa", "publisher"]] = None,
    limit: int = 50,
) -> dict:
    params = {"limit": limit}
    if status:
        params["status"] = status
    if assigned_agent:
        params["assigned_agent"] = assigned_agent
    result = _call("GET", "/tasks", params=params)
    return {"tasks": result} if isinstance(result, list) else result


@mcp.tool(description="Cancel a task that is PENDING, ASSIGNED, or RUNNING. No-op if it already finished.")
def cancel_task(task_id: str) -> dict:
    return _call("DELETE", f"/tasks/{task_id}")


@mcp.tool(
    description=(
        "Review a completed Antigravity coding task (status REVIEW) — the Antigravity Agent "
        "subsystem never auto-completes a coding task; Claude must inspect the result "
        "(get_task_result: stdout, files changed, test_result if a test_command was given) and "
        "decide. 'approve' marks it COMPLETED. 'reject' with `feedback` re-dispatches the same "
        "task with that feedback appended to its instructions, up to MAX_FIX_RETRIES times "
        "before it is marked FAILED. Only valid for assigned_agent=antigravity; a Muse4AI "
        "REVIEW (needs_review) has no programmatic resolution — the user checks it in the "
        "Muse4AI app."
    )
)
def review_task(task_id: str, decision: Literal["approve", "reject"], feedback: Optional[str] = None) -> dict:
    payload = {"decision": decision}
    if feedback is not None:
        payload["feedback"] = feedback
    return _call("POST", f"/tasks/{task_id}/review", json=payload)


@mcp.tool(description="Get one agent's status, current task, capabilities, and last recorded error.")
def get_agent_status(agent_id: str) -> dict:
    return _call("GET", f"/agents/{agent_id}")


@mcp.tool(description="List every registered agent (Claude Manager, Antigravity, Muse, Python, QA) and its status.")
def list_agents() -> dict:
    result = _call("GET", "/agents")
    return {"agents": result} if isinstance(result, list) else result


@mcp.tool(
    description=(
        "Run a workflow: a set of pre-decomposed steps (each an agent + payload), dispatched "
        "together. The Orchestrator does not decompose the goal itself — decompose it into "
        "`steps` before calling this tool (see Requirement.md FR-020)."
    )
)
def execute_workflow(workflow_name: str, goal: str, steps: list[dict]) -> dict:
    return _call(
        "POST",
        "/workflows",
        json={"workflow_name": workflow_name, "goal": goal, "steps": steps},
    )


@mcp.tool(
    description=(
        "Submit a video-generation request to the Muse Agent (Muse4AI, a local app that "
        "automates the user's own Meta Muse session — see github.com/andrew-babo/muse4ai). "
        "Per Muse4AI's real API there is no duration/resolution/style parameter: Muse decides "
        "those. `repeat` (1-4) submits that many variations in one call; `account` picks a "
        "specific Muse account alias configured in the app, or 'auto' (default)."
    )
)
def create_video(prompt: str, repeat: int = 1, account: str = "auto") -> dict:
    return _call(
        "POST",
        "/tasks",
        json={
            "task_name": f"create_video: {prompt[:40]}",
            "assigned_agent": "muse",
            "payload": {"prompt": prompt, "repeat": repeat, "account": account},
        },
    )


@mcp.tool(
    description=(
        "Check a video-generation task's status (this is the same task_id create_video "
        "returned). A REVIEW status means Muse4AI flagged the job for manual review — do "
        "not resubmit; the user must check it inside the Muse4AI app."
    )
)
def get_video_status(task_id: str) -> dict:
    task = _call("GET", f"/tasks/{task_id}")
    if "error" in task:
        return task
    if task["assigned_agent"] != "muse":
        return {"error": f"Task {task_id} is not a video task (assigned_agent={task['assigned_agent']})"}
    result = task["result"] or {}
    return {
        "task_id": task["task_id"],
        "status": task["status"],
        "job_id": result.get("job_id"),
        "output_path": task["output_path"],
    }


@mcp.tool(description="Get overall system status: agent counts, task counts by outcome, videos created, uptime.")
def get_system_status() -> dict:
    return _call("GET", "/system/status")


@mcp.tool(
    description=(
        "Publish a video to YouTube, TikTok, or Instagram via the Publisher Agent, using each "
        "platform's real API (not a generic one — parameters differ by platform). YouTube and "
        "TikTok need a local `video_path` (e.g. an output_path from a completed create_video "
        "task); Instagram needs an already-public `video_url` — it cannot post a local file "
        "directly. An unaudited TikTok app is forced to SELF_ONLY (private) visibility "
        "regardless of `privacy_level`."
    )
)
def publish_video(
    platform: Literal["youtube", "tiktok", "instagram"],
    caption: str,
    video_path: Optional[str] = None,
    video_url: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    privacy_status: str = "private",
    privacy_level: str = "SELF_ONLY",
) -> dict:
    payload = {"platform": platform, "caption": caption}
    if video_path is not None:
        payload["video_path"] = video_path
    if video_url is not None:
        payload["video_url"] = video_url
    if title is not None:
        payload["title"] = title
    if description is not None:
        payload["description"] = description
    if platform == "youtube":
        payload["privacy_status"] = privacy_status
    if platform == "tiktok":
        payload["privacy_level"] = privacy_level

    return _call(
        "POST",
        "/tasks",
        json={
            "task_name": f"publish_video[{platform}]: {caption[:40]}",
            "assigned_agent": "publisher",
            "payload": payload,
        },
    )


@mcp.tool(description="Check a publish_video task's status (same task_id publish_video returned).")
def get_publish_status(task_id: str) -> dict:
    task = _call("GET", f"/tasks/{task_id}")
    if "error" in task:
        return task
    if task["assigned_agent"] != "publisher":
        return {"error": f"Task {task_id} is not a publish task (assigned_agent={task['assigned_agent']})"}
    return {
        "task_id": task["task_id"],
        "status": task["status"],
        "result": task["result"],
        "error_message": task["error_message"],
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")

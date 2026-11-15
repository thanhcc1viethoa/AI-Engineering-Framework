"""Dispatcher — wires a QUEUED task to the right agent adapter and runs it.

`agents/` lives as a sibling of `backend/` (Requirement.md FR-002), not as a
subpackage of it, so the project root is added to sys.path here to import it.
"""

import asyncio
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config  # noqa: E402
from logger import get_logger  # noqa: E402
from models import AgentStatus, TaskStatus  # noqa: E402
from services import agent_manager, task_manager  # noqa: E402

from agents.antigravity.adapter import AntigravityError, check_cli_available, run_coding_task  # noqa: E402
from agents.muse.adapter import Muse4AIError, download_output, get_job, submit_video  # noqa: E402
from agents.python.adapter import run_automation  # noqa: E402
from agents.qa.adapter import check_task_output  # noqa: E402

logger = get_logger("dispatcher")

_semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_TASKS)


def _run_sync(task) -> dict:
    if task.assigned_agent == "antigravity":
        if not check_cli_available(config.ANTIGRAVITY_CLI_PATH):
            raise AntigravityError(
                f"Antigravity CLI ('{config.ANTIGRAVITY_CLI_PATH}') not available in this "
                "environment — see Requirement.md AS-001."
            )
        project_dir = config.PROJECTS_DIR / task.task_id
        instructions = task.payload.get("instructions") or task.description or task.task_name
        return run_coding_task(
            config.ANTIGRAVITY_CLI_PATH, project_dir, instructions, config.MAX_TASK_TIMEOUT_SECONDS
        )

    if task.assigned_agent == "muse":
        # Real Muse4AI contract (Requirement.md AS-002, resolved — see
        # agents/muse/adapter.py docstring): POST /v1/jobs takes only kind,
        # prompt, repeat and account for a video — no duration/resolution.
        prompt = task.payload.get("prompt") or task.description or task.task_name
        duplicate = next(
            (
                t
                for t in task_manager.list_tasks(assigned_agent="muse", status="RUNNING")
                if t.task_id != task.task_id and (t.payload.get("prompt") or "") == prompt
            ),
            None,
        )
        if duplicate is not None:
            raise Muse4AIError(f"Duplicate video request blocked — already running as {duplicate.task_id}")

        repeat = task.payload.get("repeat", 1)
        account = task.payload.get("account", "auto")
        job = submit_video(config.MUSE4AI_BASE_URL, config.MUSE4AI_API_KEY, prompt, repeat=repeat, account=account)
        job_id = job["id"]

        # Muse4AI's own `wait` query param long-polls for a status change;
        # looping on it is the documented way to track a job to completion.
        while job["status"] in ("queued", "running"):
            job = get_job(config.MUSE4AI_BASE_URL, config.MUSE4AI_API_KEY, job_id, wait_seconds=20)

        if job["status"] == "needs_review":
            # Documented behavior: a person must check it in Muse4AI — never
            # resubmit. Signaled back to _attempt_once via this flag so it is
            # recorded as WAITING, not COMPLETED or FAILED.
            return {"needs_review": True, "job_id": job_id, "outputs": job.get("outputs", [])}

        if job["status"] in ("failed", "cancelled"):
            message = (job.get("error") or {}).get("message") or f"Muse4AI job ended with status={job['status']}"
            raise Muse4AIError(message)

        outputs = job.get("outputs", [])
        output_path = download_output(outputs[0], str(config.OUTPUT_DIR / "videos")) if outputs else None
        return {"job_id": job_id, "status": job["status"], "outputs": outputs, "output_path": output_path}

    if task.assigned_agent == "python":
        return run_automation(task.payload)

    if task.assigned_agent == "qa":
        target_task_id = task.payload.get("target_task_id")
        target = task_manager.get_task(target_task_id) if target_task_id else None
        verdict = check_task_output(target)
        if not verdict["passed"]:
            raise ValueError(verdict["reason"])
        return verdict

    raise ValueError(f"Unknown assigned_agent '{task.assigned_agent}'")


async def dispatch_task(task_id: str) -> None:
    """Run a QUEUED task to completion, retrying a failed Antigravity task up
    to MAX_FIX_RETRIES times. Each attempt acquires the concurrency semaphore
    independently — retrying from inside the held semaphore would deadlock,
    since asyncio.Semaphore is not reentrant."""
    retries_left = config.MAX_FIX_RETRIES
    while await _attempt_once(task_id, retries_left):
        retries_left -= 1


async def _attempt_once(task_id: str, retries_left: int) -> bool:
    """Run a single attempt. Returns True if the caller should retry."""
    async with _semaphore:
        task = task_manager.get_task(task_id)
        if task is None or task.status != TaskStatus.QUEUED.value:
            return False

        agent = agent_manager.get_agent_by_type(task.assigned_agent)
        task_manager.update_task_status(task_id, TaskStatus.RUNNING)
        if agent:
            agent_manager.set_agent_status(agent.agent_id, AgentStatus.BUSY, task_id)

        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(_run_sync, task), timeout=config.MAX_TASK_TIMEOUT_SECONDS
            )
            if result.get("needs_review"):
                # Muse4AI flagged the job for manual review — not success, not
                # failure, and never retried (see agents/muse/adapter.py).
                task_manager.update_task_status(task_id, TaskStatus.WAITING, result=result)
                logger.info("Task %s needs human review in Muse4AI", task_id)
                return False
            task_manager.update_task_status(
                task_id, TaskStatus.COMPLETED, result=result, output_path=result.get("output_path")
            )
            logger.info("Task %s completed", task_id)
            return False
        except Exception as exc:  # noqa: BLE001 - any agent failure must be caught, logged, and possibly retried
            logger.error("Task %s failed: %s", task_id, exc)
            if agent:
                agent_manager.log_agent_error(agent.agent_id, str(exc))

            if retries_left > 0 and task.assigned_agent == "antigravity":
                logger.info("Retrying task %s (%d retries left)", task_id, retries_left)
                task_manager.update_task_status(task_id, TaskStatus.QUEUED)
                return True

            task_manager.update_task_status(task_id, TaskStatus.FAILED, error_message=str(exc))
            return False
        finally:
            if agent:
                current = agent_manager.get_agent(agent.agent_id)
                if current and current.status == AgentStatus.BUSY.value:
                    agent_manager.set_agent_status(agent.agent_id, AgentStatus.IDLE, None)

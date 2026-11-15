"""Dispatcher — wires an ASSIGNED task to the right agent adapter and runs it.

`agents/` lives as a sibling of `backend/` (Requirement.md FR-002), not as a
subpackage of it, so the project root is added to sys.path here to import it.
"""

import asyncio
import sys
import time
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
from agents.publisher.youtube import YouTubeError  # noqa: E402
from agents.publisher.youtube import upload_video as youtube_upload_video  # noqa: E402
from agents.publisher.tiktok import TikTokError  # noqa: E402
from agents.publisher.tiktok import post_video as tiktok_post_video  # noqa: E402
from agents.publisher.tiktok import get_publish_status as tiktok_get_publish_status  # noqa: E402
from agents.publisher.instagram import InstagramError  # noqa: E402
from agents.publisher.instagram import create_reel_container as instagram_create_reel_container  # noqa: E402
from agents.publisher.instagram import get_container_status as instagram_get_container_status  # noqa: E402
from agents.publisher.instagram import publish_container as instagram_publish_container  # noqa: E402

_TIKTOK_POLL_SECONDS = 5
_INSTAGRAM_POLL_SECONDS = 5

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
        test_command = task.payload.get("test_command")
        result = run_coding_task(
            config.ANTIGRAVITY_CLI_PATH,
            project_dir,
            instructions,
            config.MAX_TASK_TIMEOUT_SECONDS,
            test_command=test_command,
        )
        # Antigravity Agent subsystem rule: a coding task is never
        # auto-COMPLETED — Claude must review it first (see review_task /
        # POST /tasks/{id}/review). Reuses the same needs_review signal
        # Muse4AI uses below, handled once in _attempt_once.
        return {"needs_review": True, **result}

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
            # recorded as REVIEW, not COMPLETED or FAILED.
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

    if task.assigned_agent == "publisher":
        return _run_publisher_task(task)

    raise ValueError(f"Unknown assigned_agent '{task.assigned_agent}'")


def _run_publisher_task(task) -> dict:
    """Routes by payload.platform instead of a separate assigned_agent value
    per platform — adding a 4th platform only needs a new adapter module and
    one more branch here, per agents/publisher/README.md."""
    platform = task.payload.get("platform")

    if platform == "youtube":
        video_path = task.payload.get("video_path")
        if not video_path:
            raise ValueError("payload.video_path is required for platform=youtube")
        result = youtube_upload_video(
            config.YOUTUBE_TOKEN_PATH,
            video_path,
            title=task.payload.get("title") or task.task_name,
            description=task.payload.get("description") or task.payload.get("caption", ""),
            privacy_status=task.payload.get("privacy_status", "private"),
        )
        return {"platform": "youtube", "output_path": video_path, **result}

    if platform == "tiktok":
        if not config.TIKTOK_ACCESS_TOKEN:
            raise TikTokError(
                "TikTok is not configured (TIKTOK_ACCESS_TOKEN) — see agents/publisher/README.md"
            )
        video_path = task.payload.get("video_path")
        if not video_path:
            raise ValueError("payload.video_path is required for platform=tiktok")

        publish_id = tiktok_post_video(
            config.TIKTOK_ACCESS_TOKEN,
            video_path,
            title=task.payload.get("title") or task.payload.get("caption") or task.task_name,
            privacy_level=task.payload.get("privacy_level", "SELF_ONLY"),
        )

        terminal_statuses = {"PUBLISH_COMPLETE", "FAILED", "SEND_TO_USER_INBOX"}
        status_data = {"status": "PROCESSING_UPLOAD"}
        while status_data.get("status") not in terminal_statuses:
            time.sleep(_TIKTOK_POLL_SECONDS)
            status_data = tiktok_get_publish_status(config.TIKTOK_ACCESS_TOKEN, publish_id)

        if status_data.get("status") == "FAILED":
            raise TikTokError(status_data.get("fail_reason") or "TikTok publish failed")

        return {"platform": "tiktok", "publish_id": publish_id, "status": status_data.get("status"), "output_path": video_path}

    if platform == "instagram":
        if not config.INSTAGRAM_ACCESS_TOKEN or not config.INSTAGRAM_IG_USER_ID:
            raise InstagramError(
                "Instagram is not configured (INSTAGRAM_ACCESS_TOKEN / INSTAGRAM_IG_USER_ID) — "
                "see agents/publisher/README.md"
            )
        video_url = task.payload.get("video_url")
        if not video_url:
            raise ValueError(
                "payload.video_url is required for platform=instagram and must already be a "
                "public URL — Instagram's API does not accept a local file (see "
                "agents/publisher/instagram.py)"
            )

        creation_id = instagram_create_reel_container(
            config.INSTAGRAM_ACCESS_TOKEN,
            config.INSTAGRAM_IG_USER_ID,
            video_url,
            caption=task.payload.get("caption", ""),
        )

        status_code = "IN_PROGRESS"
        while status_code == "IN_PROGRESS":
            time.sleep(_INSTAGRAM_POLL_SECONDS)
            status_code = instagram_get_container_status(config.INSTAGRAM_ACCESS_TOKEN, creation_id)

        if status_code != "FINISHED":
            raise InstagramError(f"Instagram container ended with status {status_code}, not FINISHED")

        media_id = instagram_publish_container(config.INSTAGRAM_ACCESS_TOKEN, config.INSTAGRAM_IG_USER_ID, creation_id)
        return {"platform": "instagram", "media_id": media_id}

    raise ValueError(f"Unknown or missing payload.platform for publisher task: {platform!r} (expected youtube|tiktok|instagram)")


async def dispatch_task(task_id: str) -> None:
    """Run an ASSIGNED task to completion, retrying a failed Antigravity task
    up to MAX_FIX_RETRIES times. Each attempt acquires the concurrency
    semaphore independently — retrying from inside the held semaphore would
    deadlock, since asyncio.Semaphore is not reentrant."""
    retries_left = config.MAX_FIX_RETRIES
    while await _attempt_once(task_id, retries_left):
        retries_left -= 1


async def _attempt_once(task_id: str, retries_left: int) -> bool:
    """Run a single attempt. Returns True if the caller should retry."""
    async with _semaphore:
        task = task_manager.get_task(task_id)
        if task is None or task.status != TaskStatus.ASSIGNED.value:
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
                # Muse4AI flagged a job for manual review, or (always) an
                # Antigravity coding task awaiting Claude's review — not
                # success, not failure, and never auto-retried.
                task_manager.update_task_status(task_id, TaskStatus.REVIEW, result=result)
                logger.info("Task %s is in REVIEW", task_id)
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
                task_manager.update_task_status(task_id, TaskStatus.ASSIGNED)
                return True

            task_manager.update_task_status(task_id, TaskStatus.FAILED, error_message=str(exc))
            return False
        finally:
            if agent:
                current = agent_manager.get_agent(agent.agent_id)
                if current and current.status == AgentStatus.BUSY.value:
                    agent_manager.set_agent_status(agent.agent_id, AgentStatus.IDLE, None)

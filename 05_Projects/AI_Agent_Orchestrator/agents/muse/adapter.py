"""Muse4AI adapter — Requirement.md FR-008 / AS-002.

Muse4AI (https://github.com/andrew-babo/muse4ai) is a real, documented,
*local* Windows app — not a cloud service. It runs on the user's own PC,
automates their own signed-in Meta Muse session, and exposes a REST + MCP
API on 127.0.0.1. This file was corrected after reading that repository's
actual OpenAPI contract (`desktop/src/shared/api/openapi.ts`) and
`agent-kit/muse4ai/references/*.md` — it replaces an earlier version of this
adapter that guessed a generic `/videos` endpoint shape before the real
product was identified.

It has still NOT been run against a live Muse4AI instance: that needs a
Windows PC with the app installed and a signed-in Muse account, neither of
which exist in the environment this was written in. It has been tested
against a mock server built from the documented contract (see
agents/muse/test_adapter.py) — request/response parsing is verified; the
real Muse4AI app's actual behavior is not.

Facts from the real API (not guessed):
* Default local address: http://127.0.0.1:47821/v1 (port configurable in
  the app's Settings > API & agent).
* Auth: header `Authorization: Bearer msk_...` (key created in the app).
* POST /v1/jobs body: {"kind": "video"|"image", "prompt": str (<=4000 chars),
  "repeat"?: 1-4, "account"?: str (alias or "auto"), "mode"?, "reference_id"?,
  "reference_asset_id"?, "reference_ids"?, "site"?}. There is NO
  duration/resolution/style parameter — Muse itself decides those.
* Response: 202 {"jobs": [Job, ...]} — an ARRAY, because `repeat` can create
  more than one job from a single call.
* Job.status: queued | running | needs_review | succeeded | failed |
  cancelled (Muse4AI's own vocabulary — mapped to this project's TaskStatus
  in backend/services/dispatcher.py, not here).
* Job.outputs[].download_url is a signed link valid 60 minutes, no key
  needed to fetch it.
* Errors are RFC 9457 problem+json: {"code", "detail", "status", ...}.
"""

from pathlib import Path
from typing import Optional

import httpx

#: Muse4AI's own job-status vocabulary -> this project's TaskStatus values.
#: "needs_review" and "cancelled" are handled specially by the dispatcher,
#: not via this map, since they are not plain success/failure.
MUSE4AI_STATUS_TO_TASK_STATUS = {
    "queued": "QUEUED",
    "running": "RUNNING",
    "succeeded": "COMPLETED",
    "failed": "FAILED",
}

_MIME_EXTENSIONS = {"video/mp4": "mp4", "image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}


class Muse4AIError(Exception):
    pass


def _require_config(base_url: str, api_key: str) -> None:
    if not base_url or not api_key:
        raise Muse4AIError(
            "Muse4AI is not configured. Install it (https://muse4ai.andrewbabo.com), "
            "create an API key in Settings > API & agent, and set MUSE4AI_BASE_URL / "
            "MUSE4AI_API_KEY in config/.env — see Requirement.md AS-002."
        )


def _raise_for_problem(response: httpx.Response) -> None:
    if response.status_code < 400:
        return
    detail = response.text
    try:
        problem = response.json()
        detail = problem.get("detail") or problem.get("code") or detail
    except ValueError:
        pass
    raise Muse4AIError(f"Muse4AI returned {response.status_code}: {str(detail)[:500]}")


def submit_video(base_url: str, api_key: str, prompt: str, *, repeat: int = 1, account: str = "auto") -> dict:
    """POST /v1/jobs {kind: video}. Returns the first Job dict — `repeat` > 1
    creates more than one job per call; callers that use `repeat` should read
    the caller's own response rather than assume a single job."""
    _require_config(base_url, api_key)
    response = httpx.post(
        f"{base_url}/jobs",
        json={"kind": "video", "prompt": prompt, "repeat": repeat, "account": account},
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30,
    )
    _raise_for_problem(response)
    jobs = response.json().get("jobs", [])
    if not jobs:
        raise Muse4AIError("Muse4AI accepted the request but returned no jobs")
    return jobs[0]


def get_job(base_url: str, api_key: str, job_id: str, wait_seconds: int = 0) -> dict:
    """GET /v1/jobs/{id}, optionally long-polling up to `wait_seconds` for a
    status change (the API's own `wait` query parameter)."""
    _require_config(base_url, api_key)
    params = {"wait": wait_seconds} if wait_seconds else {}
    response = httpx.get(
        f"{base_url}/jobs/{job_id}",
        params=params,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=wait_seconds + 30,
    )
    _raise_for_problem(response)
    return response.json()


def cancel_job(base_url: str, api_key: str, job_id: str) -> None:
    _require_config(base_url, api_key)
    response = httpx.post(
        f"{base_url}/jobs/{job_id}/cancel",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30,
    )
    _raise_for_problem(response)


def download_output(output: dict, dest_dir: str) -> str:
    """`output` is one item of a Job's `outputs` array. The download_url is a
    signed link valid 60 minutes per the real API — no auth header needed."""
    download_url = output.get("download_url")
    if not download_url:
        raise Muse4AIError(f"Output {output.get('asset_id')} has no download_url (not ready or expired)")

    extension = _MIME_EXTENSIONS.get(output.get("mime", ""), "bin")
    dest_path = Path(dest_dir) / f"{output['asset_id']}.{extension}"
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with httpx.stream("GET", download_url, timeout=120) as response:
        _raise_for_problem(response)
        with open(dest_path, "wb") as f:
            for chunk in response.iter_bytes():
                f.write(chunk)
    return str(dest_path)

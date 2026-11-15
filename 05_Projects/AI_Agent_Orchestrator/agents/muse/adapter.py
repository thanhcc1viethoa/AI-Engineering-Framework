"""Muse4AI / Meta Muse adapter — Requirement.md FR-008.

UNVERIFIED (Requirement.md AS-002): the endpoint paths and JSON shape below
(`POST {base_url}/videos`, `GET {base_url}/videos/{job_id}`, a `download_url`
field) are a generic placeholder, not confirmed against Muse4AI's real,
current API documentation or the user's account. Confirm the real contract
before relying on this in production and adjust the three functions below.
"""

from pathlib import Path

import httpx


class Muse4AIError(Exception):
    pass


def _require_config(base_url: str, api_key: str) -> None:
    if not base_url or not api_key:
        raise Muse4AIError(
            "Muse4AI is not configured (MUSE4AI_BASE_URL / MUSE4AI_API_KEY) — see Requirement.md AS-002."
        )


def submit_video(base_url: str, api_key: str, prompt: str, **params) -> str:
    _require_config(base_url, api_key)
    response = httpx.post(
        f"{base_url}/videos",
        json={"prompt": prompt, **params},
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["job_id"]


def get_job_status(base_url: str, api_key: str, job_id: str) -> dict:
    _require_config(base_url, api_key)
    response = httpx.get(
        f"{base_url}/videos/{job_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def download_video(base_url: str, api_key: str, job_id: str, dest_dir: str) -> str:
    status = get_job_status(base_url, api_key, job_id)
    download_url = status.get("download_url")
    if not download_url:
        raise Muse4AIError(f"Job {job_id} has no download_url yet (status={status.get('status')})")

    dest_path = Path(dest_dir) / f"{job_id}.mp4"
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with httpx.stream("GET", download_url, timeout=120) as response:
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in response.iter_bytes():
                f.write(chunk)
    return str(dest_path)

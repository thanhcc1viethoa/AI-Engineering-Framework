"""YouTube Data API v3 adapter — real REST endpoints (no SDK dependency, so
this is easy to test with mocked HTTP, same pattern as agents/muse/adapter.py).

Facts below are Google's long-standing, publicly documented resumable-upload
protocol and OAuth2 token endpoint — stable, widely used public APIs, not a
guess the way the first draft of the Muse4AI adapter was.

* OAuth scope: https://www.googleapis.com/auth/youtube.upload
* Token refresh: POST https://oauth2.googleapis.com/token (grant_type=refresh_token)
* Upload init: POST https://www.googleapis.com/upload/youtube/v3/videos
  ?uploadType=resumable&part=snippet,status, body = video metadata JSON,
  headers X-Upload-Content-Type / X-Upload-Content-Length -> response
  `Location` header is the upload session URL.
* Upload: PUT the video bytes to that Location URL -> returns the created
  Video resource (has `id`).
* An API project Google has not verified/audited (true by default for a
  newly created one) is restricted to privacyStatus private/unlisted —
  YouTube enforces this itself regardless of what is requested here.

Requires a one-time OAuth consent that only a real browser on the user's
machine can do — see scripts/setup_youtube_oauth.py, which writes the token
file this module reads. This adapter has not been run against the real API
(no Google Cloud project/OAuth app exists in this environment); it has been
tested against mocked HTTP responses shaped like the documented contract —
see agents/publisher/test_youtube.py.
"""

import json
from pathlib import Path
from typing import Optional

import httpx

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"


class YouTubeError(Exception):
    pass


def _load_token_file(token_path: str) -> dict:
    path = Path(token_path)
    if not path.exists():
        raise YouTubeError(
            f"No YouTube OAuth token file at {token_path}. Run "
            "`python scripts/setup_youtube_oauth.py <client_secret.json>` once, with a "
            "real browser, to create it."
        )
    return json.loads(path.read_text())


def _get_access_token(token_path: str) -> str:
    token_data = _load_token_file(token_path)
    response = httpx.post(
        TOKEN_URL,
        data={
            "client_id": token_data["client_id"],
            "client_secret": token_data["client_secret"],
            "refresh_token": token_data["refresh_token"],
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    if response.status_code >= 400:
        raise YouTubeError(f"YouTube token refresh failed ({response.status_code}): {response.text[:300]}")
    return response.json()["access_token"]


def upload_video(
    token_path: str,
    video_path: str,
    title: str,
    description: str = "",
    tags: Optional[list[str]] = None,
    privacy_status: str = "private",
) -> dict:
    """privacy_status: private/unlisted/public. An unaudited Google Cloud
    project is forced by YouTube to private/unlisted regardless of what is
    requested here, until the project passes Google's verification."""
    video_file = Path(video_path)
    if not video_file.exists():
        raise YouTubeError(f"Video file not found: {video_path}")

    access_token = _get_access_token(token_path)
    metadata = {
        "snippet": {"title": title, "description": description, "tags": tags or []},
        "status": {"privacyStatus": privacy_status},
    }

    init_response = httpx.post(
        UPLOAD_URL,
        params={"uploadType": "resumable", "part": "snippet,status"},
        json=metadata,
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-Upload-Content-Type": "video/*",
            "X-Upload-Content-Length": str(video_file.stat().st_size),
        },
        timeout=30,
    )
    if init_response.status_code >= 400:
        raise YouTubeError(f"YouTube upload session init failed ({init_response.status_code}): {init_response.text[:300]}")
    upload_session_url = init_response.headers.get("Location")
    if not upload_session_url:
        raise YouTubeError("YouTube accepted the upload init but returned no session URL")

    upload_response = httpx.put(
        upload_session_url,
        content=video_file.read_bytes(),
        headers={"Content-Type": "video/*"},
        timeout=600,
    )
    if upload_response.status_code >= 400:
        raise YouTubeError(f"YouTube upload failed ({upload_response.status_code}): {upload_response.text[:300]}")

    video_resource = upload_response.json()
    video_id = video_resource["id"]
    return {"video_id": video_id, "url": f"https://youtu.be/{video_id}"}


def get_video_status(token_path: str, video_id: str) -> dict:
    access_token = _get_access_token(token_path)
    response = httpx.get(
        VIDEOS_URL,
        params={"part": "status,processingDetails", "id": video_id},
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    if response.status_code >= 400:
        raise YouTubeError(f"YouTube status check failed ({response.status_code}): {response.text[:300]}")
    items = response.json().get("items", [])
    if not items:
        raise YouTubeError(f"Video {video_id} not found")
    return items[0]

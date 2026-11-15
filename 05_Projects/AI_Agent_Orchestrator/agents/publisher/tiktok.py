"""TikTok Content Posting API (v2) adapter — real documented endpoints.

Facts (developers.tiktok.com/docs/en/content-posting-api-get-started and
.../content-sharing-guidelines, found via search; this container's network
policy was not tested against open.tiktokapis.com directly, so these have
not been confirmed by this adapter actually calling the live API):

* POST /v2/post/publish/video/init/ with `post_info` (title, privacy_level,
  ...) and `source_info` (source: "FILE_UPLOAD", video_size, chunk_size,
  total_chunk_count) -> {data: {publish_id, upload_url}}.
* PUT the video bytes to that upload_url with a `Content-Range` header.
* POST /v2/post/publish/status/fetch/ with {publish_id} to poll progress.
* Platform rule, not something this adapter can work around: an "unaudited"
  API client (true by default — TikTok's Content Posting API audit is
  separate from basic app review) can only post at SELF_ONLY (private)
  visibility, capped at 5 distinct TikTok accounts posting per 24h, until
  TikTok completes that audit for the app.

Needs a TikTok Developer app (developers.tiktok.com) with the
`video.publish` scope granted via that app's own OAuth consent flow — a
browser step only the user can do; there is no generic setup script here
because the redirect URI is specific to the app the user registers.
"""

from pathlib import Path

import httpx

BASE_URL = "https://open.tiktokapis.com/v2"


class TikTokError(Exception):
    pass


def _raise_for_error(response: httpx.Response) -> dict:
    try:
        data = response.json()
    except ValueError:
        raise TikTokError(f"TikTok API returned a non-JSON response ({response.status_code}): {response.text[:300]}")
    error = data.get("error") or {}
    if response.status_code >= 400 or error.get("code") not in (None, "ok"):
        raise TikTokError(f"TikTok API error {error.get('code')}: {error.get('message') or response.text[:300]}")
    return data


def post_video(access_token: str, video_path: str, title: str, privacy_level: str = "SELF_ONLY") -> str:
    """Returns a publish_id to poll with get_publish_status.

    privacy_level defaults to SELF_ONLY because an unaudited app cannot post
    publicly — see module docstring. Only override this once the app has
    passed TikTok's Content Posting API audit."""
    video_file = Path(video_path)
    if not video_file.exists():
        raise TikTokError(f"Video file not found: {video_path}")
    video_size = video_file.stat().st_size

    init_response = httpx.post(
        f"{BASE_URL}/post/publish/video/init/",
        json={
            "post_info": {"title": title, "privacy_level": privacy_level},
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size,
                "chunk_size": video_size,
                "total_chunk_count": 1,
            },
        },
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        timeout=30,
    )
    data = _raise_for_error(init_response)
    publish_id = data["data"]["publish_id"]
    upload_url = data["data"]["upload_url"]

    upload_response = httpx.put(
        upload_url,
        content=video_file.read_bytes(),
        headers={"Content-Type": "video/mp4", "Content-Range": f"bytes 0-{video_size - 1}/{video_size}"},
        timeout=600,
    )
    if upload_response.status_code >= 400:
        raise TikTokError(f"TikTok video upload failed ({upload_response.status_code}): {upload_response.text[:300]}")

    return publish_id


def get_publish_status(access_token: str, publish_id: str) -> dict:
    response = httpx.post(
        f"{BASE_URL}/post/publish/status/fetch/",
        json={"publish_id": publish_id},
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        timeout=30,
    )
    data = _raise_for_error(response)
    return data["data"]

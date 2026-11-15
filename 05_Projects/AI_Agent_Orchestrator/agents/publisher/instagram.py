"""Instagram Reels publishing via the Meta Graph API — real documented flow.

Facts (developers.facebook.com/docs/instagram-platform/content-publishing,
found via search; this container's network policy was not tested against
graph.facebook.com directly, so this has not been confirmed by this adapter
actually calling the live API):

* Two-step publish: POST /{ig_user_id}/media with media_type=REELS and
  video_url, then POST /{ig_user_id}/media_publish with the returned
  creation_id.
* Poll GET /{creation_id}?fields=status_code until FINISHED before
  publishing (values seen in the docs: IN_PROGRESS, FINISHED, ERROR, EXPIRED).
* Needs: a Facebook Page linked to an Instagram Business or Creator account,
  a Meta developer app, and — for use beyond the app's own test users — Meta
  App Review granting the content-publishing permission.

**Real limitation this adapter does not solve:** the Graph API's `media_type
=REELS` creation step only accepts `video_url` (a public, directly
downloadable URL) — there is no direct file-upload parameter in this flow.
A video generated locally (e.g. downloaded from Muse4AI into output/videos/)
is not public by default. Posting to Instagram through this Orchestrator
therefore needs the caller to supply an already-public video_url (their own
hosting, cloud storage, CDN, etc.); this adapter does not host the file for
you. A tunnel from this Orchestrator's own output/videos/ to a public URL
(e.g. ngrok/cloudflared) would close this gap and is a reasonable future
extension, not built here.
"""

import httpx

GRAPH_API_VERSION = "v26.0"
BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


class InstagramError(Exception):
    pass


def _raise_for_error(response: httpx.Response) -> dict:
    try:
        data = response.json()
    except ValueError:
        raise InstagramError(f"Instagram API returned a non-JSON response ({response.status_code}): {response.text[:300]}")
    if response.status_code >= 400 or "error" in data:
        error = data.get("error", {})
        raise InstagramError(f"Instagram API error: {error.get('message') or response.text[:300]}")
    return data


def create_reel_container(access_token: str, ig_user_id: str, video_url: str, caption: str = "") -> str:
    """`video_url` MUST already be a public, directly downloadable URL — see
    module docstring. Returns the creation_id to poll and then publish."""
    response = httpx.post(
        f"{BASE_URL}/{ig_user_id}/media",
        params={"media_type": "REELS", "video_url": video_url, "caption": caption, "access_token": access_token},
        timeout=30,
    )
    data = _raise_for_error(response)
    return data["id"]


def get_container_status(access_token: str, creation_id: str) -> str:
    response = httpx.get(
        f"{BASE_URL}/{creation_id}",
        params={"fields": "status_code", "access_token": access_token},
        timeout=30,
    )
    data = _raise_for_error(response)
    return data["status_code"]


def publish_container(access_token: str, ig_user_id: str, creation_id: str) -> str:
    response = httpx.post(
        f"{BASE_URL}/{ig_user_id}/media_publish",
        params={"creation_id": creation_id, "access_token": access_token},
        timeout=30,
    )
    data = _raise_for_error(response)
    return data["id"]

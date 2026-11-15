# agents/publisher

Publisher Agent: posts a generated video to YouTube, TikTok, or Instagram, via each platform's real, documented API — `youtube.py`, `tiktok.py`, `instagram.py`. Dispatched by `payload.platform` (see `backend/services/dispatcher.py`), not a separate `assigned_agent` value per platform, so adding a 4th platform later only needs a new module here plus one more branch in the dispatcher.

Each adapter requires the user's own developer app + OAuth consent on that platform — none of this can be done from inside this project's code:

| Platform | What the user must do first |
| -------- | ----------------------------- |
| YouTube | Create a Google Cloud project, enable the YouTube Data API v3, create an OAuth client (Desktop app), run `scripts/setup_youtube_oauth.py` once |
| TikTok | Register an app at developers.tiktok.com, request the `video.publish` scope, complete that app's own OAuth consent to get an access token |
| Instagram | Create a Meta developer app, link a Facebook Page to an Instagram Business/Creator account, get a Page/User access token with content-publishing permission |

Known real limitation: Instagram's API only accepts a public `video_url`, not a local file — see `instagram.py`'s module docstring.

Owning requirement: FR-033 in `../../Requirement.md`.

"""One-time YouTube OAuth setup — run this locally with a real browser.
Not run by the Orchestrator itself; the user runs it once by hand.

Prerequisites (done once, in Google Cloud Console — console.cloud.google.com):
1. Create a project (or reuse one), enable "YouTube Data API v3".
2. Credentials > Create credentials > OAuth client ID > Application type
   "Desktop app". Download the JSON — that is <client_secret.json> below.

Usage:
    pip install google-auth-oauthlib
    python scripts/setup_youtube_oauth.py path/to/client_secret.json

Opens a browser for you to sign in and approve the "upload videos to your
channel" permission, then writes config/youtube_token.json, which
agents/publisher/youtube.py reads on every upload. Re-run this script if that
file is ever deleted or the refresh token is revoked.
"""

import json
import sys
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python setup_youtube_oauth.py <path-to-client_secret.json>")
        sys.exit(1)

    client_secrets_path = Path(sys.argv[1])
    if not client_secrets_path.exists():
        print(f"File not found: {client_secrets_path}")
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets_path), SCOPES)
    credentials = flow.run_local_server(port=0)

    client_config = json.loads(client_secrets_path.read_text())["installed"]
    token_data = {
        "refresh_token": credentials.refresh_token,
        "client_id": client_config["client_id"],
        "client_secret": client_config["client_secret"],
    }

    project_root = Path(__file__).resolve().parent.parent
    token_path = project_root / "config" / "youtube_token.json"
    token_path.write_text(json.dumps(token_data, indent=2))
    print(f"Saved YouTube OAuth token to {token_path}")
    print("Keep this file secret — it is not committed to git (see .gitignore).")


if __name__ == "__main__":
    main()

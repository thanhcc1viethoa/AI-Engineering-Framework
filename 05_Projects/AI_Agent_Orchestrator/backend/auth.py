"""Dashboard authentication — Requirement.md FR-025.

Single shared password for a single-operator tool (not multi-user accounts).
The password and JWT secret come only from environment variables (FR-026);
`/system/status` is intentionally left open so `scripts/health_check.ps1`
can poll it without holding a token — it exposes only aggregate counters,
no task/agent detail.
"""

import time
from typing import Optional

import jwt
from fastapi import Header, HTTPException

import config

ALGORITHM = "HS256"


def create_token() -> str:
    now = int(time.time())
    payload = {"sub": "dashboard", "iat": now, "exp": now + config.DASHBOARD_TOKEN_TTL_SECONDS}
    return jwt.encode(payload, config.DASHBOARD_JWT_SECRET, algorithm=ALGORITHM)


def verify_token(token: str) -> bool:
    try:
        jwt.decode(token, config.DASHBOARD_JWT_SECRET, algorithms=[ALGORITHM])
        return True
    except jwt.PyJWTError:
        return False


async def require_auth(authorization: Optional[str] = Header(default=None)) -> None:
    if not config.DASHBOARD_JWT_SECRET or not config.DASHBOARD_PASSWORD:
        raise HTTPException(
            status_code=503,
            detail="Dashboard auth is not configured (set DASHBOARD_PASSWORD and DASHBOARD_JWT_SECRET).",
        )
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.removeprefix("Bearer ").strip()
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

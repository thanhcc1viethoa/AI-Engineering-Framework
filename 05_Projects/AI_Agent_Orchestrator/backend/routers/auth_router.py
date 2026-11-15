"""Login endpoint — Requirement.md FR-025."""

import hmac

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import config
from auth import create_token

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest) -> LoginResponse:
    if not config.DASHBOARD_PASSWORD or not config.DASHBOARD_JWT_SECRET:
        raise HTTPException(
            status_code=503,
            detail="Dashboard auth is not configured (set DASHBOARD_PASSWORD and DASHBOARD_JWT_SECRET).",
        )
    if not hmac.compare_digest(data.password, config.DASHBOARD_PASSWORD):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return LoginResponse(access_token=create_token(), expires_in=config.DASHBOARD_TOKEN_TTL_SECONDS)

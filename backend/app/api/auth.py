import secrets
import hashlib
import base64
import json

from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow

from app.core.config import settings
from app.core.security import encrypt_token
from app.database.session import get_db
from app.models.user import User
from app.models.gmail_token import GmailToken

router = APIRouter(prefix="/api/auth/google", tags=["google-auth"])

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/userinfo.email", "openid"]


def _base64_url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _generate_code_verifier() -> str:
    return _base64_url_encode(secrets.token_bytes(32))


def _code_challenge(verifier: str) -> str:
    return _base64_url_encode(hashlib.sha256(verifier.encode()).digest())


def get_flow(redirect_uri: str | None = None) -> Flow:
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri] if redirect_uri else [],
            }
        },
        scopes=SCOPES,
    )
    if redirect_uri:
        flow.redirect_uri = redirect_uri
    return flow


@router.get("/login")
async def google_login(telegram_id: str = Query(...)):
    redirect_uri = "http://localhost:8000/api/auth/google/callback"
    flow = get_flow(redirect_uri)

    code_verifier = _generate_code_verifier()
    code_challenge = _code_challenge(code_verifier)

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes="true",
        state=f"{telegram_id}:{code_verifier}",
        code_challenge_method="S256",
        code_challenge=code_challenge,
    )
    return {"auth_url": auth_url}


@router.get("/callback")
async def google_callback(code: str = Query(...), state: str = Query(...), db: Session = Depends(get_db)):
    FRONTEND_URL = "http://localhost:5173"

    try:
        parts = state.split(":", 1)
        telegram_id = parts[0]
        code_verifier = parts[1] if len(parts) > 1 else ""

        redirect_uri = "http://localhost:8000/api/auth/google/callback"
        flow = get_flow(redirect_uri)
        flow.code_verifier = code_verifier
        flow.fetch_token(code=code)

        creds = flow.credentials
        email = _extract_email(creds.id_token)

        user = db.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id)
            db.add(user)
            db.commit()

        existing = db.query(GmailToken).filter_by(user_id=user.id).first()
        if existing:
            db.delete(existing)
            db.commit()

        token = GmailToken(
            user_id=user.id,
            email=email,
            access_token=encrypt_token(creds.token),
            refresh_token=encrypt_token(creds.refresh_token),
            token_uri=creds.token_uri,
        )
        db.add(token)
        db.commit()

        return RedirectResponse(f"{FRONTEND_URL}?status=connected&email={email}")
    except Exception:
        return RedirectResponse(f"{FRONTEND_URL}?status=error")


def _extract_email(id_token: str | None) -> str:
    if not id_token:
        return ""
    parts = id_token.split(".")
    if len(parts) != 3:
        return ""
    padded = parts[1] + "=" * (4 - len(parts[1]) % 4)
    try:
        payload = json.loads(base64.urlsafe_b64decode(padded))
        return payload.get("email", "")
    except Exception:
        return ""

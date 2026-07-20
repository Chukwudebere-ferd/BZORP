from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.security import decrypt_token
from app.database.session import get_db
from app.models.user import User
from app.models.gmail_token import GmailToken
from app.services.gmail import get_gmail_service, fetch_recent_emails

router = APIRouter(prefix="/api/gmail", tags=["gmail"])


@router.get("/emails")
async def get_recent_emails(telegram_id: str = Query(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = db.query(GmailToken).filter_by(user_id=user.id).first()
    if not token:
        raise HTTPException(status_code=404, detail="Gmail not connected")

    service = get_gmail_service(
        access_token=decrypt_token(token.access_token),
        refresh_token=decrypt_token(token.refresh_token),
        token_uri=token.token_uri,
    )

    emails = fetch_recent_emails(service)
    return {"email_count": len(emails), "emails": emails}

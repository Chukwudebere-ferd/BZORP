from datetime import datetime, timedelta, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from app.core.config import settings


def get_gmail_service(access_token: str, refresh_token: str, token_uri: str = "https://oauth2.googleapis.com/token"):
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri=token_uri,
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
    )
    return build("gmail", "v1", credentials=creds)


def fetch_recent_emails(service, max_results: int = 20):
    after = int((datetime.now(timezone.utc) - timedelta(hours=24)).timestamp())
    query = f"after:{after}"

    results = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        meta = service.users().messages().get(userId="me", id=msg["id"], format="metadata", metadataHeaders=["Subject", "From", "Date"]).execute()
        headers = {h["name"]: h["value"] for h in meta.get("payload", {}).get("headers", [])}
        emails.append({
            "id": msg["id"],
            "subject": headers.get("Subject", "(no subject)"),
            "from": headers.get("From", ""),
            "date": headers.get("Date", ""),
        })
    return emails

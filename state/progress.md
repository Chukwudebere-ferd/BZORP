# Bzorp — Quick Progress

> Last updated: 2026-07-20

## ✅ Done

- Core module (config, security, logger)
- Database models (User, GmailToken, DigestLog) + Alembic
- TiDB (MySQL) connection via SQLAlchemy
- Google OAuth flow with PKCE — `/api/auth/google/login` + `/callback`
- CORS middleware for frontend at `localhost:5173`
- Gmail API — `fetch_recent_emails()` returns last 24h
- Gemini AI — `summarize_emails()` / `summarize_emails_for_scheduler()`
- Frontend — basic Gmail connect UI in `App.tsx`
- Frontend — post-connect email dashboard (fetches & displays last 24h emails)

## ✅ Done

- Telegram bot — `/start` sends welcome + connect link, `/summary` fetches emails → Gemini → Telegram

## ✅ Done

- Scheduler — daily digest via APScheduler (sends to all connected users at configurable time)
- URLs now configurable via `FRONTEND_URL` and `BACKEND_URL` env vars

## ⬜ Remaining

- Scheduler — daily digest via APScheduler
- React frontend dashboard
- Deployment config

## Key Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app + lifespan |
| `backend/app/api/auth.py` | Google OAuth routes |
| `backend/app/api/gmail.py` | Email fetch endpoint |
| `backend/app/services/gmail.py` | Gmail client + fetch logic |
| `backend/app/services/ai.py` | Gemini summarization |
| `backend/app/models/user.py` | User model |
| `backend/app/models/gmail_token.py` | OAuth token storage |
| `backend/app/models/digest_log.py` | Digest history |
| `frontend/src/App.tsx` | OAuth connect UI |

## Dev Commands

```bash
# Backend
cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend && npm run dev
```

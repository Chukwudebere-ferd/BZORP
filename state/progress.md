# Bzorp — Quick Progress

> Last updated: 2026-07-20

## ✅ Done

- Core module (config, security, logger)
- Database models (User, GmailToken, DigestLog) + Alembic + TiDB
- Google OAuth with PKCE — `/api/auth/google/login` + `/callback`
- Gmail API — `fetch_recent_emails()` returns last 24h
- Gemini AI — `summarize_emails()` / `summarize_emails_for_scheduler()`
- Frontend — Gmail connect + email dashboard with detail view
- Frontend hosted on Vercel: https://bzorp.vercel.app
- Telegram bot — `/start` welcome, `/summary` fetch → Gemini → Telegram
- Scheduler — daily digest via APScheduler (configurable time)
- URLs configurable via `FRONTEND_URL` / `BACKEND_URL` / `VITE_API_URL`

## ⬜ Remaining (you mentioned interest in)

- Send emails / auto-replies from bot
- Screenshot analysis via Gemini Vision
- Deploy backend to a server
- Serve frontend from FastAPI for single-deploy option

## Key Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app + lifespan (bot + scheduler) |
| `backend/app/api/auth.py` | Google OAuth routes |
| `backend/app/api/gmail.py` | Email fetch endpoint |
| `backend/app/services/gmail.py` | Gmail client + fetch logic |
| `backend/app/services/ai.py` | Gemini summarization |
| `backend/app/services/bot.py` | Telegram bot handlers |
| `backend/app/scheduler/__init__.py` | Daily digest scheduler |
| `backend/app/core/config.py` | All settings (now includes URLs) |
| `frontend/src/App.tsx` | Full dashboard with email list + detail |

## To Deploy Backend

1. Set `BACKEND_URL` to your public server URL in `.env`
2. Add the callback URL (`{BACKEND_URL}/api/auth/google/callback`) to Google Cloud Console → Authorized redirect URIs
3. Set `VITE_API_URL` in Vercel project settings to your backend URL

## Dev Commands

```bash
# Backend
cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend && npm run dev
```

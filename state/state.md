# Bzorp — Project State

> Last updated: 2026-07-20

## Overview

AI-powered email summaries delivered to Telegram. Gmail → Gemini AI → Telegram digest.

## Tech Stack

| Layer     | Technology                          |
| --------- | ----------------------------------- |
| Backend   | Python 3.14+, FastAPI, Uvicorn     |
| Frontend  | React, TypeScript, Vite            |
| AI        | Gemini API                          |
| Database  | TiDB (MySQL-compatible)            |
| Auth      | Google OAuth, Telegram Login        |
| Scheduler | APScheduler                        |
| Bot       | python-telegram-bot                |
| Deploy    | Pxxl                               |

## Project Structure

```
Bzorp/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logger.py
│   │   ├── database/
│   │   │   └── session.py
│   │   ├── api/
│   │   │   ├── auth.py          # Google OAuth login/callback
│   │   │   └── gmail.py         # GET /api/gmail/emails
│   │   ├── services/
│   │   │   ├── gmail.py         # Gmail API client, fetch_recent_emails
│   │   │   ├── ai.py            # Gemini summarization
│   │   │   └── bot.py           # Telegram bot handlers
│   │   ├── scheduler/
│   │   │   └── __init__.py
│   │   └── models/
│   │       ├── user.py
│   │       ├── gmail_token.py
│   │       └── digest_log.py
│   ├── alembic/
│   │   └── versions/
│   ├── .venv/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── state/
│   ├── state.md
│   └── progress.md
└── README.md
```

## Dev Commands

### Backend

```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run dev
```

## Progress

| Step | Feature | Status | Date |
|------|---------|--------|------|
| 1    | Project scaffold & state tracking | ✅ Done | 2026-07-20 |
| 2    | Backend scaffold (FastAPI + deps) | ✅ Done | 2026-07-20 |
| 3    | Frontend scaffold (Vite + React + TS) | ✅ Done | 2026-07-20 |
| 4    | Core module (config, security, logger) | ✅ Done | 2026-07-20 |
| 5    | Google Material Design auth UI | ✅ Done | 2026-07-20 |
| 6    | Dashboard redesign (Kretya-style email list + detail view) | ✅ Done | 2026-07-20 |
| 5    | Database models + Alembic + TiDB connection | ✅ Done | 2026-07-20 |
| 6    | Google OAuth flow (PKCE, token storage) | ✅ Done | 2026-07-20 |
| 7    | Gmail API — fetch last 24h emails | ✅ Done | 2026-07-20 |
| 8    | Gemini AI summarization service | ✅ Done | 2026-07-20 |
| 9    | Frontend — OAuth connect UI | ✅ Done | 2026-07-20 |
| 10   | Frontend — post-connect email dashboard | ✅ Done | 2026-07-20 |
| 11   | Telegram bot — /start, /summary | ✅ Done | 2026-07-20 |
| 12   | Scheduler — daily digest | ✅ Done | 2026-07-20 |
| 13   | React frontend full dashboard | ⬜ Pending | — |

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-07-20 | Use `uv` for Python package management | Modern, fast, lock-file based |
| 2026-07-20 | Deploy on Pxxl | Company standard |
| 2026-07-20 | FastAPI + Uvicorn for backend | ASGI, async-native, production-ready |
| 2026-07-20 | React + Vite + TypeScript for frontend | Modern, fast dev experience |
| 2026-07-20 | core/ module for config, security, logger | Single source of truth, avoids scattering |
| 2026-07-20 | Google Material Design styling for auth UI | Clean, familiar UX; follows Google OAuth brand guidelines |
| 2026-07-20 | Dashboard redesign — Kretya/Asal Design aesthetic | Modern inbox layout with avatar initials, split-panel email list/detail view |

## Installation Log

| Date | Package | Reason |
|------|---------|--------|
| 2026-07-20 | fastapi, uvicorn, sqlalchemy, alembic, python-telegram-bot, google-api-python-client, google-auth-oauthlib, google-auth-httplib2, python-dotenv, apscheduler, httpx, pymysql, cryptography, pydantic, pydantic-settings, google-genai | Backend core stack |
| 2026-07-20 | react, typescript, vite | Frontend core stack |

## Feature Log

| #  | Feature | Status | Date |
|----|---------|--------|------|
| 1  | Core module (config, security, logger) | ✅ Done | 2026-07-20 |
| 2  | Google Material Design auth form & button | ✅ Done | 2026-07-20 |
| 3  | Dashboard redesign — email list + detail view | ✅ Done | 2026-07-20 |
| 2  | Database models + Alembic | ✅ Done | 2026-07-20 |
| 3  | Google OAuth with PKCE | ✅ Done | 2026-07-20 |
| 4  | Gmail API — fetch_recent_emails | ✅ Done | 2026-07-20 |
| 5  | CORS middleware for frontend | ✅ Done | 2026-07-20 |
| 6  | Gemini AI — summarize_emails | ✅ Done | 2026-07-20 |
| 7  | Frontend — Gmail connect button | ✅ Done | 2026-07-20 |
| 8  | Frontend — email dashboard after connect | ✅ Done | 2026-07-20 |
| 9  | Telegram bot — /start, /summary | 🔄 In Progress | 2026-07-20 |
| 10 | Scheduler — daily digest | ⬜ Pending | — |
| 11 | React frontend full dashboard | ⬜ Pending | — |

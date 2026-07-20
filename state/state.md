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
│   │   ├── api/
│   │   ├── services/
│   │   ├── scheduler/
│   │   └── models/
│   ├── .venv/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── .env
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── state/
│   └── state.md
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

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-07-20 | Use `uv` for Python package management | Modern, fast, lock-file based |
| 2026-07-20 | Deploy on Pxxl | Company standard |
| 2026-07-20 | FastAPI + Uvicorn for backend | ASGI, async-native, production-ready |
| 2026-07-20 | React + Vite + TypeScript for frontend | Modern, fast dev experience |
| 2026-07-20 | core/ module for config, security, logger | Single source of truth, avoids scattering |

## Installation Log

| Date | Package | Reason |
|------|---------|--------|
| 2026-07-20 | fastapi, uvicorn, sqlalchemy, alembic, python-telegram-bot, google-api-python-client, google-auth-oauthlib, google-auth-httplib2, python-dotenv, apscheduler, httpx, pymysql, cryptography, pydantic, pydantic-settings, google-genai | Backend core stack |
| 2026-07-20 | react, typescript, vite | Frontend core stack |

## Feature Log

| #  | Feature | Status | Date |
|----|---------|--------|------|
| 1  | Core module (config, security, logger) | ✅ Done | 2026-07-20 |

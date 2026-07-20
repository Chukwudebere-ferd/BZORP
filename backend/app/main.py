from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import setup_logging
from app.api.auth import router as auth_router
from app.api.gmail import router as gmail_router
from app.services.bot import start_bot, stop_bot
from app.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    if settings.telegram_bot_token:
        await start_bot(app)
    if settings.telegram_bot_token:
        start_scheduler(app)
    yield
    if settings.telegram_bot_token:
        stop_scheduler()
    if settings.telegram_bot_token:
        await stop_bot(app)


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(gmail_router)


@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.env}

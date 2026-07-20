import logging
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Bot

from app.core.config import settings
from app.core.security import decrypt_token
from app.database.session import SessionLocal
from app.models.user import User
from app.models.gmail_token import GmailToken
from app.models.digest_log import DigestLog
from app.services.gmail import get_gmail_service, fetch_recent_emails
from app.services.ai import summarize_emails_for_scheduler

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def send_daily_digest():
    logger.info(f"Running daily digest")

    bot = Bot(token=settings.telegram_bot_token)
    db = SessionLocal()
    try:
        tokens = db.query(GmailToken).all()
        if not tokens:
            logger.info("No connected users to send digest to")
            return

        for token in tokens:
            user = db.query(User).filter_by(id=token.user_id).first()
            if not user or not user.is_active:
                continue

            try:
                service = get_gmail_service(
                    access_token=decrypt_token(token.access_token),
                    refresh_token=decrypt_token(token.refresh_token),
                    token_uri=token.token_uri,
                )
                emails = fetch_recent_emails(service)
                summary_text = summarize_emails_for_scheduler(emails)

                await bot.send_message(chat_id=int(user.telegram_id), text=summary_text)

                log = DigestLog(
                    user_id=user.id,
                    email_count=len(emails),
                    summary=summary_text,
                    status="sent",
                )
                db.add(log)
                db.commit()

                logger.info(f"Digest sent to user {user.telegram_id} ({len(emails)} emails)")
            except Exception as e:
                logger.exception(f"Failed to send digest to user {user.telegram_id}")
                db.rollback()
    finally:
        db.close()


def start_scheduler(app):
    if scheduler.running:
        return

    hour, minute = settings.scheduler_time.split(":")
    scheduler.add_job(
        send_daily_digest,
        CronTrigger(hour=int(hour), minute=int(minute)),
        id="daily_digest",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(f"Scheduler started, daily digest at {settings.scheduler_time}")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from app.core.config import settings
from app.core.security import decrypt_token
from app.database.session import SessionLocal
from app.models.user import User
from app.models.gmail_token import GmailToken
from app.services.gmail import get_gmail_service, fetch_recent_emails
from app.services.ai import summarize_emails_for_scheduler

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    await update.message.reply_text(
        f"🤖 Welcome to Bzorp!\n\n"
        f"I'll send you a daily summary of your emails.\n\n"
        f"First, connect your Gmail account:\n"
        f"{settings.frontend_url}\n\n"
        f"Use your Telegram ID to sign in: `{user_id}`\n\n"
        f"After connecting, use /summary to test."
    )


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            await update.message.reply_text(
                "You haven't signed up yet. Use /start to get started."
            )
            return

        token = db.query(GmailToken).filter_by(user_id=user.id).first()
        if not token:
            await update.message.reply_text(
                "You haven't connected your Gmail yet. "
                f"Go to {settings.frontend_url} and sign in with your Telegram ID: `{telegram_id}`"
            )
            return

        await update.message.reply_text("📬 Fetching your emails…")

        service = get_gmail_service(
            access_token=decrypt_token(token.access_token),
            refresh_token=decrypt_token(token.refresh_token),
            token_uri=token.token_uri,
        )

        emails = fetch_recent_emails(service)
        summary_text = summarize_emails_for_scheduler(emails)

        await update.message.reply_text(summary_text)
    except Exception as e:
        logger.exception("Summary failed")
        await update.message.reply_text(f"❌ Something went wrong: {e}")
    finally:
        db.close()


async def start_bot(app):
    bot_app = Application.builder().token(settings.telegram_bot_token).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("summary", summary))

    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()

    app.state.bot_app = bot_app
    logger.info("Telegram bot started")


async def stop_bot(app):
    if hasattr(app.state, "bot_app"):
        await app.state.bot_app.updater.stop()
        await app.state.bot_app.stop()
        await app.state.bot_app.shutdown()
        logger.info("Telegram bot stopped")

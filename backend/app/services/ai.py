from google import genai

from app.core.config import settings


def summarize_emails(emails: list[dict]) -> str:
    if not emails:
        return "No emails in the last 24 hours."

    client = genai.Client(api_key=settings.gemini_api_key)

    lines = []
    for e in emails:
        lines.append(f"- From: {e['from']}\n  Subject: {e['subject']}\n  Date: {e['date']}")

    prompt = f"""You are a smart email assistant. Summarize the following emails from the last 24 hours into a concise morning digest.

Group them into categories like:
- 📌 Requires attention (action needed, replies expected)
- 📅 Meetings & events
- 💬 Conversations
- 📰 Newsletters & promotions
- 💳 Financial updates

Today's emails ({len(emails)} total):

{chr(10).join(lines)}

Write a friendly digest in plain text. Start with a summary line like "You received X emails in the last 24 hours." Then list the categories with bullet points. End with a one-line quick takeaway."""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response.text



def summarize_emails_for_scheduler(emails: list[dict]) -> str:
    if not emails:
        return "☀️ Good morning! No new emails in the last 24 hours. Enjoy your day!"

    client = genai.Client(api_key=settings.gemini_api_key)

    lines = []
    for e in emails:
        lines.append(f"- From: {e['from']}\n  Subject: {e['subject']}\n  Date: {e['date']}")

    prompt = f"""You are a smart email assistant creating a daily morning digest for Telegram.

Summarize these {len(emails)} emails from the last 24 hours into a clean, readable Telegram message.

Use this format:
☀️ Good Morning!

You received {len(emails)} emails in the last 24 hours.

📌 Highlights
• X emails require your attention
• Y meetings or events
• Z newsletters

Then a 2-3 sentence quick summary of what happened.

Keep it plain text. No markdown. No emojis except the ones shown above.

Emails:
{chr(10).join(lines)}"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response.text

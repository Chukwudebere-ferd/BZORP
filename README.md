# 🤖 Bzorp

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge\&logo=react\&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge\&logo=typescript\&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge)
![TiDB](https://img.shields.io/badge/TiDB-Database-EF4E28?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

<p align="center">
AI-powered email summaries delivered where you chat.
</p>

---

## 📖 Overview

**Bzorp** is an open-source AI assistant that connects to your Gmail inbox, analyzes the last 24 hours of emails, and delivers a concise morning summary directly to Telegram.

Instead of opening your inbox and sorting through newsletters, promotions, receipts, and conversations, Bzorp reads everything for you and sends a clean digest before your day starts.

---

## ✨ Features

* Gmail integration via Google OAuth
* Telegram authentication
* AI-generated email summaries using Gemini
* Daily digest of the previous 24 hours
* Smart categorization of emails
* Clean and readable Telegram messages
* Secure OAuth token handling
* Open-source and self-hostable

---

## 🚀 Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic
* TiDB
* APScheduler
* python-telegram-bot
* Google Gmail API
* Gemini API

### Frontend

* React
* TypeScript
* Vite
* CSS

> Additional libraries and tools may be added as the project evolves.

---

## ⚙️ How It Works

```text
User
   │
   ▼
Telegram Login
   │
   ▼
Connect Gmail Account
   │
   ▼
Google OAuth
   │
   ▼
Store Secure Tokens
   │
   ▼
Every Morning
   │
   ▼
Fetch Last 24 Hours of Emails
   │
   ▼
Gemini AI Analysis
   │
   ▼
Generate Digest
   │
   ▼
Send Summary to Telegram
```

---

## 📬 Example Digest

```text
🌅 Good Morning!

You received 18 emails in the last 24 hours.

📌 Highlights

• 2 emails require your attention
• 1 meeting invitation
• 4 work-related conversations
• 3 financial updates
• 8 newsletters

Quick Summary

Your inbox was mostly work-related today. A meeting invitation was received for tomorrow morning, two emails may require a response, and several newsletters were detected.
```

---

## 📂 Project Structure

```text
bzorp/

├── backend/
│   ├── api/
│   ├── auth/
│   ├── gmail/
│   ├── telegram/
│   ├── scheduler/
│   ├── ai/
│   ├── database/
│   └── utils/
│
├── frontend/
│   ├── src/
│   └── public/
│
├── docs/
│
└── README.md
```

---

## 🛠 Planned Improvements

* Outlook support
* Multiple Gmail accounts
* Configurable delivery time
* Timezone support
* Email labels and categories
* AI urgency detection
* Weekly email reports
* Digest history
* Web dashboard
* Slack integration
* Discord integration

---

## 🔒 Privacy

Bzorp only accesses emails after the user explicitly grants permission through Google OAuth.

Email data is processed solely to generate summaries and is never sold or shared with third parties.

---

## 🤝 Contributing

Contributions, ideas, bug reports, and feature requests are welcome.

If you'd like to improve Bzorp, feel free to fork the repository and open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">
Built with ❤️ using Python, FastAPI, React, TypeScript, Gemini, and the Gmail API.
</p>

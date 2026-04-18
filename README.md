# 🤖 Telegram Bot — Render + MongoDB

A production-ready Telegram bot with **inline keyboard buttons**, **MongoDB logging**, and **one-click Render deployment**.

---

## 📁 Project Structure

```
telegram-bot/
├── bot.py            # Main bot entry point
├── config.py         # Environment variable loader
├── database.py       # MongoDB async helper (motor)
├── http_server.py    # Aiohttp health-check server (for Render)
├── requirements.txt  # Python dependencies
├── render.yaml       # Render Blueprint (auto-deploy config)
├── Procfile          # Process definition
├── runtime.txt       # Python version pin
├── .env.example      # Environment variable template
└── .gitignore
```

---

## ⚡ Quick Start (Local)

### 1. Clone & install

```bash
git clone https://github.com/YOUR_USERNAME/telegram-bot.git
cd telegram-bot
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env and fill in BOT_TOKEN and MONGO_URI
```

### 3. Run

```bash
python bot.py
```

---

## ☁️ Deploy on Render (Free)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot.git
git push -u origin main
```

### Step 2 — Create Render Service
1. Go to [render.com](https://render.com) → **New** → **Blueprint**
2. Connect your GitHub repo
3. Render will auto-detect `render.yaml`

### Step 3 — Add Secret Environment Variables
In Render Dashboard → **Environment**:

| Key | Value |
|-----|-------|
| `BOT_TOKEN` | Your Telegram bot token from [@BotFather](https://t.me/BotFather) |
| `MONGO_URI` | Your MongoDB Atlas connection string |

### Step 4 — Deploy 🚀
Click **Apply** — Render will install deps and start your bot!

---

## 🗄️ MongoDB Atlas Setup

1. Go to [cloud.mongodb.com](https://cloud.mongodb.com)
2. Create a free **M0** cluster
3. Create a database user
4. Whitelist IP: `0.0.0.0/0` (allow all, required for Render)
5. Get connection string: **Connect → Drivers → Python**
6. Paste into `MONGO_URI` env var

### Collections created automatically:
- `users` — stores user info on `/start`
- `button_clicks` — logs every button press

---

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Show main menu with buttons |
| `/help` | Show help message |
| `/stats` | Show total users & clicks |

---

## 🔧 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BOT_TOKEN` | ✅ Yes | — | Telegram bot token |
| `MONGO_URI` | ⚠️ Optional | — | MongoDB connection string |
| `DB_NAME` | No | `telegram_bot` | MongoDB database name |
| `EMOJI_ID` | No | `5474667...` | Custom emoji sticker ID |
| `PORT` | No | `8080` | HTTP health-check port |

---

## 🛠️ Tech Stack

- **[python-telegram-bot v21](https://python-telegram-bot.org/)** — Bot framework
- **[motor](https://motor.readthedocs.io/)** — Async MongoDB driver
- **[aiohttp](https://docs.aiohttp.org/)** — Async HTTP server (health checks)
- **[MongoDB Atlas](https://www.mongodb.com/atlas)** — Cloud database (free tier)
- **[Render](https://render.com)** — Cloud hosting (free tier)

---

## ⚠️ Security Notes

- **Never** commit your `.env` file or real `BOT_TOKEN` to Git
- Use Render's **Secret** environment variables for sensitive values
- Rotate your bot token immediately if accidentally exposed via [@BotFather](https://t.me/BotFather) → `/revoke`

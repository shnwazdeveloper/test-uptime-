import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import Database
from config import Config
from http_server import run_http_server

# ==================== LOGGING ====================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== KEYBOARD ====================
EMOJI_ID = Config.EMOJI_ID

def build_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔵 Primary", callback_data="primary_btn"),
            InlineKeyboardButton("✅ Success", callback_data="success_btn"),
        ],
        [
            InlineKeyboardButton("❌ Danger", callback_data="danger_btn"),
        ],
        [
            InlineKeyboardButton(
                text="⭐ Premium Emoji Button",
                callback_data="emoji_btn"
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==================== HANDLERS ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data.get("db")
    user = update.effective_user

    # Save user to MongoDB
    if db:
        await db.save_user({
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })

    reply_markup = build_keyboard()
    await update.message.reply_text(
        text=(
            "<b>🔥 New Button UI Preview</b>\n\n"
            "Colored buttons + premium emoji icons\n\n"
            f"👋 Welcome, {user.first_name}!"
        ),
        parse_mode="HTML",
        reply_markup=reply_markup,
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    db = context.bot_data.get("db")
    data = query.data

    messages = {
        "primary_btn": "🔵 <b>Primary</b> button clicked!",
        "success_btn": "✅ <b>Success</b> button clicked!",
        "danger_btn":  "❌ <b>Danger</b> button clicked!",
        "emoji_btn":   "⭐ <b>Premium Emoji</b> button clicked!",
    }

    text = messages.get(data, "❓ Unknown button")

    # Log click to MongoDB
    if db:
        await db.log_button_click({
            "user_id": query.from_user.id,
            "button": data,
        })

    await query.edit_message_text(
        text=f"{text}\n\n<i>Click /start to go back.</i>",
        parse_mode="HTML",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>📖 Help</b>\n\n"
        "/start - Show main menu\n"
        "/help  - Show this message\n"
        "/stats - Show bot statistics",
        parse_mode="HTML",
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data.get("db")
    if db:
        count = await db.get_user_count()
        clicks = await db.get_total_clicks()
        await update.message.reply_text(
            f"<b>📊 Bot Statistics</b>\n\n"
            f"👥 Total Users: <b>{count}</b>\n"
            f"🖱️ Total Clicks: <b>{clicks}</b>",
            parse_mode="HTML",
        )
    else:
        await update.message.reply_text("⚠️ Database not connected.")


# ==================== MAIN ====================
async def main():
    config = Config()

    # Connect MongoDB
    db = None
    if config.MONGO_URI:
        db = Database(config.MONGO_URI)
        await db.connect()
        logger.info("✅ MongoDB connected.")
    else:
        logger.warning("⚠️  MONGO_URI not set — running without database.")

    # Build the bot application
    application = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .build()
    )

    # Inject DB into bot_data
    application.bot_data["db"] = db

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start HTTP keep-alive server for Render
    if config.PORT:
        asyncio.create_task(run_http_server(config.PORT))
        logger.info(f"🌐 HTTP server running on port {config.PORT}")

    logger.info("🤖 Bot started! Send /start in Telegram.")
    await application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())

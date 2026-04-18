import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ==================== BOT ====================
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    EMOJI_ID: str  = os.getenv("EMOJI_ID", "5474667187258006816")

    # ==================== MONGO ====================
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    DB_NAME: str   = os.getenv("DB_NAME", "telegram_bot")

    # ==================== SERVER ====================
    PORT: int = int(os.getenv("PORT", "8080"))

    def __post_init__(self):
        if not self.BOT_TOKEN:
            raise ValueError("❌ BOT_TOKEN environment variable is not set!")

import logging
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, mongo_uri: str, db_name: str = "telegram_bot"):
        self.mongo_uri = mongo_uri
        self.db_name   = db_name
        self.client    = None
        self.db        = None

    # ==================== CONNECTION ====================
    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db     = self.client[self.db_name]
            # Ping to confirm connection
            await self.client.admin.command("ping")
            logger.info("✅ MongoDB connection successful.")
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            self.db = None

    async def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("🔌 MongoDB disconnected.")

    # ==================== USERS ====================
    async def save_user(self, user_data: dict):
        """Upsert a user record."""
        if not self.db:
            return
        try:
            collection = self.db["users"]
            user_data["updated_at"] = datetime.utcnow()
            await collection.update_one(
                {"user_id": user_data["user_id"]},
                {
                    "$set": user_data,
                    "$setOnInsert": {"created_at": datetime.utcnow()},
                },
                upsert=True,
            )
        except Exception as e:
            logger.error(f"save_user error: {e}")

    async def get_user_count(self) -> int:
        """Return total number of unique users."""
        if not self.db:
            return 0
        try:
            return await self.db["users"].count_documents({})
        except Exception as e:
            logger.error(f"get_user_count error: {e}")
            return 0

    # ==================== BUTTON CLICKS ====================
    async def log_button_click(self, click_data: dict):
        """Insert a button click log entry."""
        if not self.db:
            return
        try:
            click_data["timestamp"] = datetime.utcnow()
            await self.db["button_clicks"].insert_one(click_data)
        except Exception as e:
            logger.error(f"log_button_click error: {e}")

    async def get_total_clicks(self) -> int:
        """Return total number of button clicks logged."""
        if not self.db:
            return 0
        try:
            return await self.db["button_clicks"].count_documents({})
        except Exception as e:
            logger.error(f"get_total_clicks error: {e}")
            return 0

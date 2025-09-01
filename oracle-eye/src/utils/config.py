import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    def __init__(self):
        # Telegram API configuration
        self.TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID", "0"))
        self.TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")
        self.TELEGRAM_PHONE_NUMBER = os.getenv("TELEGRAM_PHONE_NUMBER", "")
        
        # Collection settings
        self.COLLECTION_INTERVAL = int(os.getenv("COLLECTION_INTERVAL", "86400"))  # 24 hours
        self.COLLECTION_ENABLED = os.getenv("COLLECTION_ENABLED", "true").lower() == "true"
        self.MAX_MESSAGES_PER_COLLECTION = int(os.getenv("MAX_MESSAGES_PER_COLLECTION", "1000"))
        
        # Database configuration
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../shared/database/crypto_insights.db")
        
        # Create sessions directory for Telethon
        self.SESSIONS_DIR = Path("../shared/sessions")
        self.SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Validate required configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate that required configuration is present"""
        if not self.TELEGRAM_API_ID:
            raise ValueError("TELEGRAM_API_ID is required")
        if not self.TELEGRAM_API_HASH:
            raise ValueError("TELEGRAM_API_HASH is required")
        if not self.TELEGRAM_PHONE_NUMBER:
            raise ValueError("TELEGRAM_PHONE_NUMBER is required")
        
        # Create database directory
        db_path = Path(self.DATABASE_URL.replace("sqlite:///", ""))
        db_path.parent.mkdir(parents=True, exist_ok=True)

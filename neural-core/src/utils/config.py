import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    def __init__(self):
        # OpenAI API configuration
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        
        # Cost control
        self.MAX_COST_PER_SUMMARY = float(os.getenv("MAX_COST_PER_SUMMARY", "10.00"))
        
        # Database configuration
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../shared/database/crypto_insights.db")
        
        # Validate required configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate that required configuration is present"""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        
        # Create database directory
        db_path = Path(self.DATABASE_URL.replace("sqlite:///", ""))
        db_path.parent.mkdir(parents=True, exist_ok=True)

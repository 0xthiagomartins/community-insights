import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    def __init__(self):
        # OpenAI API configuration
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_ORGANIZATION_ID = os.getenv("OPENAI_ORGANIZATION_ID", "")
        
        # Cost control
        self.DEFAULT_COST_PER_1K_TOKENS = float(os.getenv("DEFAULT_COST_PER_1K_TOKENS", "0.002"))
        self.DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
        self.MAX_COST_PER_SUMMARY = float(os.getenv("MAX_COST_PER_SUMMARY", "10.00"))
        
        # Database configuration
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../shared/database/community_insights.db")
        
        # Logging configuration
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE", "../shared/logs/neural_core.log")
        
        # LangChain configuration
        self.LANGCHAIN_VERBOSE = os.getenv("LANGCHAIN_VERBOSE", "true").lower() == "true"
        self.LANGCHAIN_TRACING = os.getenv("LANGCHAIN_TRACING", "false").lower() == "true"
        
        # Validate required configuration
        self._validate_config()
        self._create_directories()
    
    def _validate_config(self):
        """Validate that required configuration is present"""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
    
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        # Create logs directory
        log_dir = Path(self.LOG_FILE).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create database directory
        db_path = Path(self.DATABASE_URL.replace("sqlite:///", ""))
        db_path.parent.mkdir(parents=True, exist_ok=True)

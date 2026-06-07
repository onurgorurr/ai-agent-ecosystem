import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import yaml


class Settings:
    """Application settings"""

    def __init__(self):
        # Load environment variables
        load_dotenv()

        # API Keys
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
        self.GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
        self.SERPAPI_KEY = os.getenv("SERPAPI_KEY")

        # LLM Provider
        self.LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

        # Database
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/agents.db")
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

        # API Server
        self.API_HOST = os.getenv("API_HOST", "0.0.0.0")
        self.API_PORT = int(os.getenv("API_PORT", "8000"))

        # Logging
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE", "logs/agents.log")

        # Directories
        self.REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "reports"))
        self.GENERATED_CODE_DIR = Path(
            os.getenv("GENERATED_CODE_DIR", "generated_projects")
        )

        # Model defaults
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        # Create directories
        self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        self.GENERATED_CODE_DIR.mkdir(parents=True, exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        Path("data").mkdir(exist_ok=True)

        # Validate
        self._validate()

        # Configure logger
        logger.add(self.LOG_FILE, rotation="500 MB", level=self.LOG_LEVEL)

    def _validate(self):
        """Validate required settings"""
        provider = self.LLM_PROVIDER.lower()
        
        if provider == "openai" and not self.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set. OpenAI will not work.")
        elif provider == "gemini" and not self.GOOGLE_GEMINI_API_KEY:
            logger.warning("GOOGLE_GEMINI_API_KEY not set. Gemini will not work.")
        elif provider == "anthropic" and not self.ANTHROPIC_API_KEY:
            logger.warning("ANTHROPIC_API_KEY not set. Anthropic will not work.")
        
        logger.info(f"LLM Provider: {provider}")
        logger.info(f"Settings loaded. API: {self.API_HOST}:{self.API_PORT}")


# Global settings instance
settings = Settings()

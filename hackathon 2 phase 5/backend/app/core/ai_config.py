from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class AISettings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"  # Latest flash model

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"  # Ignore extra env vars from .env
    )

ai_settings = AISettings()

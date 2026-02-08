import os
from dotenv import load_dotenv

load_dotenv()

from typing import Optional

class Settings:
    PROJECT_NAME: str = "Todo App Phase 5"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changethis_secret_key_extremely_insecure_for_dev")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list = []
    
    # Initialize logic in __init__ or using a property to handle env var parsing
    raw_origins = os.getenv("BACKEND_CORS_ORIGINS")
    if raw_origins:
        BACKEND_CORS_ORIGINS = [origin.strip() for origin in raw_origins.split(",")]
    else:
        BACKEND_CORS_ORIGINS = ["*"]

settings = Settings()

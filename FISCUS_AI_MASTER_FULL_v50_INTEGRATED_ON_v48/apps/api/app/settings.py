from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    JWT_SECRET: str = "dev-secret"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    RATE_LIMIT_PER_MIN: int = 300
    ENABLE_DOCS: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

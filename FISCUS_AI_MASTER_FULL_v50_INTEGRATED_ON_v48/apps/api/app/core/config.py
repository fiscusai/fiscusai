from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./fiscus.db"
    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    ACCESS_EXPIRE_MIN: int = 20
    REFRESH_EXPIRE_DAYS: int = 7
    ENABLE_DOCS: bool = True
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    RATE_LIMIT_PER_MIN: int = 60
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASS: str | None = None
    SMTP_FROM: str = "FISCUS AI <no-reply@example.com>"
    SENTRY_DSN: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()

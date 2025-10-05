import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_DOMAIN: Optional[str] = ""
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    EMAIL_SALT: str

    DEFAULT_PAGE_MIN_LIMIT: int = 1
    DEFAULT_PAGE_MAX_LIMIT: int = 100
    DEFAULT_PAGE_LIMIT: int = 30
    DEFAULT_PAGE_OFFSET: int = 0

    FRONTEND_URL: Optional[str] = "http://localhost:5173"

    API_DOMAIN: Optional[str] = None
    STAGING_API_DOMAIN: Optional[str] = None

    DEFAULT_ADMIN_EMAIL: str
    DEFAULT_ADMIN_PASS: str
    PORT: int = int(os.getenv("PORT", 8000))
    ENVIRONMENT: Optional[str] = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()

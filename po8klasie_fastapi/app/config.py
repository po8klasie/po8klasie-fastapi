from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    site_url: str = Field(..., env="SITE_URL")
    db_url: str = Field(..., env="DATABASE_URL")
    test_db_url: Optional[str] = Field("", env="TEST_DATABASE_URL")
    sentry_dsn: Optional[str] = Field("", env="SENTRY_DSN")
    environment: str = Field("production", env="ENVIRONMENT")

    app_version: str = "v0.0.1"  # TODO: Get from env var


settings = Settings()

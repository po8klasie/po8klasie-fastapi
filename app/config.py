from typing import Optional

from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    db_url: PostgresDsn = Field(..., env="DATABASE_URL")
    sentry_dsn: Optional[str] = Field("", env="SENTRY_DSN")

    app_version: str = "v0.0.1"  # TODO: Get from env var


settings = Settings()

import os

from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    db_url: PostgresDsn = Field(..., env="DATABASE_URL")
    base_dir: str = os.path.dirname(__file__)
    data_assets_root_dir: str = os.path.join(base_dir, "../data_assets")

    app_version: str = "v0.0.1"  # TODO: Get from env var


settings = Settings()

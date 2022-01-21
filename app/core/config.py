from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # ENV configs
    APP_ENVIRONMENT: str = "dev"  # TODO: transform it in a enum.
    AP1_V1_STR: str = "/api/v1"

    # DB configs
    SQLALCHEMY_DB_URI: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

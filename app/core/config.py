import secrets
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # ENV configs
    APP_ENVIRONMENT: str = "dev"  # TODO: transform it in a enum.
    BASE_URL: str = "http://localhost"
    API_V1_STR: str = "/api/v1"

    # SECURITY configs
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        60 * 3
    )  # 60 min * 3 hrs = 3 hours

    # DB configs
    SQLALCHEMY_DB_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

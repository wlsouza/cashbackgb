import os
import secrets
from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

class Settings(BaseSettings):
    # ENV configs
    APP_ENVIRONMENT: str = "dev"
    BASE_URL: str = "http://localhost"
    API_V1_STR: str = "/api/v1"
    STAGE: str = ""

    @validator("STAGE", pre=True)
    def define_root_path(
        cls, v:str, values: Dict[str, Any]
    ) -> str:
        if v:
            return v
        # I didn't use walrus operator for old versions compatibility reasons.
        stage = os.environ.get('STAGE', None)
        if stage:
            return f"/{stage}"
        return ""

    # SECURITY configs
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 3  # 60 min * 3 hrs = 3 hours

    # DB configs
    PROD_DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/CASHBACKGB"  # noqa
    TEST_DB_URL: str = "sqlite+aiosqlite:///test.db"
    SQLALCHEMY_DB_URL: Optional[str] = None

    @validator("SQLALCHEMY_DB_URL", pre=True)
    def define_database_uri(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Optional[str]:
        if v:
            return v
        if values.get("APP_ENVIRONMENT") == "PROD":
            return values.get("PROD_DB_URL")
        return values.get("TEST_DB_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

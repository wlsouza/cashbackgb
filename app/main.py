from typing import Any

from fastapi import FastAPI

from app.api.api_v1.api import api_v1_router
from app.core.config import settings

app = FastAPI()

app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.get("/")
def im_alive() -> Any:
    return "Hi, I'm alive!"

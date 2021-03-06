from typing import Any

from fastapi import FastAPI
from mangum import Mangum

from app.api.api_v1.api import api_v1_router
from app.core.config import settings

app = FastAPI(title="CashbackGB", root_path=settings.STAGE)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.get("/")
def im_alive() -> Any:
    return "Hi, I'm alive!"


handler = Mangum(app)

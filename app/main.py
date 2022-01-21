from typing import Any

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def im_alive() -> Any:
    return "Hi, I'm alive!"

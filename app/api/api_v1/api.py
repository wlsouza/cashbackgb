from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, purchases

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(users.router, prefix="/users", tags=["users"])
api_v1_router.include_router(purchases.router, prefix="/purchases", tags=["purchases"])
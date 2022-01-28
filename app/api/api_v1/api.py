from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, cashback, purchases, users

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_v1_router.include_router(users.router, prefix="/users", tags=["Users"])
api_v1_router.include_router(
    purchases.router, prefix="/purchases", tags=["Purchases"]
)
api_v1_router.include_router(
    cashback.router, prefix="/cashback", tags=["Cashback"]
)

from os import access
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, crud
from app.api import deps
from app.core.security import create_jwt_token


router = APIRouter()

@router.post(
    "/login",
    response_model=schemas.Token,
    status_code= status.HTTP_200_OK,
    responses= {
        status.HTTP_401_UNAUTHORIZED:{
            "model": schemas.HTTPError
        }
    }
)
async def create_user_token(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await crud.user.get_authenticated_user(
        db=db,
        user_email=form_data.username,
        user_password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_jwt_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
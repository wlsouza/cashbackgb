from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas, models
from app.api import deps

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.Purchase,
    status_code=status.HTTP_201_CREATED,
    responses=deps.GET_TOKEN_USER_RESPONSES,
)
async def create_purchase(
    purchase_in: schemas.PurchaseCreate,
    token_user: models.User = Depends(deps.get_token_user),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    # if the purchase cpf is not the same as the user
    if purchase_in.cpf != token_user.cpf:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "It is not allowed to register purchases for a "
                "different user. Please check the entered CPF."
            )
        )
    # if the purchase code has already been used.
    if await crud.purchase.get_by_code(db=db, code=purchase_in.code):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The purchase code has already been used."
        )
    purchase = await crud.purchase.create(db=db, purchase_in=purchase_in)
    return purchase



from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas, models
from app.api import deps


router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.Purchase],
    status_code=status.HTTP_200_OK,
    responses=deps.GET_TOKEN_USER_RESPONSES,
)
async def get_purchases(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db),
    token_user: models.User = Depends(deps.get_token_user),
) -> Any:
    # return user purchases
    purchases = await crud.purchase.get_multi_by_user_id(
        db=db, user_id=token_user.id, skip=skip, limit=limit
    )
    return purchases


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
    # access rules
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
    target_code_purchase = await crud.purchase.get_by_code(
        db=db, code=purchase_in.code
    )
    if target_code_purchase:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The purchase code has already been used."
        )
    purchase = await crud.purchase.create(db=db, purchase_in=purchase_in)
    return purchase


@router.put(
    "/{purchase_id}",
    response_model=schemas.Purchase,
    status_code=status.HTTP_200_OK,
    responses=deps.GET_TOKEN_USER_RESPONSES,
)
async def update_current_purchase(
    purchase_id: str,
    purchase_in: schemas.PurchaseUpdatePUT,
    token_user: models.User = Depends(deps.get_token_user),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    purchase = await crud.purchase.get_by_id(db=db, id=purchase_id)
    # access rules
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase not found."
        )
    if purchase.user_id != token_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="It is not allowed to change purchases from other users."
        )
    if purchase.status_.name != schemas.statusEnum.IN_VALIDATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Only purchases in validation can be changed."
            )
        )
    # data rules
    if purchase.user_.cpf != purchase_in.cpf:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "It is not allowed to transfer purchases to other users."
            )
        )
    # the "IF"s below have been separated only for readability.
    # (Zen of python n.7)
    if purchase_in.code != purchase.code:
        target_code_purchase = await crud.purchase.get_by_code(
            db=db, code=purchase_in.code
        )
        if target_code_purchase:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The purchase code has already been used."
            )
    purchase = await crud.purchase.update(
        db=db, db_purchase=purchase, purchase_in=purchase_in
    )
    return purchase


@router.delete(
    "/{purchase_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Purchase,
    responses=deps.GET_TOKEN_USER_RESPONSES,
)
async def delete_purchase_by_id(
    purchase_id: int,
    db: AsyncSession = Depends(deps.get_db),
    token_user: models.User = Depends(deps.get_token_user),
):
    purchase = await crud.purchase.get_by_id(db=db, id=purchase_id)
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase not found.",
        )
    if token_user.id != purchase.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    deleted_user = await crud.purchase.delete_by_id(db=db, id=purchase_id)
    return deleted_user

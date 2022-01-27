from typing import Any
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from httpx import AsyncClient

from app import schemas, models
from app.core.config import settings
from app.api import deps

router = APIRouter()



@router.get(
    "/",
    response_model=schemas.CashBack,
    status_code=status.HTTP_200_OK,
    responses=deps.GET_TOKEN_USER_RESPONSES|{503: {"model": schemas.HTTPError}},
)
async def get_cashback(
    async_client: AsyncClient = Depends(deps.get_async_client),
    token_user: models.User = Depends(deps.get_token_user),
) -> Any:
    # get user purchases
    user_purchases = token_user.purchases_

    # sum internal cashback 
    accumulated_cashback = 0
    for purchase in user_purchases:
        accumulated_cashback += float(purchase.cashback_value)
    
    # get cashback of external service
    url =f"{settings.EXTERNAL_CASHBACK_API}?cpf={token_user.cpf}"
    resp = await async_client.get(url)
    
    external_cashback = resp.json().get("cashback")

    # if external service is unavailable return 503
    if resp.status_code != 200 or not external_cashback:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail= "The service is currently unavailable, please try again later."
        ) 

    accumulated_cashback += external_cashback

    return schemas.CashBack(cashback=accumulated_cashback)
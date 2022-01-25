import pytest

from httpx import AsyncClient
from fastapi import status

from app import models
from app.core.config import settings
from app.tests.utils.auth import (
    get_user_token_headers,
    get_expired_user_token_headers,
    get_not_active_user_token_headers
)

# region delete purchase - GET /purchases/

@pytest.mark.asyncio
async def test_get_purchases_must_accept_delete_verb(
    async_client: AsyncClient, random_purchase:models.Purchase
) -> None:
    headers = get_user_token_headers(random_purchase.user_)
    response = await async_client.get(
        url=f"{settings.API_V1_STR}/purchases/", headers=headers
    )
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_when_successfully_get_purchases_must_return_200(
    async_client: AsyncClient, random_purchase:models.Purchase
) -> None:
    headers = get_user_token_headers(random_purchase.user_)
    response = await async_client.get(
        f"{settings.API_V1_STR}/purchases/", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_when_successfully_get_purchases_must_return_a_list(
    async_client: AsyncClient, random_purchase:models.Purchase
) -> None:
    headers = get_user_token_headers(random_purchase.user_)
    response = await async_client.get(
        f"{settings.API_V1_STR}/purchases/", headers=headers
    )
    assert isinstance(response.json(),list)

@pytest.mark.asyncio
async def test_when_successfully_get_purchases_it_must_be_returned(
    async_client: AsyncClient, random_purchase:models.Purchase
) -> None:
    headers = get_user_token_headers(random_purchase.user_)
    response = await async_client.get(
        f"{settings.API_V1_STR}/purchases/", headers=headers
    )
    assert response.json()[0].get("id") == random_purchase.id

@pytest.mark.asyncio
async def test_when_getting_purchases_if_token_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient
) -> None:
    response = await async_client.get(
        f"{settings.API_V1_STR}/purchases/"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_when_getting_purchases_if_token_is_expired_must_return_403(
    async_client: AsyncClient, random_purchase:models.Purchase
) -> None:
    headers = get_expired_user_token_headers(random_purchase.user_)
    response = await async_client.get(
        f"{settings.API_V1_STR}/purchases/", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_getting_purchases_if_token_is_not_active_yet_must_return_403(
    async_client: AsyncClient, random_purchase:models.Purchase
) -> None:
    headers = get_not_active_user_token_headers(random_purchase.user_)
    response = await async_client.get(
        f"{settings.API_V1_STR}/purchases/", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

# endregions
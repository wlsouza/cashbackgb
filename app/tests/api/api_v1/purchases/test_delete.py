import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.core.config import settings
from app.tests.utils.auth import (
    get_expired_user_token_headers,
    get_not_active_user_token_headers,
    get_user_token_headers,
)
from app.tests.utils.user import random_user_dict

# region delete purchase by id - DELETE /purchases/{purchase_id}


@pytest.mark.asyncio
async def test_resource_purchase_id_must_accept_delete_verb(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    response = await async_client.delete(
        url=f"{settings.API_V1_STR}/purchases/{random_purchase.id}"
    )
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_when_successfully_delete_purchase_by_id_must_return_200(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    headers = get_user_token_headers(random_purchase.user_)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_when_successfully_delete_purchase_by_id_it_must_be_returned(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    headers = get_user_token_headers(random_purchase.user_)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
    )
    assert response.json().get("id") == random_purchase.id


@pytest.mark.asyncio
async def test_when_successfully_delete_purchase_by_id_it_must_be_persisted(
    async_client: AsyncClient,
    random_purchase: models.Purchase,
    db: AsyncSession,
) -> None:
    headers = get_user_token_headers(random_purchase.user_)
    await async_client.delete(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
    )
    db_user = await crud.purchase.get_by_id(db=db, id=random_purchase.id)
    assert not db_user


@pytest.mark.asyncio
async def test_when_deleting_purchase_by_id_of_another_user_must_return_403(
    async_client: AsyncClient,
    random_purchase: models.Purchase,
    db: AsyncSession,
) -> None:
    user = await crud.user.create(db=db, user_in=random_user_dict())
    headers = get_user_token_headers(user)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_deleting_purchase_by_id_if_token_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    response = await async_client.delete(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_deleting_purchase_by_id_if_token_is_expired_must_return_403(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    headers = get_expired_user_token_headers(random_purchase.user_)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_deleting_purchase_by_id_if_token_is_not_active_yet_must_return_403(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    headers = get_not_active_user_token_headers(random_purchase.user_)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_deleting_purchase_by_id_if_purchase_does_not_exist_must_return_404(
    random_purchase: models.Purchase,
    async_client: AsyncClient,
    db: AsyncSession,
) -> None:
    purchase_id = random_purchase.id
    headers = get_user_token_headers(random_purchase.user_)
    await crud.purchase.delete_by_id(db=db, id=purchase_id)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/purchases/{purchase_id}", headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


# endregions

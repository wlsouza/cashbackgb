import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, crud
from app.core.config import settings
from app.tests.utils.user import random_user_dict
from app.tests.utils.purchase import (
    random_purchase_dict_for_json,
    random_purchase_dict_for_crud
)
from app.tests.utils.auth import (
    get_user_token_headers,
    get_expired_user_token_headers,
    get_not_active_user_token_headers
)

# region create purchase - POST /purchases/

@pytest.mark.asyncio
async def test_resource_purchases_must_accept_post_verb(
    async_client: AsyncClient
) -> None:
    response = await async_client.post(url=f"{settings.API_V1_STR}/purchases/")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_when_purchase_is_created_returns_status_201(
    random_user:models.User,
    async_client: AsyncClient,
) -> None:
    headers = get_user_token_headers(random_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/purchases/",
        headers=headers,
        json=random_purchase_dict_for_json(random_user)
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_when_purchase_is_created_it_must_be_returned(
    random_user:models.User,
    async_client: AsyncClient,
) -> None:
    payload = random_purchase_dict_for_json(random_user)
    headers = get_user_token_headers(random_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/purchases/",
        headers=headers,
        json=payload
    )
    assert response.json().get("code") == payload["code"]

@pytest.mark.asyncio
async def test_when_purchase_is_created_it_must_be_persisted(
    random_user:models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    payload = random_purchase_dict_for_json(random_user)
    headers = get_user_token_headers(random_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/purchases/",
        headers=headers,
        json=payload
    )
    db_purchase = await crud.purchase.get_by_id(db=db, id=response.json().get("id"))
    assert db_purchase

@pytest.mark.asyncio
async def test_when_purchase_is_created_if_user_cpf_is_not_15350946056_purchase_status_must_in_validation(
    random_user:models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    payload = random_purchase_dict_for_json(random_user)
    headers = get_user_token_headers(random_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/purchases/",
        headers=headers,
        json=payload
    )
    assert response.json().get("status") == "In validation"

@pytest.mark.asyncio
async def test_when_purchase_is_created_if_user_cpf_is_15350946056_purchase_status_must_approved(
    async_client: AsyncClient, db: AsyncSession
) -> None:
    user = await crud.user.get_by_cpf(db=db, cpf="15350946056")
    if not user:
        user_dict = random_user_dict() | {"cpf": "15350946056"}
        user = await crud.user.create(db=db, user_in=user_dict)
    payload = random_purchase_dict_for_json(user)
    headers = get_user_token_headers(user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/purchases/",
        headers=headers,
        json=payload
    )
    assert response.json().get("status") == "Approved"

@pytest.mark.asyncio
async def test_when_creating_purchase_if_token_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient, random_user:models.User,
) -> None:
    payload = random_purchase_dict_for_json(random_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/purchases/", json=payload
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_creating_purchase_if_token_is_expired_must_return_403(
    async_client: AsyncClient, random_user: models.User
) -> None:
    payload = random_purchase_dict_for_json(random_user)
    headers = get_expired_user_token_headers(random_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/purchases/", headers=headers, json=payload
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_creating_purchase_if_token_is_not_active_yet_must_return_403(
    async_client: AsyncClient, random_user: models.User
) -> None:
    payload = random_purchase_dict_for_json(random_user)
    headers = get_not_active_user_token_headers(random_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/purchases/", headers=headers, json=payload
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_creating_purchase_to_another_user_must_return_403(
    random_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    target_user = user = await crud.user.create(
        db=db, user_in=random_user_dict()
    )
    payload = random_purchase_dict_for_json(target_user)
    headers = get_user_token_headers(random_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/purchases/",
        headers=headers,
        json=payload
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_creating_purchase_if_code_has_already_been_must_return_403(
    random_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    new_purchase = await crud.purchase.create(
        db=db, purchase_in=random_purchase_dict_for_crud(user=random_user)
    )
    payload = random_purchase_dict_for_json(random_user) | {"code": new_purchase.code}
    headers = get_user_token_headers(random_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/purchases/",
        headers=headers,
        json=payload
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_creating_purchase_if_body_is_not_valid_must_return_422(
    random_user:models.User,
    async_client: AsyncClient,
) -> None:
    headers = get_user_token_headers(random_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/purchases/",
        headers=headers,
        json={"invalid":"body"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

# endregion
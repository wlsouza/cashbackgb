import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.tests.utils.user import random_user_dict


@pytest.mark.asyncio
async def test_resource_token_must_accept_post_verb(
    async_client: AsyncClient,
) -> None:
    response = await async_client.post(f"{settings.API_V1_STR}/auth/login")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_when_credentials_are_valid_must_return_status_200(
    async_client: AsyncClient, db: AsyncSession
) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    payload = {
        "username": user_dict.get("email"),
        "password": user_dict.get("password"),
    }
    response = await async_client.post(
        f"{settings.API_V1_STR}/auth/login", data=payload
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_login_when_credentials_are_valid_must_return_jwt_token(
    async_client: AsyncClient, db: AsyncSession
) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    payload = {
        "username": user_dict.get("email"),
        "password": user_dict.get("password"),
    }
    response = await async_client.post(
        f"{settings.API_V1_STR}/auth/login", data=payload
    )
    assert response.json().get("access_token")


@pytest.mark.asyncio
async def test_login_when_credentials_are_invalid_must_return_status_401(
    async_client: AsyncClient, db: AsyncSession
) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    payload = {
        "username": user_dict.get("email"),
        "password": f"{user_dict.get('password')}_invalid_password",
    }
    response = await async_client.post(
        f"{settings.API_V1_STR}/auth/login", data=payload
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_when_invalid_payload_are_passed_must_return_status_422(
    async_client: AsyncClient, db: AsyncSession
) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    payload = {
        "field": "testing",
    }
    response = await async_client.post(
        f"{settings.API_V1_STR}/auth/login", data=payload
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

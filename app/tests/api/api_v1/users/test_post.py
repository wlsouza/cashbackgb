import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.tests.utils.user import random_user_dict

# region create user - POST /users/

@pytest.mark.asyncio
async def test_resource_users_must_accept_post_verb(
    async_client: AsyncClient,
) -> None:
    response = await async_client.post(url=f"{settings.API_V1_STR}/users/")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_when_user_is_created_returns_status_201(
    async_client: AsyncClient,
) -> None:
    user_dict = random_user_dict()
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", json=user_dict
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_when_user_is_created_it_must_be_returned(
    async_client: AsyncClient,
) -> None:
    user_dict = random_user_dict()
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", json=user_dict
    )
    assert user_dict["cpf"] == response.json().get("cpf")


@pytest.mark.asyncio
async def test_when_user_is_created_it_must_be_persisted(
    async_client: AsyncClient, db: AsyncSession
) -> None:
    user_dict = random_user_dict()
    await async_client.post(f"{settings.API_V1_STR}/users/", json=user_dict)
    db_user = await crud.user.get_by_email(db=db, email=user_dict["email"])
    assert db_user

@pytest.mark.asyncio
async def test_when_creating_user_if_a_user_with_this_email_already_exist_returns_status_400(
    async_client: AsyncClient, db: AsyncSession
) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", json=user_dict
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_when_creating_user_if_a_user_with_this_cpf_already_exist_returns_status_400(
    async_client: AsyncClient, db: AsyncSession
) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    # change email to fall into cpf verification
    user_dict["email"] = "valid_email@test.com"
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", json=user_dict
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# endregion
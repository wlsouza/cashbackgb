from typing import Dict, Any
import random

import pytest
from unittest import mock
from httpx import AsyncClient, Response
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.api.deps import get_async_client
from app.core.config import settings
from app.tests.utils.auth import (
    get_user_token_headers,
    get_expired_user_token_headers,
    get_not_active_user_token_headers
)
from app.tests.utils.purchase import create_random_purchase_in_db
from app.main import app

@pytest.fixture()
def dependency_overrides():
    yield app.dependency_overrides
    app.dependency_overrides = {}

# region get cashback - GET /cashback/

@pytest.mark.asyncio
async def test_get_cashback_must_accept_get_verb(
    random_user: models.User, async_client: AsyncClient
) -> None:
    headers = get_user_token_headers(random_user)
    response = await async_client.get(
        url=f"{settings.API_V1_STR}/cashback/", headers=headers
    )
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

@pytest.mark.asyncio
async def test_when_successfully_get_cashback_it_must_return_200(
    random_user: models.User, async_client: AsyncClient
) -> None:
    headers = get_user_token_headers(random_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/cashback/", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_when_successfully_get_cashback_it_must_be_returned(
    random_user: models.User, async_client: AsyncClient
) -> None:
    headers = get_user_token_headers(random_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/cashback/", headers=headers
    )
    assert response.json().get("cashback")

@pytest.mark.asyncio
async def test_when_successfully_get_cashback_must_be_the_sum_of_internal_and_external_cashback(
    dependency_overrides: Dict[Any,Any], random_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:

    external_cashback_value = round(random.uniform(10,200),2)
    #mocking external request
    mock_test = mock.AsyncMock()
    mock_test.get.return_value= Response(
        status_code=200, json={"cashback": external_cashback_value}
    )
    dependency_overrides[get_async_client] = lambda:mock_test
    #generating internal cashback value
    internal_cashback_value = 0
    for _ in range(5):
        purchase =  await create_random_purchase_in_db(db=db, user=random_user)
        internal_cashback_value += float(purchase.cashback_value)
    # validating
    headers = get_user_token_headers(random_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/cashback/", headers=headers
    )
    expected = internal_cashback_value + external_cashback_value
    assert response.json().get("cashback") == expected

@pytest.mark.asyncio
async def test_when_getting_cashback_if_external_service_fail_must_return_503(
    dependency_overrides: Dict[Any,Any], random_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    #mocking external request
    mock_test = mock.AsyncMock()
    mock_test.get.return_value= Response(
        status_code=400, json={"detail": "bad request"}
    )
    dependency_overrides[get_async_client] = lambda:mock_test
    # validating
    headers = get_user_token_headers(random_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/cashback/", headers=headers
    )
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

@pytest.mark.asyncio
async def test_when_getting_cashback_if_token_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient
) -> None:
    response = await async_client.get(
        f"{settings.API_V1_STR}/cashback/"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_when_getting_cashback_if_token_is_expired_must_return_403(
    random_user: models.User, async_client: AsyncClient
) -> None:
    headers = get_expired_user_token_headers(random_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/cashback/", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_getting_cashback_if_token_is_not_active_yet_must_return_403(
    random_user: models.User, async_client: AsyncClient
) -> None:
    headers = get_not_active_user_token_headers(random_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/cashback/", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

# endregions
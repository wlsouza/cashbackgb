from unittest import mock
from typing import AsyncGenerator

import pytest
import jwt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from app.api import deps
from app.core.security import create_jwt_token


# region test get_db function
@pytest.mark.asyncio
async def test_get_db_must_return_asyncgenerator():
    db_async_iter = deps.get_db()
    assert isinstance(db_async_iter, AsyncGenerator)


@pytest.mark.asyncio
async def test_get_db_must_can_be_async_iterated():
    db_async_iter = deps.get_db()
    db_session = await db_async_iter.__anext__()
    assert db_session


@pytest.mark.asyncio
async def test_get_db_after_be_async_iterated_must_return_asyncsession():
    db_async_iter = deps.get_db()
    db_session = await db_async_iter.__anext__()
    assert isinstance(db_session, AsyncSession)

# endregion

# region test get_async_client function
@pytest.mark.asyncio
async def test_get_async_client_must_return_asyncgenerator():
    async_client_iter = deps.get_async_client()
    assert isinstance(async_client_iter, AsyncGenerator)


@pytest.mark.asyncio
async def test_get_async_client_must_can_be_async_iterated():
    async_client_iter = deps.get_async_client()
    async_client = await async_client_iter.__anext__()
    assert async_client


@pytest.mark.asyncio
async def test_get_async_after_be_async_iterated_must_return_asyncclient():
    async_client_iter = deps.get_async_client()
    async_client = await async_client_iter.__anext__()
    assert isinstance(async_client, AsyncClient)

# endregion

# region test get_token_payload function


def test_get_token_payload_if_token_is_valid_must_return_the_payload():
    subject="testing"
    token = create_jwt_token(subject=subject)
    payload = deps.get_token_payload(token=token)
    assert subject in payload.values()

@mock.patch("app.api.deps.decode_jwt_token")
def test_get_token_payload_if_token_is_expired_must_return_403_httpexception(
    mocked_decode_jwt_token
):
    # forcing rise ExpiredSignatureError when decode_jwt_token_is_called
    mocked_decode_jwt_token.side_effect=jwt.ExpiredSignatureError()

    with pytest.raises(HTTPException) as exc_info:
        deps.get_token_payload()
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

@mock.patch("app.api.deps.decode_jwt_token")
def test_get_token_payload_if_token_is_not_valid_yet_must_return_403_httpexception(
    mocked_decode_jwt_token
):
    # forcing rise ImmatureSignatureError when decode_jwt_token_is_called
    mocked_decode_jwt_token.side_effect=jwt.ImmatureSignatureError()

    with pytest.raises(HTTPException) as exc_info:
        deps.get_token_payload()
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

@mock.patch("app.api.deps.decode_jwt_token")
def test_get_token_payload_if_token_is_not_valid_must_return_403_httpexception(
    mocked_decode_jwt_token
):
    # forcing rise InvalidTokenError when decode_jwt_token_is_called
    mocked_decode_jwt_token.side_effect=jwt.InvalidTokenError()

    with pytest.raises(HTTPException) as exc_info:
        deps.get_token_payload()
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

# endregion

# region test get_token_user function
@pytest.mark.asyncio
@mock.patch("app.api.deps.crud.user.get_by_id")
async def test_get_token_user_if_payload_is_valid_must_return_the_token_user(
    mocked_crud_user_get_by_id
):
    expected = mock.Mock()
    # forcing crud.user.get_by_id return a Mock object
    mocked_crud_user_get_by_id.return_value=expected
    valid_payload = {
        'exp': 1642985912,
        'nbf': 1642975112,
        'sub': '1'
    }
    result = await deps.get_token_user(payload=valid_payload)
    assert result == expected

@pytest.mark.asyncio
async def test_get_token_user_if_payload_is_not_valid_must_return_403_httpexception():
    invalid_payload = {
        'exp': 1642985912,
        'nbf': 1642975112,
    }
    with pytest.raises(HTTPException) as exc_info:
        await deps.get_token_user(payload=invalid_payload)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
@mock.patch("app.api.deps.crud.user.get_by_id")
async def test_get_token_user_if_payload_user_if_not_found_must_return_404_httpexception(    mocked_crud_user_get_by_id
):
    # forcing crud.user.get_by_id return None
    mocked_crud_user_get_by_id.return_value=None
    valid_payload = {
        'exp': 1642985912,
        'nbf': 1642975112,
        'sub': '1'
    }
    with pytest.raises(HTTPException) as exc_info:
        await deps.get_token_user(payload=valid_payload)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

# endregion
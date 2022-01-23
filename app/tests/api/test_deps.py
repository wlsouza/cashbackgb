from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps


# region test get_db function
@pytest.mark.asyncio
async def test_get_db_must_return_asyncsession():
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

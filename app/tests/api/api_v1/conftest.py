import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.tests.utils.user import (random_user_dict)


@pytest.fixture()
async def random_user(db: AsyncSession) -> models.User:
    user_dict = random_user_dict()
    user = await crud.user.create(db=db, user_in=user_dict)
    return user

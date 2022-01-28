import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.tests.utils.purchase import create_random_purchase_in_db
from app.tests.utils.user import random_user_dict


@pytest_asyncio.fixture()
async def random_user(db: AsyncSession) -> models.User:
    user = await crud.user.create(db=db, user_in=random_user_dict())
    return user


@pytest_asyncio.fixture(name="random_purchase")
async def random_purchase(
    db: AsyncSession, random_user: models.User
) -> models.Purchase:
    purchase = await create_random_purchase_in_db(db=db, user=random_user)
    return purchase

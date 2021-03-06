import asyncio
from typing import AsyncGenerator, List

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.core.config import settings
from app.database.session import async_session
from app.main import app
from app.tests.utils.purchase_status import create_purchase_status_in_db


@pytest_asyncio.fixture(scope="module")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(
        app=app, base_url=settings.BASE_URL
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncGenerator:
    async with async_session() as db:
        yield db


# fixture to create basic purchase_status (used in api and crud tests)
@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_basic_purchase_status(
    db: AsyncSession,
) -> List[models.PurchaseStatus]:
    basic_names = [
        schemas.statusEnum.APPROVED,
        schemas.statusEnum.IN_VALIDATION,
        schemas.statusEnum.DISAPPROVED,
    ]
    status_obj = []
    for status_name in basic_names:
        status = await crud.purchase_status.get_by_name(
            db=db, name=status_name
        )
        if not status:
            status = await create_purchase_status_in_db(
                db=db, name=status_name
            )
        status_obj.append(status)
    return status_obj


# to correct the error "RuntimeError: Task attached to a different loop"
# https://github.com/pytest-dev/pytest-asyncio/issues/38#issuecomment-264418154
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

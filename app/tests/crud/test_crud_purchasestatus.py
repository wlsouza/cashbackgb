import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.tests.utils.purchase_status import random_purchase_status_dict


@pytest.mark.asyncio
async def test_create_purchase_status_by_dict(db: AsyncSession) -> None:
    ps_dict = random_purchase_status_dict()
    new_purchase_status = await crud.purchase_status.create(
        db=db, purchase_status_in=ps_dict
    )
    assert new_purchase_status.name == ps_dict["name"]


@pytest.mark.asyncio
async def test_if_get_by_id_return_correct_purchase_status(
    db: AsyncSession,
) -> None:
    ps_dict = random_purchase_status_dict()
    created_purchase_status = await crud.purchase_status.create(
        db=db, purchase_status_in=ps_dict
    )
    returned_purchase_status = await crud.purchase_status.get_by_id(
        db=db, id=created_purchase_status.id
    )
    assert returned_purchase_status.name == ps_dict["name"]


@pytest.mark.asyncio
async def test_if_get_by_name_return_correct_purchase_status(
    db: AsyncSession,
) -> None:
    created_purchase_status = await crud.purchase_status.create(
        db=db, purchase_status_in=random_purchase_status_dict()
    )
    returned_purchase_status = await crud.purchase_status.get_by_name(
        db=db, name=created_purchase_status.name
    )
    assert returned_purchase_status.id == created_purchase_status.id

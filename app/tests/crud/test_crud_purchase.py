from decimal import Decimal
from typing import List

import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.tests.utils.purchase import random_purchase_dict_for_crud
from app.tests.utils.purchase_status import create_purchase_status_in_db
from app.tests.utils.user import random_user_dict
from app.tests.utils.purchase import fake


@pytest_asyncio.fixture(scope="session", name="random_user")
async def create_random_user(db: AsyncSession) -> models.User:
    user = await crud.user.create(db=db, user_in=random_user_dict())
    return user


@pytest_asyncio.fixture(name="random_purchase")
async def random_purchase(
    db: AsyncSession, random_user: models.User
) -> models.Purchase:
    new_purchase = await crud.purchase.create(
        db=db, purchase_in=random_purchase_dict_for_crud(user=random_user)
    )
    return new_purchase

@pytest.mark.asyncio
async def test_create_purchase_by_schema(
    db: AsyncSession,
    random_user: models.User,
) -> None:
    purchase_dict = random_purchase_dict_for_crud(user=random_user)
    purchase_schema = schemas.PurchaseCreate(**purchase_dict)
    new_purchase = await crud.purchase.create(
        db=db, purchase_in=purchase_schema
    )
    assert new_purchase.code == purchase_dict.get("code")


@pytest.mark.asyncio
async def test_create_purchase_by_dict(
    db: AsyncSession, random_user: models.User
) -> None:
    purchase_dict = random_purchase_dict_for_crud(user=random_user)
    new_purchase = await crud.purchase.create(db=db, purchase_in=purchase_dict)
    assert new_purchase.code == purchase_dict.get("code")


@pytest.mark.asyncio
async def test_when_create_purchase_with_random_user_the_status_id_must_be_of_in_validation(
    db: AsyncSession, random_user: models.User
) -> None:
    purchase_dict = random_purchase_dict_for_crud(user=random_user)
    new_purchase = await crud.purchase.create(db=db, purchase_in=purchase_dict)
    assert new_purchase.status_.name == "In validation"


@pytest.mark.asyncio
async def test_when_create_purchase_with_the_user_of_cpf_15350946056_the_status_id_must_be_of_approved(
    db: AsyncSession,
) -> None:
    user = await crud.user.get_by_cpf(db=db, cpf="15350946056")
    if not user:
        user_dict = random_user_dict() | {"cpf": "15350946056"}
        user = await crud.user.create(db=db, user_in=user_dict)
    new_purchase = await crud.purchase.create(
        db=db, purchase_in=random_purchase_dict_for_crud(user=user)
    )
    assert new_purchase.status_.name == "Approved"


@pytest.mark.asyncio
async def test_if_get_by_id_return_correct_purchase(
    db: AsyncSession, random_purchase: models.Purchase
) -> None:
    returned_purchase = await crud.purchase.get_by_id(
        db=db, id=random_purchase.id
    )
    assert returned_purchase.code == random_purchase.code

@pytest.mark.asyncio
async def test_if_get_by_code_return_correct_purchase(
    db: AsyncSession, random_purchase: models.Purchase
) -> None:
    returned_purchase = await crud.purchase.get_by_code(
        db=db, code=random_purchase.code
    )
    assert returned_purchase.id == random_purchase.id

@pytest.mark.asyncio
async def test_if_delete_by_id_really_delete_the_purchase(
    db: AsyncSession, random_purchase: models.Purchase
) -> None:
    await crud.purchase.delete_by_id(db=db, id=random_purchase.id)
    returned_user = await crud.purchase.get_by_id(db=db, id=random_purchase.id)
    assert returned_user is None


@pytest.mark.asyncio
async def test_update_purchase_by_purchaseupdateput_schema(
    db: AsyncSession, random_purchase: models.Purchase
) -> None:
    update_data = random_purchase_dict_for_crud(user=random_purchase.user_)
    purchase_update_in = schemas.PurchaseUpdatePUT(
        **update_data, status=schemas.statusEnum.IN_VALIDATION
    )
    updated_purchase = await crud.purchase.update(
        db=db, db_purchase=random_purchase, purchase_in=purchase_update_in
    )
    assert updated_purchase.code == update_data.get("code")


@pytest.mark.asyncio
async def test_update_purchase_by_purchaseupdatepatch_schema(
    db: AsyncSession, random_purchase: models.Purchase
) -> None:
    expected_code = fake.uuid4()
    purchase_update_in = schemas.PurchaseUpdatePATCH(code=expected_code)
    updated_purchase = await crud.purchase.update(
        db=db, db_purchase=random_purchase, purchase_in=purchase_update_in
    )
    assert updated_purchase.code == expected_code


@pytest.mark.asyncio
async def test_update_purchase_by_dict(
    db: AsyncSession, random_purchase: models.Purchase
) -> None:
    expected_code = fake.uuid4()
    updated_purchase = await crud.purchase.update(
        db=db, db_purchase=random_purchase, purchase_in={"code": expected_code}
    )
    assert updated_purchase.code == expected_code


@pytest.mark.asyncio
async def test_when_update_purchase_value_must_update_cashback(
    db: AsyncSession, random_purchase: models.Purchase
) -> None:
    old_cashback_value = random_purchase.cashback_value
    random_purchase.cashback_value
    updated_purchase = await crud.purchase.update(
        db=db, db_purchase=random_purchase, purchase_in={"value": Decimal(825)}
    )
    assert updated_purchase.cashback_value != old_cashback_value


@pytest.mark.asyncio
async def test_if_get_multi_return_a_list_of_purchases(
    db: AsyncSession, random_purchase: models.Purchase
) -> None:
    purchases = await crud.purchase.get_multi(db=db, limit=1)
    assert isinstance(purchases, list)


@pytest.mark.asyncio
async def test_if_get_multi_return_the_correct_quantity_of_purchases(
    db: AsyncSession, random_user: models.User
) -> None:
    for _ in range(3):
        await crud.purchase.create(
            db=db, purchase_in=random_purchase_dict_for_crud(user=random_user)
        )
    purchases = await crud.purchase.get_multi(db=db, limit=2)
    assert len(purchases) == 2


@pytest.mark.asyncio
async def test_if_get_multi_skip_the_correct_quantity_of_purchases(
    db: AsyncSession, random_user: models.User
) -> None:
    for _ in range(5):
        await crud.purchase.create(
            db=db, purchase_in=random_purchase_dict_for_crud(user=random_user)
        )
    db_purchases = await crud.purchase.get_multi(db=db, limit=5)
    purchase = await crud.purchase.get_multi(db=db, skip=2, limit=1)
    assert purchase[0].id == db_purchases[2].id


@pytest.mark.asyncio
async def test_if_get_multi_by_user_id_return_a_list_of_purchases(
    db: AsyncSession,
    random_user: models.User,
    random_purchase: models.Purchase,
) -> None:
    purchases = await crud.purchase.get_multi_by_user_id(
        db=db, user_id=random_user.id, limit=1
    )
    assert isinstance(purchases, list)


@pytest.mark.asyncio
async def test_if_get_multi_by_user_id_return_the_correct_quantity_of_purchases(
    db: AsyncSession, random_user: models.User
) -> None:
    for _ in range(3):
        await crud.purchase.create(
            db=db, purchase_in=random_purchase_dict_for_crud(user=random_user)
        )
    purchases = await crud.purchase.get_multi_by_user_id(
        db=db, user_id=random_user.id, limit=2
    )
    assert len(purchases) == 2


@pytest.mark.asyncio
async def test_if_get_multi_by_user_id_skip_the_correct_quantity_of_purchases(
    db: AsyncSession, random_user: models.User
) -> None:
    for _ in range(5):
        await crud.purchase.create(
            db=db, purchase_in=random_purchase_dict_for_crud(user=random_user)
        )
    db_purchases = await crud.purchase.get_multi_by_user_id(
        db=db, user_id=random_user.id, limit=5
    )
    purchase = await crud.purchase.get_multi_by_user_id(
        db=db, user_id=random_user.id, skip=2, limit=1
    )
    assert purchase[0].id == db_purchases[2].id

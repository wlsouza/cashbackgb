from re import S
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas, models
from app.tests.utils.user import random_user_dict
from app.tests.utils.purchase import random_purchase_dict

@pytest.fixture(scope="session")
async def db_user(db:AsyncSession) -> models.User:
    user =  await crud.user.create(db=db, user_in=random_user_dict())
    return user

@pytest.fixture(scope="session")
async def approved_purchase_status(db:AsyncSession) -> models.PurchaseStatus:
    status = await crud.purchase_status.get_by_name(db=db, name="APPROVED")
    if not status:
        status_dict = {
            "name": "APPROVED",
            "description": "Approved status"
        } 
        status = await crud.purchase_status.create(
            db=db, purchase_status_in=status_dict
        )
    return status


@pytest.mark.asyncio
async def test_create_purchase_by_schema(
    db:AsyncSession, db_user:models.User, approved_purchase_status: models.PurchaseStatus
) -> None:
    purchase_dict = random_purchase_dict(user=db_user, status=approved_purchase_status)
    purchase_schema = schemas.PurchaseCreate(**purchase_dict)
    new_purchase = await crud.purchase.create(db=db, purchase_in=purchase_schema)
    assert new_purchase.code == purchase_dict.code


@pytest.mark.asyncio
async def test_create_user_by_dict(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    new_user = await crud.user.create(db=db, user_in=user_dict)
    assert new_user.email == user_dict["email"]


@pytest.mark.asyncio
async def test_when_create_user_return_hashed_password(
    db: AsyncSession,
) -> None:
    user_dict = random_user_dict()
    user_in = schemas.UserCreate(**user_dict)
    new_user = await crud.user.create(db=db, user_in=user_in)
    assert hasattr(new_user, "hashed_password")

@pytest.mark.asyncio
async def test_if_get_by_email_return_correct_user(db: AsyncSession) -> None:
    new_user = await crud.user.create(db=db, user_in=random_user_dict())
    returned_user = await crud.user.get_by_email(
        db=db, email=new_user.email
    )
    assert returned_user.id == new_user.id


@pytest.mark.asyncio
async def test_if_get_by_id_return_correct_user(db: AsyncSession) -> None:
    new_user = await crud.user.create(db=db, user_in=random_user_dict())
    returned_user = await crud.user.get_by_id(db=db, id=new_user.id)
    assert returned_user.id == new_user.id

@pytest.mark.asyncio
async def test_if_get_by_cpf_return_correct_user(db: AsyncSession) -> None:
    new_user = await crud.user.create(db=db, user_in=random_user_dict())
    returned_user = await crud.user.get_by_cpf(db=db, cpf=new_user.cpf)
    assert returned_user.id == new_user.id


@pytest.mark.asyncio
async def test_if_delete_by_id_really_delete_the_user(db: AsyncSession):
    user_dict = random_user_dict()
    new_user = await crud.user.create(db=db, user_in=user_dict)
    await crud.user.delete_by_id(db=db, id=new_user.id)
    returned_user = await crud.user.get_by_id(db=db, id=new_user.id)
    assert returned_user is None


@pytest.mark.asyncio
async def test_update_user_by_userupdateput_schema(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    new_user = await crud.user.create(db=db, user_in=user_dict)
    user_update_in = schemas.UserUpdatePUT(**random_user_dict())
    updated_user = await crud.user.update(
        db=db, db_user=new_user, user_in=user_update_in
    )
    assert updated_user.email == user_update_in.email


@pytest.mark.asyncio
async def test_update_user_by_userupdatepatch_schema(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    new_user = await crud.user.create(db=db, user_in=user_dict)
    user_update_in = schemas.UserUpdatePATCH(email=fake.free_email())
    updated_user = await crud.user.update(
        db=db, db_user=new_user, user_in=user_update_in
    )
    assert updated_user.email == user_update_in.email


@pytest.mark.asyncio
async def test_update_user_by_dict(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    new_user = await crud.user.create(db=db, user_in=user_dict)
    user_update_in = {"email": fake.free_email()}
    updated_user = await crud.user.update(
        db=db, db_user=new_user, user_in=user_update_in
    )
    assert updated_user.email == user_update_in["email"]


@pytest.mark.asyncio
async def test_if_get_multi_return_a_list_of_users(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    users = await crud.user.get_multi(db=db, limit=1)
    assert isinstance(users, list)


@pytest.mark.asyncio
async def test_if_get_multi_return_the_correct_quantity_of_user(
    db: AsyncSession,
) -> None:
    for _ in range(3):
        user_dict = random_user_dict()
        await crud.user.create(db=db, user_in=user_dict)
    users = await crud.user.get_multi(db=db, limit=2)
    assert len(users) == 2


@pytest.mark.asyncio
async def test_if_get_multi_skip_the_correct_quantity_of_user(
    db: AsyncSession,
) -> None:
    for _ in range(3):
        user_dict = random_user_dict()
        await crud.user.create(db=db, user_in=user_dict)
    db_users = await crud.user.get_multi(db=db, limit=5)
    users = await crud.user.get_multi(db=db, skip=2, limit=1)
    assert users[0].id == db_users[2].id
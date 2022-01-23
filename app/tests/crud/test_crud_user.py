import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.core.security import verify_password
from app.tests.utils.user import fake, random_user_dict


@pytest.mark.asyncio
async def test_create_user_by_schema(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    user_in = schemas.UserCreate(**user_dict)
    new_user = await crud.user.create(db=db, user_in=user_in)
    assert new_user.email == user_in.email


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
async def test_when_create_user_return_valid_hashed_password(
    db: AsyncSession,
) -> None:
    user_dict = random_user_dict()
    user_in = schemas.UserCreate(**user_dict)
    new_user = await crud.user.create(db=db, user_in=user_in)
    result = verify_password(user_dict["password"], new_user.hashed_password)
    assert result


@pytest.mark.asyncio
async def test_if_get_by_email_return_correct_user(db: AsyncSession) -> None:
    new_user = await crud.user.create(db=db, user_in=random_user_dict())
    returned_user = await crud.user.get_by_email(db=db, email=new_user.email)
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
    for _ in range(5):
        user_dict = random_user_dict()
        await crud.user.create(db=db, user_in=user_dict)
    db_users = await crud.user.get_multi(db=db, limit=5)
    users = await crud.user.get_multi(db=db, skip=2, limit=1)
    assert users[0].id == db_users[2].id


@pytest.mark.asyncio
async def test_when_successfully_get_authenticated_user_must_return_user(
    db: AsyncSession,
) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    result = await crud.user.get_authenticated_user(
        db=db,
        user_email=user_dict["email"],
        user_password=user_dict["password"],
    )
    assert isinstance(result, models.User)


@pytest.mark.asyncio
async def test_when_getting_authenticated_user_if_invalid_email_must_return_none(
    db: AsyncSession,
) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    result = await crud.user.get_authenticated_user(
        db=db,
        user_email="invalid_email@test.com",
        user_password=user_dict["password"],
    )
    assert result is None


@pytest.mark.asyncio
async def test_when_getting_authenticated_user_if_invalid_password_must_return_none(
    db: AsyncSession,
) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    result = await crud.user.get_authenticated_user(
        db=db,
        user_email=user_dict["email"],
        user_password="invalid_password_test",
    )
    assert result is None

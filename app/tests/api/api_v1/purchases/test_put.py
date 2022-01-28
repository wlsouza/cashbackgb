import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.core.config import settings
from app.tests.utils.auth import (
    get_expired_user_token_headers,
    get_not_active_user_token_headers,
    get_user_token_headers,
)
from app.tests.utils.purchase import (
    create_random_purchase_in_db,
    fake,
    random_purchase_dict_for_json,
)
from app.tests.utils.user import random_user_dict

# region update purchase by id- PUT /purchases/{purchase_id}


@pytest.mark.asyncio
async def test_resource_purchase_id_must_accept_put_verb(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}"
    )
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_when_successfully_update_purchase_by_id_must_return_200(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    payload = random_purchase_dict_for_json(random_purchase.user_)
    headers = get_user_token_headers(random_purchase.user_)
    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_when_successfully_update_purchase_by_id_it_must_be_returned(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    payload = random_purchase_dict_for_json(random_purchase.user_)
    headers = get_user_token_headers(random_purchase.user_)
    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
        json=payload,
    )
    assert response.json().get("code") == payload.get("code")


@pytest.mark.asyncio
async def test_when_successfully_update_purchase_by_id_it_must_be_persisted(
    async_client: AsyncClient,
    db: AsyncSession,
    random_purchase: models.Purchase,
) -> None:
    payload = random_purchase_dict_for_json(random_purchase.user_)
    headers = get_user_token_headers(random_purchase.user_)
    await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
        json=payload,
    )
    # It refresh the purchase in the session because the update was done in
    # another session, so the object in memory of that session is out of date.
    await db.refresh(random_purchase)
    assert random_purchase.code == payload.get("code")


@pytest.mark.asyncio
async def test_when_updating_purchase_by_id_if_purchase_does_not_exist_must_return_404(
    async_client: AsyncClient,
    db: AsyncSession,
    random_purchase: models.Purchase,
) -> None:
    target_id = random_purchase.id
    payload = random_purchase_dict_for_json(random_purchase.user_)
    headers = get_user_token_headers(random_purchase.user_)
    await crud.purchase.delete_by_id(db=db, id=target_id)
    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{target_id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_when_updating_purchase_by_id_if_token_user_is_not_the_same_of_purchase_must_return_403(
    async_client: AsyncClient,
    db: AsyncSession,
    random_purchase: models.Purchase,
) -> None:
    user = await crud.user.create(db=db, user_in=random_user_dict())
    headers = get_user_token_headers(user)
    payload = random_purchase_dict_for_json(random_purchase.user_)
    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_purchase_by_id_if_purchase_status_is_not_in_validation_must_return_403(
    async_client: AsyncClient,
    db: AsyncSession,
    random_purchase: models.Purchase,
) -> None:

    await crud.purchase.update(
        db=db,
        db_purchase=random_purchase,
        purchase_in={"status": schemas.statusEnum.APPROVED},
    )
    payload = random_purchase_dict_for_json(random_purchase.user_)
    headers = get_user_token_headers(random_purchase.user_)
    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_purchase_by_id_if_purchase_cpf_will_be_changed_must_return_403(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    payload = random_purchase_dict_for_json(random_purchase.user_) | {
        "cpf": fake.cpf()
    }
    headers = get_user_token_headers(random_purchase.user_)
    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_purchase_by_id_if_purchase_code_has_already_been_used_must_return_403(
    async_client: AsyncClient,
    db: AsyncSession,
    random_purchase: models.Purchase,
) -> None:
    user = await crud.user.create(db=db, user_in=random_user_dict())
    new_purchase = await create_random_purchase_in_db(db=db, user=user)
    payload = random_purchase_dict_for_json(random_purchase.user_) | {
        "code": new_purchase.code
    }
    headers = get_user_token_headers(random_purchase.user_)

    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_purchase_by_id_if_token_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    payload = random_purchase_dict_for_json(random_purchase.user_)
    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        json=payload,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_updating_purchase_by_id_if_token_is_expired_must_return_403(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    payload = random_purchase_dict_for_json(random_purchase.user_)
    headers = get_expired_user_token_headers(random_purchase.user_)
    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_purchase_by_id_if_token_is_not_active_yet_must_return_403(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    payload = random_purchase_dict_for_json(random_purchase.user_)
    headers = get_not_active_user_token_headers(random_purchase.user_)
    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_purchase_by_id_if_body_is_not_valid_must_return_422(
    async_client: AsyncClient, random_purchase: models.Purchase
) -> None:
    payload = {"invalid": "body"}
    headers = get_user_token_headers(random_purchase.user_)
    response = await async_client.put(
        f"{settings.API_V1_STR}/purchases/{random_purchase.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# endregion

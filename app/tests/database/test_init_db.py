from unittest import mock

import pytest

from app.database.init_db import init_db

@pytest.mark.asyncio
@mock.patch("app.database.init_db.crud.purchase_status.create")
@mock.patch("app.database.init_db.crud.purchase_status.get_by_name")
async def test_when_call_init_db_if_initial_statuses_does_not_exist_created_method_must_be_called(
    mocked_get_by_name, mocked_create
) -> None:
    # mock setup
    mocked_get_by_name.return_value = None
    # assert
    await init_db(db=mock.Mock())
    assert mocked_create.call_count == 3


@pytest.mark.asyncio
@mock.patch("app.database.init_db.crud.purchase_status.create")
@mock.patch("app.database.init_db.crud.purchase_status.get_by_name")
async def test_when_call_init_db_if_initial_statuses_already_exist_created_method_must_not_be_called(
    mocked_get_by_name, mocked_create
) -> None:
    # assert
    await init_db(db=mock.Mock())
    assert mocked_create.call_count == 0
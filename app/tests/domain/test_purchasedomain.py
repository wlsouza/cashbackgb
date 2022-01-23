import pytest
from unittest import mock
from decimal import Decimal
from random import randrange

from app import domain, crud


def test_calculate_cashback_with_value_lower_than_1000_must_return_10_percent():
    purchase_value = Decimal(randrange(100001))/100
    expected_value = purchase_value * Decimal(0.1)
    cashback_value = domain.purchase.calculate_cashback(
        purchase_value=purchase_value
    )
    assert cashback_value == expected_value

def test_calculate_cashback_with_value_between_1000_and_1500_must_return_15_percent():
    purchase_value = Decimal(randrange(100001,150001))/100
    expected_value = purchase_value * Decimal(0.15)
    cashback_value = domain.purchase.calculate_cashback(
        purchase_value=purchase_value
    )
    assert cashback_value == expected_value

def test_calculate_cashback_with_value_upper_then_15000_must_return_15_percent():
    purchase_value = Decimal(randrange(150001, 500000))/100
    expected_value = purchase_value * Decimal(0.20)
    cashback_value = domain.purchase.calculate_cashback(
        purchase_value=purchase_value
    )
    assert cashback_value == expected_value

@pytest.mark.asyncio
@mock.patch.object(crud.user,"get_by_id")
@mock.patch.object(crud.purchase_status,"get_by_name")
async def test_get_default_purchase_status_id_when_cpf_is_15350946056_must_return_the_id_of_approved_purchase_status(
    mocked_purchase_status_get_by_name,
    mocked_user_get_by_id
):
    # Mocking the cpf returned by crud.user.get_by_id
    mocked_user_get_by_id.return_value.cpf = "15350946056"
    arg_mock = mock.Mock()
    await domain.purchase.get_default_purchase_status_id(
        db=arg_mock, purchase_user_id=arg_mock
    )
    # asserting if the method was called with "Approved"
    mocked_purchase_status_get_by_name.assert_awaited_with(db=arg_mock, name="Approved")
    

@pytest.mark.asyncio
@mock.patch.object(crud.user,"get_by_id")
@mock.patch.object(crud.purchase_status,"get_by_name")
async def test_get_default_purchase_status_id_when_cpf_is_not_15350946056_must_return_the_id_of_in_validation_purchase_status(
    mocked_purchase_status_get_by_name,
    mocked_user_get_by_id
):
    # Mocking the cpf returned by crud.user.get_by_id
    mocked_user_get_by_id.return_value.cpf = "99999999999"
    arg_mock = mock.Mock()
    await domain.purchase.get_default_purchase_status_id(
        db=arg_mock, purchase_user_id=arg_mock
    )
    # asserting if the method was called with "In validation"
    mocked_purchase_status_get_by_name.assert_awaited_with(db=arg_mock, name="In validation")
    
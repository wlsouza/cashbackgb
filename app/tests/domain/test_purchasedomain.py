from decimal import Decimal
from random import randrange

from app import domain

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
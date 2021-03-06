import random
from decimal import Decimal
from typing import Any, Dict

import pytest

from app import domain, schemas
from app.tests.utils.purchase import fake


@pytest.fixture
def random_purchase_dict() -> Dict[str, Any]:
    value = Decimal(random.randrange(100, 200000)) / 100
    cashback_value = domain.purchase.calculate_cashback(purchase_value=value)
    purchase_dict = {
        "id": fake.random_int(),
        "code": fake.uuid4(),
        "value": value,
        "status": fake.word(),
        "date": fake.date(),
        "cpf": fake.cpf(),
        "cashback_value": cashback_value,
    }
    return purchase_dict


def test_purchase_schema_if_cashback_percent_is_not_passed_it_must_be_calculated(
    random_purchase_dict: Dict[str, Any]
):
    purchase_schema = schemas.Purchase(**random_purchase_dict)
    expected = round(
        purchase_schema.cashback_value / purchase_schema.value * 100
    )
    assert purchase_schema.cashback_percent == expected


def test_purchase_schema_if_cashback_percent_is_passed_it_must_returned(
    random_purchase_dict: Dict[str, Any]
):
    expected = random.randint(1, 20)
    purchase_schema = schemas.Purchase(
        **random_purchase_dict, cashback_percent=expected
    )
    assert purchase_schema.cashback_percent == expected

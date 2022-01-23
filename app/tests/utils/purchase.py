from decimal import Decimal
from random import randrange
from typing import Dict, Union

from faker import Faker

from app import models

fake = Faker("pt_BR")

# receives the object from the entire bank to ensure that the dev will
# create the object and not pass a random integer.
def random_purchase_dict(
    user: models.User,
) -> Dict[str, Union[str, Decimal]]:
    user_dict = {
        "code": fake.lexify(),
        "value": Decimal(randrange(200000)) / 100,
        "date": fake.date_object(),
        "cpf": user.cpf,
    }
    return user_dict

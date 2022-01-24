import random
from decimal import Decimal
from typing import Dict, Union

from faker import Faker

from app import models

fake = Faker("pt_BR")

# receives the object from the entire bank to ensure that the dev will
# create the object and not pass a random integer.
def random_purchase_dict_for_crud(
    user: models.User,
) -> Dict[str, Union[str, Decimal]]:
    user_dict = {
        "code": fake.uuid4(),
        "value": Decimal(random.randrange(100, 200000))/100,
        "date": fake.date_object(),
        "cpf": user.cpf,
    }
    return user_dict

def random_purchase_dict_for_json(
    user: models.User,
) -> Dict[str, Union[str, float]]:
    user_dict = {
        "code": fake.uuid4(),
        "value": round(random.uniform(0, 2500),2),
        "date": fake.date(),
        "cpf": user.cpf,
    }
    return user_dict
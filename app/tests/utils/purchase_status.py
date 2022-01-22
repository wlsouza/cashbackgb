from typing import Dict

from faker import Faker

fake = Faker()


def random_purchase_status_dict() -> Dict[str, str]:
    user_dict = {
        "name": fake.word(),
        "description": fake.sentence(),
    }
    return user_dict
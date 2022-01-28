from typing import Dict

from faker import Faker

fake = Faker("pt_BR")


def random_user_dict() -> Dict[str, str]:
    user_dict = {
        "full_name": fake.name(),
        "email": fake.free_email(),
        "cpf": fake.ssn(),
        "password": fake.password(length=12),
    }
    return user_dict

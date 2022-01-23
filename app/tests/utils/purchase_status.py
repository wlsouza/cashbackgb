from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from app import models, crud

fake = Faker()


def random_purchase_status_dict() -> Dict[str, str]:
    user_dict = {
        "name": fake.word(),
        "description": fake.sentence(),
    }
    return user_dict

def in_validation_status_dict():
    return {
        "name": "In validation",
        "description": "In validation status"
    }

def approved_status_dict():
    return {
        "name": "Approved",
        "description": "Approved status"
    }

def disapproved_status_dict():
    return {
        "name": "Disapproved",
        "description": "Disapproved status"
    }


async def create_purchase_status_in_db(db:AsyncSession, name:str) -> models.PurchaseStatus:
    status = await crud.purchase_status.get_by_name(db=db, name=name)
    if not status:
        status = await crud.purchase_status.create(
            db=db, purchase_status_in={"name": name, "description": name}
        )
    return status
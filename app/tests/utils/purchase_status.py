from typing import Dict

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models

fake = Faker()


def random_purchase_status_dict() -> Dict[str, str]:
    user_dict = {
        "name": fake.word(),
        "description": fake.sentence(),
    }
    return user_dict

async def create_purchase_status_in_db(
    db: AsyncSession, name: str
) -> models.PurchaseStatus:
    status = await crud.purchase_status.get_by_name(db=db, name=name)
    if not status:
        status = await crud.purchase_status.create(
            db=db, purchase_status_in={"name": name, "description": name}
        )
    return status

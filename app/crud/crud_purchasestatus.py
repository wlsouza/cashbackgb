from typing import Union, Optional, List, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


class CrudPurchaseStatus:

    async def create(
        self,
        db:AsyncSession,
        purchase_status_in: Dict[str, Any]
    ) -> models.PurchaseStatus:
        ps_data = purchase_status_in.copy()
        db_purchase_status = models.PurchaseStatus(**ps_data)
        db.add(db_purchase_status)
        await db.commit()
        await db.refresh(db_purchase_status)
        return db_purchase_status

    async def get_by_id(
        self, db:AsyncSession, id: Union[int, str]
    ) -> Optional[models.PurchaseStatus]:
        result = await db.execute(
            select(models.PurchaseStatus)
            .where(models.PurchaseStatus.id == id)
        )
        return result.scalar()

    async def get_by_name(
        self, db:AsyncSession, name: str
    ) -> Optional[models.PurchaseStatus]:
        result = await db.execute(
            select(models.PurchaseStatus)
            .where(models.PurchaseStatus.name == name)
        )
        return result.scalar()


purchase_status = CrudPurchaseStatus()
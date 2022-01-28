from typing import Any, Dict, List, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, domain, models, schemas


class CrudPurchase:
    async def get_by_id(
        self, db: AsyncSession, id: Union[int, str]
    ) -> Optional[models.Purchase]:
        result = await db.execute(
            select(models.Purchase).where(models.Purchase.id == id)
        )
        return result.scalar()

    async def get_by_code(
        self, db: AsyncSession, code: Union[int, str]
    ) -> Optional[models.Purchase]:
        result = await db.execute(
            select(models.Purchase).where(models.Purchase.code == code)
        )
        return result.scalar()

    async def get_multi(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Optional[List[models.Purchase]]:
        result = await db.execute(
            select(models.Purchase).offset(skip).limit(limit)
        )
        return result.scalars().unique().all()

    async def get_multi_by_user_id(
        self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
    ) -> Optional[List[models.Purchase]]:
        result = await db.execute(
            select(models.Purchase)
            .where(models.Purchase.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().unique().all()

    async def create(
        self,
        db: AsyncSession,
        purchase_in: Union[schemas.PurchaseCreate, Dict[str, Any]],
    ) -> models.Purchase:
        if isinstance(purchase_in, dict):
            create_data = purchase_in.copy()
        else:
            create_data = purchase_in.dict()

        # treats the dictionary to insert the user_id instead of the cpf.
        if create_data.get("cpf"):
            user = await crud.user.get_by_cpf(
                db=db, cpf=create_data.pop("cpf")
            )
            create_data["user_id"] = user.id

        # treats the dictionary to insert the status_id.
        if not create_data.get("status_id"):
            if create_data.get("status"):
                # treats the dictionary to insert the status_id instead
                # of the name.
                status = await crud.purchase_status.get_by_name(
                    db=db, name=create_data.pop("status")
                )
                create_data["status_id"] = status.id
            else:
                # get default domain status
                status_id = (
                    await domain.purchase.get_default_purchase_status_id(
                        db=db, purchase_user_id=create_data.get("user_id")
                    )
                )
                create_data["status_id"] = status_id

        # apply cashback business rule because PurchaseCreate schema
        # don't have this value.
        if not create_data.get("cashback_value"):
            cashback_value = domain.purchase.calculate_cashback(
                purchase_value=create_data.get("value")
            )
            create_data["cashback_value"] = cashback_value

        db_purchase = models.Purchase(**create_data)
        db.add(db_purchase)
        await db.commit()
        await db.refresh(db_purchase)
        return db_purchase

    async def update(
        self,
        db: AsyncSession,
        db_purchase: models.Purchase,
        purchase_in: Union[
            schemas.PurchaseUpdatePUT,
            schemas.PurchaseUpdatePATCH,
            Dict[str, Any],
        ],
    ) -> models.Purchase:
        if isinstance(purchase_in, dict):
            update_data = purchase_in.copy()
        elif isinstance(purchase_in, schemas.PurchaseUpdatePUT):
            update_data = purchase_in.dict()
        else:
            update_data = purchase_in.dict(exclude_unset=True)

        # treats the dictionary to insert the user_id instead of the cpf.
        if update_data.get("cpf"):
            user = await crud.user.get_by_cpf(
                db=db, cpf=update_data.pop("cpf")
            )
            update_data["user_id"] = user.id

        # treats the dictionary to insert the status_id instead of the name.
        if update_data.get("status") and not update_data.get("status_id"):
            status = await crud.purchase_status.get_by_name(
                db=db, name=update_data.pop("status")
            )
            update_data["status_id"] = status.id

        # apply cashback business rule because PurchaseUpdate
        # schema don't have this value.
        if not update_data.get("cashback_value") and update_data.get("value"):
            cashback_value = domain.purchase.calculate_cashback(
                purchase_value=update_data.get("value")
            )
            update_data["cashback_value"] = cashback_value

        for field, value in update_data.items():
            if hasattr(db_purchase, field):
                setattr(db_purchase, field, value)
        await db.commit()
        await db.refresh(db_purchase)
        return db_purchase

    async def delete_by_id(
        self, db: AsyncSession, id: Union[int, str]
    ) -> Optional[models.Purchase]:
        purchase = await self.get_by_id(db=db, id=id)
        if not purchase:
            return None
        await db.delete(purchase)
        await db.commit()
        return purchase


purchase = CrudPurchase()

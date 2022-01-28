from sqlalchemy.ext.asyncio import AsyncSession

from app import crud


async def init_db(db: AsyncSession) -> None:
    # add initial status

    basic_names = ["Approved", "In validation", "Disapproved"]
    for status_name in basic_names:
        status = await crud.purchase_status.get_by_name(
            db=db, name=status_name
        )
        if not status:
            status = await crud.purchase_status.create(
            db=db, purchase_status_in={
                "name": status_name, 
                "description": status_name
            }
        )
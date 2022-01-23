from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud


class PurchaseDomain:
    """
    Class responsible for purchasing business rules

    """

    # I'm forcing the dev to use named argument to avoid errors
    def calculate_cashback(self, *, purchase_value: Decimal) -> Decimal:
        """
        Method that calculates cashback given the purchase value.
        Rule:
            - For purchases worth up to 1000 BRL the cashback will be 10%.
            - For purchases with a value between 1000 and 1500 BRL the cashback will be 15%.
            - For purchases over 1500 BRL the cashback will be 20%.

        Args:
            purchase_value (Decimal): Value of purchase.

        Returns:
            Decimal: Calculated cashback.
        """
        if purchase_value <= 1000:
            return purchase_value * Decimal(0.1)
        if purchase_value <= 1500:
            return purchase_value * Decimal(0.15)
        return purchase_value * Decimal(0.2)

    async def get_default_purchase_status_id(
        self, db: AsyncSession, *, purchase_user_id: int
    ) -> int:
        """
        Method that get correct default purchase status for a new purchase.
        Rule:
            - Every new purchase must have the status "In validation", except
            when the user's CPF is '15350946056', in this case the status
            must be "Approved"
        Args:
            purchase_user_id (int): id of purchase user.
            db (AsyncSession): Database async session.

        Returns:
            int: id of status.
        """
        user = await crud.user.get_by_id(db=db, id=purchase_user_id)
        if user.cpf == "15350946056":
            status = await crud.purchase_status.get_by_name(
                db=db, name="Approved"
            )
        else:
            status = await crud.purchase_status.get_by_name(
                db=db, name="In validation"
            )
        return status.id


purchase = PurchaseDomain()

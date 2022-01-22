from decimal import Decimal

class PurchaseDomain:
    """
    Class responsible for purchasing business rules

    """

    # I'm forcing the dev to use named argument to avoid errors
    def calculate_cashback(self, *, purchase_value:Decimal) -> Decimal:
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


purchase = PurchaseDomain()
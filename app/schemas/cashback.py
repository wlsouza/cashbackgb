from pydantic import BaseModel


# Properties to return to client
class CashBack(BaseModel):
    cashback: float

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class statusEnum(str, Enum):
    APPROVED = "Approved"
    IN_VALIDATION = "In validation"
    DISAPPROVED = "Disapproved"


# Shared properties
class PurchaseBase(BaseModel):
    code: str
    value: Decimal
    date: date


# Properties to receive via API on creation
class PurchaseCreate(PurchaseBase):
    cpf: str


# Properties to receive via API on update -- PATCH (allows not filling all fields)
class PurchaseUpdatePATCH(PurchaseBase):
    code: Optional[str] = None
    value: Optional[Decimal] = None
    date: Optional[date] = None
    status: Optional[statusEnum] = None
    cpf: Optional[str] = None

    class Config:
        extra = "forbid"


# Properties to receive via API on update -- PUT (force fill all fields)
class PurchaseUpdatePUT(PurchaseBase):
    status: statusEnum
    cpf: str

    class Config:
        extra = "forbid"


# Properties shared by models stored in DB
class PurchaseInDBBase(PurchaseBase):
    id: int
    cashback_value: Decimal

    class Config:
        orm_mode = True


# Properties to return to client
class Purchase(PurchaseInDBBase):
    status: statusEnum
    cpf: str
    cashback_value: Decimal


# Properties properties stored in DB
class PurchaseInDB(PurchaseInDBBase):
    user_id: int
    status_id: int

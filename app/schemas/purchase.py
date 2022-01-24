from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional, Any, Set

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
    status: str
    cpf: str
    cashback_value: Decimal

    #I would really rather bring a separate object (ex: status = {
    # "id": 1, "name": "In Validation", "description": "In validation status"
    # }) than making status name as purchase status , but as the challenge
    # indicates that the status should be "In Validation" I understand that 
    # I should make the object flat.
    #override from_orm to fill correctly the status and cpf
    @classmethod
    def from_orm(cls, obj: Any):
        # "obj" is the orm model instance
        if hasattr(obj, "status_"):
            setattr(obj, "status", obj.status_.name)
        if hasattr(obj, "user_"):
            setattr(obj, "cpf", obj.user_.cpf)
        # create schema
        schema = super().from_orm(obj)
        # remove setted attributes
        delattr(obj, "status")
        delattr(obj, "cpf")
        return schema


# Properties properties stored in DB
class PurchaseInDB(PurchaseInDBBase):
    user_id: int
    status_id: int

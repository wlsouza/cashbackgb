from typing import Optional

from pydantic import BaseModel, EmailStr, validator

# from validate_docbr import CPF

# cpf = CPF()


# Shared properties
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    cpf: str

    # @validator("cpf")
    # def validate_cpf(cls, v):
    #     if not cpf.validate(v):
    #         ValueError('Invalid CPF')
    #     return v



# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update -- PATCH (allows not filling all fields)
class UserUpdatePATCH(UserBase):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    password: Optional[str] = None

    class Config:
        extra = "forbid"


# Properties to receive via API on update -- PUT (force fill all fields)
class UserUpdatePUT(UserBase):
    full_name: str
    email: EmailStr
    cpf: str
    password: str

    class Config:
        extra = "forbid"


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str

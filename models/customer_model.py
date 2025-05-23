from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel,Field

class CustomerBase(SQLModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

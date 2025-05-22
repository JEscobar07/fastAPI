from pydantic import BaseModel, EmailStr

class CustomerBase(BaseModel):
    name: str
    age: int
    description: str | None
    email: EmailStr

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int | None = None

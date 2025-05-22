from pydantic import BaseModel

class Transaction(BaseModel):
    id: int
    amount: float
    description: str
    
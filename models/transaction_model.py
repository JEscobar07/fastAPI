from pydantic import BaseModel
from 

class Transaction(BaseModel):
    id: int
    amount: float
    description: str
    
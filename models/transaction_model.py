from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel,Field

class Transaction(SQLModel):
    id: Optional[int] 
    amount: float 
    description: str
    
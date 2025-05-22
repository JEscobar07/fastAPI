from pydantic import BaseModel
from typing import List
from models.customer_model import Customer
from models.transaction_model import Transaction

class Invoice (BaseModel):
    id: int
    customer : Customer
    transactions : List[Transaction]
    total:int

    @property    
    def ammount_total(self):
        return sum(transaction.amount for transaction in self.transactions)

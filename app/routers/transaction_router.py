from fastapi import APIRouter
from models.transaction_model import Transaction

router = APIRouter(tags=['transactions'])

@router.post('/')
async def create_transaction(transaction: Transaction):
    return transaction

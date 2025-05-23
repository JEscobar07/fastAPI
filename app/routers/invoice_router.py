from fastapi import APIRouter
from models.invoice_model import Invoice

router = APIRouter(tags=['invoices'])

@router.post('/')
async def create_invoice(invoice: Invoice):
    return invoice

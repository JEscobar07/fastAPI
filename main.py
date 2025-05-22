import zoneinfo
from fastapi import FastAPI,status,HTTPException
from datetime import datetime
from data.db import SessionDep, create_all_tables
from models.customer_model import Customer 
from models.customer_model import CustomerCreate
from models.transaction_model import Transaction
from models.invoice_model import Invoice
from typing import List

# Parametro que indica que ejecute un metodo al inicio y al final de la aplicacion
myapp = FastAPI(lifespan=create_all_tables)

@myapp.get('/')

async def myfirst():
    return {'message': 'Hello world'}

@myapp.get('/time')
async def time():
    return {"time":datetime.now()}

country_timezones = {
    'CO': 'America/Bogota',
    'MX': 'America/Mexico_City',
    'AR': 'America/Argentina/Buenos_Aires',
    'BR': 'America/Sao_Paulo',
    'PE': 'America/Lima'
}


@myapp.get('/time/{iso_code}')
async def time(iso_code : str):
    iso = iso_code.upper()
    timezone = country_timezones.get(iso)
    if( timezone == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lo sentimos pero el {iso} no existe")

    tz = zoneinfo.ZoneInfo(timezone)
    return {"time": datetime.now(tz)}

db_customers:List[Customer] = []

@myapp.get('/customers', response_model=List[Customer])
async def return_all_customers():
    return db_customers

@myapp.get('/customers/{id}',response_model=Customer)
async def return_id_customer(id: int):
    for c in db_customers:
        if (c.id == id):
            return c
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'El customer con el id: {id} no existe')

@myapp.post('/customers', response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    customer.id = len(db_customers) + 1
    db_customers.append(customer)
    return customer


@myapp.post('/transactions')
async def create_transaction(transaction: Transaction):
    return transaction

@myapp.post('/invoices')
async def create_invoice(invoice: Invoice):
    return invoice

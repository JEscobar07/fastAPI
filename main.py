import zoneinfo
from fastapi import FastAPI,status,HTTPException
from datetime import datetime
from data.db import SessionDep, create_all_tables
from models.customer_model import Customer,CustomerCreate,CustomerUpdate
from models.transaction_model import Transaction
from models.invoice_model import Invoice
from typing import List
from sqlmodel import select

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
async def return_all_customers(session: SessionDep):
    # Ejecuta transacciones SQL
    return session.exec(select(Customer)).all() #devuelve una lista
     

@myapp.get('/customers/{id}',response_model=Customer)
async def return_id_customer(id: int,session: SessionDep):
    # customer = session.exec(select(Customer).where(id == Customer.id)).first()
    customer = session.get(Customer,id)
    if customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'El customer con el id: {id} no existe')
    return  customer
    # if != None:
    #     return session.exec(select(Customer).where(id == Customer.id))
    # 
    # for c in db_customers:
    #     if (c.id == id):
    #         return c
    
@myapp.post('/customers', response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    # agregar, confirmar y refrescar la variable por que necesitamos que el customer genere el id
    session.add(customer)
    session.commit()
    session.refresh(customer)
    # customer.id = len(db_customers) + 1
    # db_customers.append(customer)
    return customer

@myapp.delete('/customers/{id}')
async def delete_customer(id: int, session: SessionDep):
    customer = session.get(Customer, id)
    if customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"el customer con el id : {id} no se encuentra en la base de datos")
    session.delete(customer)
    session.commit()
    return {"message":f"El customer con el id: {id} ha sido eliminado con exito"}

@myapp.put('/customers/{id}', response_model=CustomerCreate)
async def put_customer(id: int,body: CustomerUpdate, session: SessionDep):
    
    customer_db = session.get(Customer, id)
    
    if customer_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El customer con el id: {id} no se encuentra en la base de datos")
    
    update_data = body.model_dump()

    # Version nueva
    customer_db.sqlmodel_update(update_data)
    # Version vieja
    # for key,value in update_data.items():
    #     setattr(customer_db, key,value)

    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)

    return customer_db

@myapp.patch('/Customers/{id}', response_model=Customer, status_code=status.HTTP_201_CREATED)
def patch_customer(id: int , body: CustomerUpdate, session: SessionDep):

    customer_db = session.get(Customer,id)
    if customer_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"El customer con el id: {id} no se encuentra en la BD")
    
    # Obtener solo los campos que envió el cliente
    customer_data = body.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@myapp.post('/transactions')
async def create_transaction(transaction: Transaction):
    return transaction

@myapp.post('/invoices')
async def create_invoice(invoice: Invoice):
    return invoice

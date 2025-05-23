from typing import List
from fastapi import APIRouter,HTTPException,status
from models.customer_model import Customer,CustomerCreate,CustomerUpdate
from data.db import SessionDep
from sqlmodel import select

router = APIRouter(tags=['customers'])

@router.get('/', response_model=List[Customer])
async def return_all_customers(session: SessionDep):
    # Ejecuta transacciones SQL
    return session.exec(select(Customer)).all() #devuelve una lista
     

@router.get('/{id}',response_model=Customer)
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
    
@router.post('/', response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    # agregar, confirmar y refrescar la variable por que necesitamos que el customer genere el id
    session.add(customer)
    session.commit()
    session.refresh(customer)
    # customer.id = len(db_customers) + 1
    # db_customers.append(customer)
    return customer

@router.delete('/{id}')
async def delete_customer(id: int, session: SessionDep):
    customer = session.get(Customer, id)
    if customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"el customer con el id : {id} no se encuentra en la base de datos")
    session.delete(customer)
    session.commit()
    return {"message":f"El customer con el id: {id} ha sido eliminado con exito"}

@router.put('/{id}', response_model=CustomerCreate)
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

@router.patch('/{id}', response_model=Customer, status_code=status.HTTP_201_CREATED)
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
import zoneinfo
from fastapi import FastAPI,status,HTTPException
from datetime import datetime
from data.db import create_all_tables
from app.routers import customer_router,invoice_router,transaction_router


# Parametro que indica que ejecute un metodo al inicio y al final de la aplicacion
myapp = FastAPI(lifespan=create_all_tables)
myapp.include_router(prefix='/customers',router=customer_router.router)
myapp.include_router(prefix='/transactions',router=transaction_router.router)
myapp.include_router(prefix='/invoices',router=invoice_router.router)

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






from typing import Annotated
from fastapi import Depends,FastAPI
from sqlmodel import Session, create_engine,SQLModel

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

# Este es el motor
engine = create_engine(sqlite_url)

# Para verificar que la bd si tenga las tablas
def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

# Obtener una nueva sesion de BD
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
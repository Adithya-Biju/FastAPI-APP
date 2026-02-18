from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
import app.models
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings

sqlaclhemy_database_url = settings.database

#Prod settings 
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

engine = create_engine(sqlaclhemy_database_url)
SessionDep = Annotated[Session, Depends(get_session)]

#Test settings
def create_test_db_and_tables():
    SQLModel.metadata.create_all(engine_test)

def get_test_session():
    with Session(engine_test) as session:
        yield session

sqlaclhemy_test_database_url = settings.database+"_test"
engine_test = create_engine(sqlaclhemy_test_database_url)

@asynccontextmanager
async def lifespan(app: FastAPI):

    create_db_and_tables()
    print("Database connection successfully established")

    yield
    print("Closing resources")
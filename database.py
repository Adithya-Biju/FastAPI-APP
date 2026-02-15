from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
import models
from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import settings

sqlaclhemy_database_url = settings.database

engine = create_engine(sqlaclhemy_database_url)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):

    # create_db_and_tables()
    print("Database connection successfully established")

    yield
    print("Closing resources")
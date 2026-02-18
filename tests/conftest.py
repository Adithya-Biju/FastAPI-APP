import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.main import app
from app.database import get_session
from app.config import settings
from fastapi.testclient import TestClient


sqlaclhemy_test_database_url = settings.database + "_test"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(sqlaclhemy_test_database_url)
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
import pytest
from sqlmodel import select, Session
from fastapi.testclient import TestClient
from app.models import User
from app.schema import UserCreate

@pytest.fixture
def create_user_fixture(client: TestClient):
    user_data = UserCreate(email="test123@gmail.com", password="test123")
    res = client.post("/users/", json=user_data.model_dump())
    
    return {
        "response": res,
        "original_data": user_data,
        "json": res.json()
    }

def test_user_creation_and_db_persistence(session: Session, create_user_fixture):
    res = create_user_fixture["response"]
    user_json = create_user_fixture["json"]
    original_data = create_user_fixture["original_data"]


    assert res.status_code == 201
    assert user_json["email"] == "test123@gmail.com"
    assert "password" not in user_json 
    assert "id" in user_json            

    statement = select(User).where(User.email == original_data.email)
    db_user = session.exec(statement).first()

    assert db_user is not None
    assert db_user.email == original_data.email
    assert db_user.password != original_data.password
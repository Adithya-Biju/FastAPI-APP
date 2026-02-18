from sqlmodel import Session
from fastapi.testclient import TestClient
from app.schema import Token
from tests.routes.test_user import create_user_fixture

def test_login(client: TestClient, create_user_fixture):

    user_data = create_user_fixture["original_data"]

    res = client.post("/login",data={
        "username": user_data.email,
        "password": user_data.password
    })

    assert res.status_code ==  200

    token_data = Token(**res.json())
    
    assert token_data.access_token is not None
    assert token_data.token_type == "bearer"
    assert "access_token" in res.json()
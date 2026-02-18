from fastapi.testclient import TestClient
from sqlmodel import Session

def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("message") == "Health check successful"

def test_root_not_found(client: TestClient):
    response = client.get("/this-route-does-not-exist")
    assert response.status_code == 404

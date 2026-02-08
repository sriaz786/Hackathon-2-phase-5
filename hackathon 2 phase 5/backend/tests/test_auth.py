from fastapi.testclient import TestClient
from app.core.config import settings

def test_signup(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data

def test_login(client: TestClient):
    # First create user
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "email": "login@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }
    )
    
    # Then login
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "login@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

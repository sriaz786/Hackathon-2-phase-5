from fastapi.testclient import TestClient
from app.core.config import settings

def get_auth_token(client: TestClient, email: str = "todo@example.com", password: str = "password123") -> str:
    # Signup
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "email": email,
            "password": password,
            "confirm_password": password
        }
    )
    # Login
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": email,
            "password": password
        }
    )
    return response.json()["access_token"]

def test_create_todo(client: TestClient):
    token = get_auth_token(client)
    response = client.post(
        f"{settings.API_V1_STR}/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Todo", "description": "Test Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["status"] == "pending"

def test_read_todos(client: TestClient):
    token = get_auth_token(client)
    # Create a todo
    client.post(
        f"{settings.API_V1_STR}/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Todo"}
    )
    
    response = client.get(
        f"{settings.API_V1_STR}/todos/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Test Todo"

def test_update_todo(client: TestClient):
    token = get_auth_token(client)
    # Create a todo
    create_res = client.post(
        f"{settings.API_V1_STR}/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Old Title"}
    )
    todo_id = create_res.json()["id"]
    
    response = client.put(
        f"{settings.API_V1_STR}/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "New Title", "status": "completed"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["status"] == "completed"

def test_delete_todo(client: TestClient):
    token = get_auth_token(client)
    # Create a todo
    create_res = client.post(
        f"{settings.API_V1_STR}/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "To Delete"}
    )
    todo_id = create_res.json()["id"]
    
    response = client.delete(
        f"{settings.API_V1_STR}/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
    # Verify it's gone
    get_res = client.get(
        f"{settings.API_V1_STR}/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_res.status_code == 404

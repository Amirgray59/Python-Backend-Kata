import pytest
from httpx import AsyncClient
import uuid

@pytest.mark.asyncio
async def test_create_user(async_client):
    email = f"test@{uuid.uuid4()}.com"
    payload = {"name": "test", "email": email}
    
    response = await async_client.post("/users", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test"
    assert data["email"] == email
    assert "id" in data

@pytest.mark.asyncio
async def test_all_users(async_client):
    email = f"test@{uuid.uuid4()}.com"
    payload = {"name": "test", "email": email}
    await async_client.post("/users", json=payload)

    response = await async_client.get("/users")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) >= 1
    
    for user in data:
        assert "id" in user
        assert "name" in user
        assert "email" in user

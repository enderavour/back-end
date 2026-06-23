import uuid
import pytest


def unique_email(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4()}@test.com"


def unique(prefix: str):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


@pytest.mark.anyio
async def test_create_user(client):
    email = f"{uuid.uuid4()}@test.com"
    username = unique("user")

    response = await client.post(
        "/users/",
        json={
            "email": email,
            "username": username,
            "password": "12345678",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email


@pytest.mark.anyio
async def test_get_users(client):
    response = await client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)





@pytest.mark.anyio
async def test_get_user_not_found(client):
    response = await client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User Not Found"

@pytest.mark.anyio
async def test_users_pagination(client):
    response = await client.get("/users/?skip=0&limit=5")
    assert response.status_code == 200

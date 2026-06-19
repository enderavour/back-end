import pytest


@pytest.mark.anyio
async def test_create_user(client):
    response = await client.post(
        "/users/",
        json={
            "email": "test@test.com",
            "username": "test",
            "password": "12345678",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test@test.com"
    assert "password" not in data


@pytest.mark.anyio
async def test_get_users(client):
    response = await client.get("/users/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_user_by_id(client):
    create = await client.post(
        "/users/",
        json={
            "email": "one@test.com",
            "username": "one",
            "password": "12345678",
        },
    )

    user_id = create.json()["id"]

    response = await client.get(f"/users/{user_id}")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_user_not_found(client):
    response = await client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User Not Found"


@pytest.mark.anyio
async def test_update_user(client):
    create = await client.post(
        "/users/",
        json={
            "email": "update@test.com",
            "username": "old",
            "password": "12345678",
        },
    )

    user_id = create.json()["id"]

    response = await client.patch(
        f"/users/{user_id}",
        json={"username": "updated"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["username"] == "updated"


@pytest.mark.anyio
async def test_delete_user(client):
    create = await client.post(
        "/users/",
        json={
            "email": "delete@test.com",
            "username": "delete",
            "password": "12345678",
        },
    )

    user_id = create.json()["id"]

    response = await client.delete(f"/users/{user_id}")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_users_pagination(client):
    response = await client.get("/users/?skip=0&limit=5")

    assert response.status_code == 200

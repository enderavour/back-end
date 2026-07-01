import uuid
import pytest
from app.core.security import create_access_token, decode_token
from app.schemas.user import SignUpRequest
from app.services.user import UserService


def test_create_access_token():
    token = create_access_token({"sub": "1"})

    assert token is not None
    assert isinstance(token, str)


def test_decode_token():
    token = create_access_token({"sub": "1"})

    payload = decode_token(token)

    assert payload["sub"] == "1"


@pytest.mark.asyncio
async def test_create_auth0_user(db_session):
    uid = uuid.uuid4().hex

    email = f"{uid}@test.com"
    username = f"auth0_{uid}"

    user = await UserService.get_user_by_email(
        db_session,
        email
    )

    assert user is None

    created = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=email,
            username=username,
            password="auth0-user"
        )
    )

    assert created.email == email
    assert created.username == username

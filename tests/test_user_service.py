import uuid

import pytest

from app.schemas.user import SignUpRequest
from app.services.user import UserService


@pytest.mark.asyncio
async def test_create_user(db_session):
    unique_email = f"{uuid.uuid4()}@test.com"
    unique_username = f"user_{uuid.uuid4().hex[:8]}"

    data = SignUpRequest(
        email=unique_email,
        username=unique_username,
        password="123456"
    )

    user = await UserService.create_user(
        db_session,
        data
    )

    assert user.id is not None
    assert user.email == unique_email
    assert user.username == unique_username


@pytest.mark.asyncio
async def test_get_user_by_email(db_session):
    unique_email = f"{uuid.uuid4()}@test.com"
    unique_username = f"user_{uuid.uuid4().hex[:8]}"

    data = SignUpRequest(
        email=unique_email,
        username=unique_username,
        password="123456"
    )

    await UserService.create_user(
        db_session,
        data
    )

    user = await UserService.get_user_by_email(
        db_session,
        unique_email
    )

    assert user is not None
    assert user.email == unique_email

import pytest
import uuid

from app.schemas.user import (
    SignUpRequest,
    UserUpdateRequest,
)
from app.services.user import UserService


@pytest.mark.asyncio
async def test_update_user_username(
    db_session
):
    old_username = f"user_{uuid.uuid4().hex[:8]}"
    new_username = f"user_{uuid.uuid4().hex[:8]}"

    user = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=old_username,
            password="123456"
        )
    )

    updated = await UserService.update_user(
        db_session,
        user.id,
        UserUpdateRequest(
            username=new_username
        )
    )

    assert updated.username == new_username

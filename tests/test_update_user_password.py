import pytest
import uuid

from app.core.security import verify_password
from app.schemas.user import (
    SignUpRequest,
    UserUpdateRequest,
)
from app.services.user import UserService


@pytest.mark.asyncio
async def test_update_user_password(
    db_session
):
    user = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:8]}",
            password="old_password"
        )
    )

    updated = await UserService.update_user(
        db_session,
        user.id,
        UserUpdateRequest(
            password="new_password"
        )
    )

    assert verify_password(
        "new_password",
        updated.password
    )

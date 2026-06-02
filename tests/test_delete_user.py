import pytest
import uuid

from app.schemas.user import SignUpRequest
from app.services.user import UserService


@pytest.mark.asyncio
async def test_delete_user(db_session):
    user = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    await UserService.delete_user(
        db_session,
        user.id
    )

    deleted = await UserService.get_user_by_id(
        db_session,
        user.id
    )

    assert deleted is None

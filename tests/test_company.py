import pytest
import uuid
from app.services.company import CompanyService
from app.services.user import UserService
from app.schemas.company import CompanyCreate
from app.schemas.user import SignUpRequest
from fastapi import HTTPException


def unique_user():
    uid = uuid.uuid4().hex[:8]
    return SignUpRequest(
        email=f"{uid}@test.com",
        username=f"user_{uid}",
        password="12345678",
    )


@pytest.mark.asyncio
async def test_get_companies(db_session):
    user = await UserService.create_user(db_session, unique_user())

    await CompanyService.create_company(db_session, CompanyCreate(name="A"), user.id)
    await CompanyService.create_company(db_session, CompanyCreate(name="B"), user.id)

    result = await CompanyService.get_companies(db_session, 0, 10)

    assert len(result) >= 2


@pytest.mark.asyncio
async def test_delete_company(db_session):
    user = await UserService.create_user(db_session, unique_user())

    company = await CompanyService.create_company(
        db_session,
        CompanyCreate(name="Test"),
        user.id
    )

    await CompanyService.delete_company(db_session, company.id, user.id)

    with pytest.raises(HTTPException):
        await CompanyService.get_company(db_session, company.id)

@pytest.mark.asyncio
async def test_change_visibility(db_session):
    user = await UserService.create_user(db_session, unique_user())

    company = await CompanyService.create_company(
        db_session,
        CompanyCreate(name="Test"),
        user.id
    )

    updated = await CompanyService.change_visibility(
        db_session,
        company.id,
        user.id,
        False
    )

    assert updated.is_visible is False

import pytest
from app.services.company import CompanyService
from app.schemas.company import CompanyCreate
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_create_company(db_session):
    user_id = 1

    company = await CompanyService.create_company(
        db_session,
        data=CompanyCreate(name="Test", description="desc"),
        owner_id=user_id
    )

    assert company.id is not None
    assert company.name == "Test"
    assert company.owner_id == user_id

@pytest.mark.asyncio
async def test_get_company(db_session):
    company = await CompanyService.create_company(
        db_session,
        CompanyCreate(name="Test"),
        owner_id=1
    )

    result = await CompanyService.get_company(db_session, company.id)

    assert result.id == company.id

@pytest.mark.asyncio
async def test_get_companies(db_session):
    await CompanyService.create_company(db_session, CompanyCreate(name="A"), 1)
    await CompanyService.create_company(db_session, CompanyCreate(name="B"), 1)

    result = await CompanyService.get_companies(db_session, 0, 10)

    assert len(result) >= 2


@pytest.mark.asyncio
async def test_delete_company(db_session):
    company = await CompanyService.create_company(
        db_session,
        CompanyCreate(name="Test"),
        owner_id=1
    )

    await CompanyService.delete_company(
        db_session,
        company.id,
        1
    )

    with pytest.raises(HTTPException) as exc:
        await CompanyService.get_company(db_session, company.id)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_change_visibility(db_session):
    company = await CompanyService.create_company(
        db_session,
        CompanyCreate(name="Test"),
        owner_id=1
    )

    updated = await CompanyService.change_visibility(
        db_session,
        company.id,
        owner_id=1,
        is_visible=False
    )

    assert updated.is_visible is False

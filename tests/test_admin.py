import pytest
import uuid

from app.models.company import Company
from app.models.company_member import CompanyMember
from app.schemas.user import SignUpRequest
from app.services.company import CompanyMemberService
from app.services.user import UserService


@pytest.mark.asyncio
async def test_make_admin(db_session):
    owner = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"owner_{uuid.uuid4().hex[:6]}",
            password="123456"
        )
    )

    member_user = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:6]}",
            password="123456"
        )
    )

    company = Company(
        name="Test Company",
        owner_id=owner.id
    )

    db_session.add(company)
    await db_session.commit()
    await db_session.refresh(company)

    member = CompanyMember(
        company_id=company.id,
        user_id=member_user.id,
        role="member"
    )

    db_session.add(member)
    await db_session.commit()
    await db_session.refresh(member)

    updated = await CompanyMemberService.make_admin(
        db_session,
        company,
        member,
        owner.id
    )

    assert updated.role == "admin"



@pytest.mark.asyncio
async def test_get_admins(db_session):
    owner = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"owner_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    admin_user = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"admin_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    company = Company(
        name="Test Company",
        owner_id=owner.id
    )

    db_session.add(company)
    await db_session.commit()
    await db_session.refresh(company)

    member = CompanyMember(
        company_id=company.id,
        user_id=admin_user.id,
        role="admin"
    )

    db_session.add(member)
    await db_session.commit()

    admins = await CompanyMemberService.get_admins(
        db_session,
        company.id
    )

    assert len(admins) == 1
    assert admins[0].role == "admin"


@pytest.mark.asyncio
async def test_get_admins_empty(db_session):
    owner = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"owner_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    company = Company(
        name="Test Company",
        owner_id=owner.id
    )

    db_session.add(company)
    await db_session.commit()
    await db_session.refresh(company)

    admins = await CompanyMemberService.get_admins(
        db_session,
        company.id
    )

    assert admins == []

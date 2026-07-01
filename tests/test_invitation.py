import pytest
from app.services.invitation import InvitationService
from app.services.join_request import JoinRequestService
from app.models.company_member import CompanyMember
from app.services.company import CompanyMemberService
from sqlalchemy import select

@pytest.mark.asyncio
async def test_create_invitation(db_session):
    invitation = await InvitationService.create_invitation(
        db_session,
        company_id=1,
        sender_id=1,
        receiver_id=2
    )

    assert invitation.id is not None
    assert invitation.company_id == 1
    assert invitation.sender_id == 1
    assert invitation.receiver_id == 2


@pytest.mark.asyncio
async def test_accept_invitation(db_session):
    invitation = await InvitationService.create_invitation(
        db_session,
        company_id=1,
        sender_id=1,
        receiver_id=2
    )

    member = await InvitationService.accept_invitation(
        db_session,
        invitation
    )

    assert member.company_id == 1
    assert member.user_id == 2


@pytest.mark.asyncio
async def test_decline_invitation(db_session):
    invitation = await InvitationService.create_invitation(
        db_session,
        company_id=1,
        sender_id=1,
        receiver_id=2
    )

    updated = await InvitationService.decline_invitation(
        db_session,
        invitation
    )

    assert updated.status == "declined"


@pytest.mark.asyncio
async def test_create_join_request(db_session):
    request = await JoinRequestService.create_request(
        db_session,
        company_id=1,
        user_id=2
    )

    assert request.id is not None
    assert request.company_id == 1
    assert request.user_id == 2


@pytest.mark.asyncio
async def test_accept_join_request(db_session):
    request = await JoinRequestService.create_request(
        db_session,
        company_id=1,
        user_id=2
    )

    member = await JoinRequestService.accept_request(
        db_session,
        request
    )

    assert member.company_id == 1
    assert member.user_id == 2


@pytest.mark.asyncio
async def test_remove_member(db_session):
    member = CompanyMember(
        company_id=1,
        user_id=2
    )

    db_session.add(member)

    await db_session.commit()

    await CompanyMemberService.remove_member(
        db_session,
        member
    )

    result = await db_session.execute(
        select(CompanyMember).where(
            CompanyMember.id == member.id
        )
    )

    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_remove_member(db_session):
    member = CompanyMember(
        company_id=1,
        user_id=2
    )

    db_session.add(member)

    await db_session.commit()

    await CompanyMemberService.remove_member(
        db_session,
        member
    )

    result = await db_session.execute(
        select(CompanyMember).where(
            CompanyMember.id == member.id
        )
    )

    assert result.scalar_one_or_none() is None

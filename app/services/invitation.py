from app.models.invitation import Invitation
from app.models.company_member import CompanyMember
from sqlalchemy import select
from app.models.invitation import Invitation
from fastapi import HTTPException

class InvitationService:

    @staticmethod
    async def create_invitation(
        db,
        company_id,
        sender_id,
        receiver_id
    ):
        invitation = Invitation(
            company_id=company_id,
            sender_id=sender_id,
            receiver_id=receiver_id
        )

        db.add(invitation)

        await db.commit()
        await db.refresh(invitation)

        return invitation

    @staticmethod
    async def accept_invitation(
        db,
        invitation
    ):
        invitation.status = "accepted"

        member = CompanyMember(
            company_id=invitation.company_id,
            user_id=invitation.receiver_id
        )

        db.add(member)

        await db.commit()

        return member

    @staticmethod
    async def decline_invitation(
        db,
        invitation
    ):
        invitation.status = "declined"

        await db.commit()

        return invitation

    @staticmethod
    async def cancel_invitation(
        db,
        invitation
    ):
        await db.delete(invitation)

        await db.commit()

    from sqlalchemy import select
    from app.models.invitation import Invitation

    @staticmethod
    async def get_user_invitations(
        db,
        user_id
    ):
        result = await db.execute(
            select(Invitation).where(
                Invitation.receiver_id == user_id,
                Invitation.status == "pending"
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_company_invitations(
        db,
        company_id
    ):
        result = await db.execute(
            select(Invitation).where(
                Invitation.company_id == company_id,
                Invitation.status == "pending"
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db,
        invitation_id: int
    ):
        result = await db.execute(
            select(Invitation).where(
                Invitation.id == invitation_id
            )
        )

        invitation = result.scalar_one_or_none()

        if not invitation:
            raise HTTPException(
                status_code=404,
                detail="Invitation not found"
            )

        return invitation

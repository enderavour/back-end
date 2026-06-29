from app.models.join_request import JoinRequest
from app.models.company_member import CompanyMember
from sqlalchemy import select
from fastapi import HTTPException

class JoinRequestService:

    @staticmethod
    async def create_request(
        db,
        company_id,
        user_id
    ):
        request = JoinRequest(
            company_id=company_id,
            user_id=user_id
        )

        db.add(request)

        await db.commit()
        await db.refresh(request)

        return request

    @staticmethod
    async def accept_request(
        db,
        request
    ):
        request.status = "accepted"

        member = CompanyMember(
            company_id=request.company_id,
            user_id=request.user_id
        )

        db.add(member)

        await db.commit()

        return member

    @staticmethod
    async def decline_request(
        db,
        request
    ):
        request.status = "declined"

        await db.commit()

        return request

    @staticmethod
    async def cancel_request(
        db,
        request
    ):
        await db.delete(request)

        await db.commit()


    @staticmethod
    async def get_user_requests(
        db,
        user_id
    ):
        result = await db.execute(
            select(JoinRequest).where(
                JoinRequest.user_id == user_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_company_requests(
        db,
        company_id
    ):
        result = await db.execute(
            select(JoinRequest).where(
                JoinRequest.company_id == company_id,
                JoinRequest.status == "pending"
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
            db,
            request_id: int
    ):
        result = await db.execute(
            select(JoinRequest).where(
                JoinRequest.id == request_id
            )
        )

        request = result.scalar_one_or_none()

        if not request:
            raise HTTPException(
                status_code=404,
                detail="Request not found"
            )

        return request

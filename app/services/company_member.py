from sqlalchemy import select
from app.models.company_member import CompanyMember
from fastapi import HTTPException

class CompanyMemberService:

    @staticmethod
    async def remove_member(
        db,
        member
    ):
        await db.delete(member)

        await db.commit()

    @staticmethod
    async def leave_company(
        db,
        member
    ):
        await db.delete(member)

        await db.commit()

    @staticmethod
    async def get_company_members(
        db,
        company_id,
        skip=0,
        limit=10
    ):
        result = await db.execute(
            select(CompanyMember)
            .where(
                CompanyMember.company_id == company_id
            )
            .offset(skip)
            .limit(limit)
        )

        return result.scalars().all()

    @staticmethod
    async def make_admin(
        db,
        company,
        member,
        owner_id
    ):
        if company.owner_id != owner_id:
            raise HTTPException(
                status_code=403,
                detail="Only owner can appoint admins"
            )

        member.role = "admin"

        await db.commit()
        await db.refresh(member)

        return member

    @staticmethod
    async def remove_admin(
        db,
        company,
        member,
        owner_id
    ):
        if company.owner_id != owner_id:
            raise HTTPException(
                status_code=403,
                detail="Only owner can remove admins"
            )

        member.role = "member"

        await db.commit()
        await db.refresh(member)

        return member

    @staticmethod
    async def get_admins(
        db,
        company_id
    ):
        result = await db.execute(
            select(CompanyMember).where(
                CompanyMember.company_id == company_id,
                CompanyMember.role == "admin"
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_member(
        db,
        company_id: int,
        user_id: int
    ):
        result = await db.execute(
            select(CompanyMember).where(
                CompanyMember.company_id == company_id,
                CompanyMember.user_id == user_id
            )
        )

        member = result.scalar_one_or_none()

        if not member:
            raise HTTPException(
                status_code=404,
                detail="Member not found"
            )

        return member

    @staticmethod
    async def get_user_companies(db, user_id: int):
        result = await db.execute(
            select(CompanyMember)
            .where(CompanyMember.user_id == user_id)
        )

        return result.scalars().all()

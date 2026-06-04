from sqlalchemy import select
from app.models.company_member import CompanyMember

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

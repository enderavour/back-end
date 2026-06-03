from sqlalchemy import select
from app.models.company import Company


class CompanyRepository:

    @staticmethod
    async def create(db, company):
        db.add(company)

        await db.commit()
        await db.refresh(company)

        return company

    @staticmethod
    async def get_by_id(db, company_id):
        result = await db.execute(
            select(Company).where(
                Company.id == company_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db,
        skip=0,
        limit=10
    ):
        result = await db.execute(
            select(Company)
            .offset(skip)
            .limit(limit)
        )

        return result.scalars().all()

    @staticmethod
    async def delete(db, company):
        await db.delete(company)
        await db.commit()

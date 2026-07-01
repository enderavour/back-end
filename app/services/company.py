from fastapi import HTTPException
from app.models.company_member import CompanyMember
from sqlalchemy import select
from app.models.company import Company
from app.repositories.company import CompanyRepository

class CompanyService:

    @staticmethod
    async def create_company(
        db,
        data,
        owner_id
    ):
        company = Company(
            name=data.name,
            description=data.description,
            owner_id=owner_id
        )

        return await CompanyRepository.create(
            db,
            company
        )

    @staticmethod
    async def get_company(
        db,
        company_id
    ):
        company = await CompanyRepository.get_by_id(
            db,
            company_id
        )

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found"
            )

        return company

    @staticmethod
    async def get_companies(
        db,
        skip,
        limit
    ):
        return await CompanyRepository.get_all(
            db,
            skip,
            limit
        )

    @staticmethod
    async def update_company(
        db,
        company_id: int,
        owner_id: int,
        data
    ):
        company = await CompanyRepository.get_by_id(
            db,
            company_id
        )

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found"
            )

        if company.owner_id != owner_id:
            raise HTTPException(
                status_code=403,
                detail="Only owner can edit company"
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(company, key, value)

        await db.commit()
        await db.refresh(company)

        return company

    @staticmethod
    async def delete_company(
        db,
        company_id: int,
        owner_id: int
    ):
        company = await CompanyRepository.get_by_id(
            db,
            company_id
        )

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found"
            )

        if company.owner_id != owner_id:
            raise HTTPException(
                status_code=403,
                detail="Only owner can delete company"
            )

        await CompanyRepository.delete(
            db,
            company
        )

        return {
            "message": "Company deleted"
        }

    @staticmethod
    async def change_visibility(
        db,
        company_id: int,
        owner_id: int,
        is_visible: bool
    ):
        company = await CompanyRepository.get_by_id(
            db,
            company_id
        )

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found"
            )

        if company.owner_id != owner_id:
            raise HTTPException(
                status_code=403,
                detail="Only owner can change visibility"
            )

        company.is_visible = is_visible

        await db.commit()
        await db.refresh(company)

        return company

    @staticmethod
    async def check_owner_or_admin(db, company_id: int, user_id: int):
        company = await CompanyService.get_company(db, company_id)

        if company.owner_id == user_id:
            return company

        member = await CompanyMemberService.get_member(db, company_id, user_id)

        if member.role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

        return company


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
    async def check_admin_permissions(db, company_id, user_id):
        company = await CompanyService.get_company(db, company_id)

        if company.owner_id == user_id:
            return

        member = await CompanyMemberService.get_member(db, company.id, user_id)

        if member.role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

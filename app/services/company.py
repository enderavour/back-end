from fastapi import HTTPException

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

        return await CompanyRepository.update(db, company, update_data)

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

        return await CompanyRepository.update(db, company, {"is_visible": is_visible})

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_auth_user
from app.db.deps import get_db
from app.schemas.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanySchema,
)
from app.services.company import CompanyService

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.post(
    "/",
    response_model=CompanySchema,
    status_code=status.HTTP_201_CREATED
)
async def create_company(
    data: CompanyCreate,
    current_user=Depends(get_auth_user),
    db: AsyncSession = Depends(get_db),
):
    return await CompanyService.create_company(
        db,
        data,
        current_user.id
    )


@router.get("/", response_model=list[CompanySchema], status_code=status.HTTP_200_OK)
async def get_companies(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    return await CompanyService.get_companies(
        db,
        skip,
        limit
    )


@router.get("/{company_id}", response_model=CompanySchema, status_code=status.HTTP_200_OK)
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await CompanyService.get_company(
        db,
        company_id
    )

@router.patch("/{company_id}", response_model=CompanySchema, status_code=status.HTTP_200_OK)
async def update_company(
    company_id: int,
    data: CompanyUpdate,
    current_user=Depends(get_auth_user),
    db: AsyncSession = Depends(get_db),
):
    return await CompanyService.update_company(
        db,
        company_id,
        current_user,
        data
    )

@router.delete("/{company_id}")
async def delete_company(
    company_id: int,
    current_user=Depends(get_auth_user),
    db: AsyncSession = Depends(get_db),
):
    return await CompanyService.delete_company(
        db,
        company_id,
        current_user.id
    )


@router.patch("/{company_id}/visibility", response_model=CompanySchema, status_code=status.HTTP_200_OK)
async def change_visibility(
    company_id: int,
    is_visible: bool,
    current_user=Depends(get_auth_user),
    db: AsyncSession = Depends(get_db),
):
    return await CompanyService.change_visibility(
        db,
        company_id,
        current_user.id,
        is_visible
    )

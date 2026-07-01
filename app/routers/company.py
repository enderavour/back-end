from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_auth_user
from app.db.deps import get_db
from app.schemas.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanySchema,
)
from app.services.company import CompanyService, CompanyMemberService
from app.services.invitation import InvitationService
from app.services.join_request import JoinRequestService

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.post(
    "/",
    response_model=CompanySchema,
    status_code=201
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


@router.get("/")
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


@router.get("/{company_id}")
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await CompanyService.get_company(
        db,
        company_id
    )

@router.patch("/{company_id}")
async def update_company(
    company_id: int,
    data: CompanyUpdate,
    current_user=Depends(get_auth_user),
    db: AsyncSession = Depends(get_db),
):
    return await CompanyService.update_company(
        db,
        company_id,
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


@router.patch("/{company_id}/visibility")
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


@router.get("/{company_id}/members")
async def company_members(
    company_id: int,
    skip: int = 0,
    limit: int = 10,
    db=Depends(get_db),
):
    return await CompanyMemberService.get_company_members(
        db,
        company_id,
        skip,
        limit
    )

@router.get("/{company_id}/invitations")
async def company_invitations(
    company_id: int,
    db=Depends(get_db),
):
    return await InvitationService.get_company_invitations(
        db,
        company_id
    )

@router.get("/{company_id}/requests")
async def company_requests(
    company_id: int,
    db=Depends(get_db),
):
    return await JoinRequestService.get_company_requests(
        db,
        company_id
    )


@router.post("/{company_id}/admins/{user_id}")
async def appoint_admin(
    company_id: int,
    user_id: int,
    current_user=Depends(get_auth_user),
    db=Depends(get_db),
):
    company = await CompanyService.get_company(
        db,
        company_id
    )

    member = await CompanyMemberService.get_member(
        db,
        company_id,
        user_id
    )

    return await CompanyMemberService.make_admin(
        db,
        company,
        member,
        current_user.id
    )


@router.delete("/{company_id}/admins/{user_id}")
async def remove_admin(
    company_id: int,
    user_id: int,
    current_user=Depends(get_auth_user),
    db=Depends(get_db),
):
    company = await CompanyService.get_company(
        db,
        company_id
    )

    member = await CompanyMemberService.get_member(
        db,
        company_id,
        user_id
    )

    return await CompanyMemberService.remove_admin(
        db,
        company,
        member,
        current_user.id
    )

@router.get("/{company_id}/admins")
async def get_admins(
    company_id: int,
    db=Depends(get_db),
):
    return await CompanyMemberService.get_admins(
        db,
        company_id
    )

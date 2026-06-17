from fastapi import APIRouter, Depends, HTTPException
from app.services.analytics_service import AnalyticsService
from app.core.security import get_auth_user, get_current_user
from app.services.company import CompanyService
from app.services.company_member import CompanyMemberService
from app.db.deps import get_db

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/me")
async def get_analytics_current(
    current_user=Depends(get_auth_user)
):
    return await AnalyticsService.get_user_stats(current_user.id)

@router.get("/me/quizzes")
async def get_current_user_quizzes(
    current_user=Depends(get_auth_user)
):
    return await AnalyticsService.get_user_quiz_stats(current_user.id)


@router.get("/me/last")
async def get_analytics_last(
    current_user=Depends(get_auth_user)
):
    return await AnalyticsService.get_user_last_attempts(current_user.id)


@router.get("/company/{company_id}")
async def get_company_analytics(
    company_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    company = await CompanyService.get_company(db, company_id)

    if company.owner_id != current_user.id:
        member = await CompanyMemberService.get_member(
            db,
            company_id,
            current_user.id
        )

        if not member or member.role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

    return await AnalyticsService.get_company_stats(company_id)


@router.get("/company/{company_id}/users")
async def get_company_users_analytics(
    company_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    company = await CompanyService.get_company(db, company_id)

    if company.owner_id != current_user.id:
        member = await CompanyMemberService.get_member(
            db,
            company_id,
            current_user.id
        )

        if not member or member.role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

    return await AnalyticsService.get_company_user_stats(company_id)


@router.get("/company/{company_id}/last")
async def get_last_company_analytics(
    company_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    company = await CompanyService.get_company(db, company_id)

    if company.owner_id != current_user.id:
        member = await CompanyMemberService.get_member(
            db,
            company_id,
            current_user.id
        )

        if not member or member.role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

    return await AnalyticsService.get_company_last_activity(company_id)


@router.get("/company/{company_id}/user/{user_id}/quizzes")
async def get_company_user_quizzes(
    company_id: int,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    company = await CompanyService.get_company(db, company_id)

    if company.owner_id != current_user.id:
        member = await CompanyMemberService.get_member(
            db,
            company_id,
            current_user.id
        )

        if not member or member.role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

    return await AnalyticsService.get_company_user_quiz_stats(
        company_id,
        user_id
    )

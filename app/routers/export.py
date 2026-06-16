from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_auth_user
from app.services.export import ExportService
from app.services.company import CompanyService
from app.services.company_member import CompanyMemberService
from app.db.deps import get_db
from fastapi.responses import Response

router = APIRouter(
    prefix="/export",
    tags=["Export"]
)

@router.get("/me/json")
async def export_me_json(
    current_user=Depends(get_auth_user)
):
    return await ExportService.export_user_json(current_user.id)

@router.get("/me/csv")
async def export_me_csv(
    current_user=Depends(get_auth_user)
):
    csv_data = await ExportService.export_user_csv(current_user.id)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers = {
            "Content-Disposition": 'attachment; filename="my_answers.csv"'
        }
    )

@router.get("/company/{company_id}/json")
async def export_company_json(
    company_id: int,
    db=Depends(get_db),
    current_user=Depends(get_auth_user)
):
    company = await CompanyService.get_company(
        db,
        company_id
    )

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

    return await ExportService.export_company_json(company_id)

@router.get("/company/{company_id}/csv")
async def export_company_csv(
    company_id: int,
    db=Depends(get_db),
    current_user=Depends(get_auth_user)
):
    company = await CompanyService.get_company(
        db,
        company_id
    )

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

    csv_data = ExportService.export_company_csv(company_id)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers = {
            "Content-Disposition": f'attachment; filename="company_{company_id}.csv'
        }
    )

@router.get("/company/{company_id}/quiz/{quiz_id}/csv")
async def export_quiz_csv(
    company_id: int,
    quiz_id: int,
    db=Depends(get_db),
    current_user=Depends(get_auth_user)
):
    company = await CompanyService.get_company(
        db,
        company_id
    )

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

    csv_data =  await ExportService.export_quiz_csv(
        company_id,
        quiz_id
    )

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers = {
            "Content-Disposition": f'attachment; filename="user_{quiz_id}.csv'
        }
    )


@router.get("/company/{company_id}/user/{user_id}/json")
async def export_company_user_json(
    company_id: int,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_auth_user)
):
    company = await CompanyService.get_company(db, company_id)

    if company.owner_id != current_user.id:
        member = await CompanyMemberService.get_member(db, company_id, current_user.id)

        if not member or member.role != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")


    return await ExportService.export_company_user_json(company_id, user_id)


@router.get("/company/{company_id}/user/{user_id}/csv")
async def export_company_user_csv(
    company_id: int,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_auth_user)
):
    company = await CompanyService.get_company(db, company_id)

    if company.owner_id != current_user.id:
        member = await CompanyMemberService.get_member(db, company_id, current_user.id)

        if not member or member.role != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")

    csv_data = await ExportService.export_company_user_csv(company_id, user_id)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers = {
            "Content-Disposition": f'attachment; filename="user_{user_id}.csv'
        }
    )


@router.get("/company/{company_id}/quiz/{quiz_id}/json")
async def export_quiz_json(
    company_id: int,
    quiz_id: int,
    db=Depends(get_db),
    current_user=Depends(get_auth_user)
):
    company = await CompanyService.get_company(db, company_id)

    if company.owner_id != current_user.id:
        member = await CompanyMemberService.get_member(db, company_id, current_user.id)

        if not member or member.role != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")

    return await ExportService.export_quiz_json(company_id, quiz_id)

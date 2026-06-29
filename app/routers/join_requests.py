from fastapi import APIRouter, Depends

from app.core.security import get_auth_user
from app.db.deps import get_db
from app.services.join_request import JoinRequestService

router = APIRouter(
    prefix="/requests",
    tags=["Join Requests"]
)

@router.post("/{company_id}")
async def create_request(
    company_id: int,
    current_user=Depends(get_auth_user),
    db=Depends(get_db),
):
    return await JoinRequestService.create_request(
        db,
        company_id,
        current_user.id
    )


@router.get("/my")
async def my_requests(
    current_user=Depends(get_auth_user),
    db=Depends(get_db),
):
    return await JoinRequestService.get_user_requests(
        db,
        current_user.id
    )


@router.post("/{request_id}/accept")
async def accept_request(
    request_id: int,
    current_user=Depends(get_auth_user),
    db=Depends(get_db),
):
    request = await JoinRequestService.get_by_id(
        db,
        request_id
    )

    return await JoinRequestService.accept_request(
        db,
        request
    )

@router.post("/{request_id}/decline")
async def decline_request(
    request_id: int,
    current_user=Depends(get_auth_user),
    db=Depends(get_db),
):
    request = await JoinRequestService.get_by_id(
        db,
        request_id
    )

    return await JoinRequestService.decline_request(
        db,
        request
    )

@router.delete("/{request_id}")
async def cancel_request(
    request_id: int,
    current_user=Depends(get_auth_user),
    db=Depends(get_db),
):
    request = await JoinRequestService.get_by_id(
        db,
        request_id
    )

    return await JoinRequestService.cancel_request(
        db,
        request
    )

from fastapi import APIRouter, Depends

from app.core.security import get_auth_user
from app.db.deps import get_db
from app.services.invitation import InvitationService

router = APIRouter(
    prefix="/invitations",
    tags=["Invitations"]
)

@router.get("/my")
async def my_invitations(
    current_user=Depends(get_auth_user),
    db=Depends(get_db),
):
    return await InvitationService.get_user_invitations(
        db,
        current_user.id
    )


@router.post("/{invitation_id}/accept")
async def accept_invitation(
    invitation_id: int,
    current_user=Depends(get_auth_user),
    db=Depends(get_db),
):
    invitation = await InvitationService.get_by_id(
        db,
        invitation_id
    )

    return await InvitationService.accept_invitation(
        db,
        invitation
    )


@router.post("/{invitation_id}/decline")
async def decline_invitation(
    invitation_id: int,
    current_user=Depends(get_auth_user),
    db=Depends(get_db),
):
    invitation = await InvitationService.get_by_id(
        db,
        invitation_id
    )

    return await InvitationService.decline_invitation(
        db,
        invitation
    )

@router.delete("/{invitation_id}")
async def cancel_invitation(
    invitation_id: int,
    current_user=Depends(get_auth_user),
    db=Depends(get_db),
):
    invitation = await InvitationService.get_by_id(
        db,
        invitation_id
    )

    return await InvitationService.cancel_invitation(
        db,
        invitation
    )

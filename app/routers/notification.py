from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_auth_user
from app.db.deps import get_db
from app.services.join_request import JoinRequestService
from app.services.notification import NotificationService
router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/")
async def get_notifications(
    db=Depends(get_db),
    current_user=Depends(get_auth_user)
):
    return await NotificationService.get_user_notifications(db, current_user.id)

@router.patch("/{notification_id}/read")
async def read_notification(
    notification_id: int,
    db=Depends(get_db),
    current_user=Depends(get_auth_user)
):
    notification = await NotificationService.get_notification(db, notification_id)

    if not notification:
        raise HTTPException(404, detail="Notification not found")

    if notification.user_id != current_user.id:
        raise HTTPException(403, detail="Access to the notification is denied")

    return await NotificationService.mark_as_read(db, notification_id)

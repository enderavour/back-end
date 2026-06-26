from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification

class NotificationService:
    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: int,
        message: str
    ) -> Notification:
        notification = Notification(
            user_id = user_id,
            message = message
        )

        db.add(notification)

        return notification

    @staticmethod
    async def get_user_notifications(
        db: AsyncSession,
        user_id: int
    ):
        result = await db.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )

        return result.scalars().all()

    @staticmethod
    async def get_notification(
        db: AsyncSession,
        notification_id: int
    ):
        result = await db.execute(
            select(Notification)
            .where(Notification.id == notification_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def mark_as_read(
        db: AsyncSession,
        notification_id: int
    ):
        notification = await NotificationService.get_notification(db, notification_id)

        if not notification:
            return None

        notification.is_read = True

        await db.commit()
        await db.refresh(notification)

        return notification

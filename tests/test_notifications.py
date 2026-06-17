import pytest

from app.services.notification import NotificationService


@pytest.mark.asyncio
async def test_create_notification(db_session):
    notification = await NotificationService.create(
        db=db_session,
        user_id=1,
        message="Test notification"
    )

    await db_session.commit()

    assert notification.user_id == 1
    assert notification.message == "Test notification"
    assert notification.is_read is False


@pytest.mark.asyncio
async def test_get_user_notifications(db_session, clear_notifications):
    await NotificationService.create(
        db_session,
        1,
        "First"
    )

    await NotificationService.create(
        db_session,
        1,
        "Second"
    )

    await db_session.commit()

    notifications = await NotificationService.get_user_notifications(
        db_session,
        1
    )

    assert len(notifications) == 2


@pytest.mark.asyncio
async def test_mark_notification_read(db_session):
    notification = await NotificationService.create(
        db_session,
        1,
        "Hello"
    )

    await db_session.commit()

    await NotificationService.mark_as_read(
        db_session,
        notification.id
    )

    assert notification.is_read is True


@pytest.mark.asyncio
async def test_only_user_notifications(db_session, clear_notifications):
    await NotificationService.create(db_session, 1, "User1")
    await NotificationService.create(db_session, 2, "User2")

    await db_session.commit()

    notifications = await NotificationService.get_user_notifications(
        db_session,
        1
    )

    assert len(notifications) == 1
    assert notifications[0].user_id == 1

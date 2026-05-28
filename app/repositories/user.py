from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.models.user import User


class UserRepository:
    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10,
    ):
        result = await db.execute(select(User).offset(skip).limit(limit))

        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))

        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user: User):
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info("User was created")

        return user

    @staticmethod
    async def delete(db: AsyncSession, user: User):
        await db.delete(user)
        await db.commit()
        logger.info("User was deleted")

    @staticmethod
    async def update(db: AsyncSession, user: User, data: dict):
        for key, value in data.items():
            setattr(user, key, value)

        logger.info("User was updated")
        await db.commit()
        await db.refresh(user)
        return user

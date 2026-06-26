from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logger import logger
from app.models.user import User, UserDTO
from app.core.security import hash_password

class UserRepository:
    @staticmethod
    async def get_all(db, skip=0, limit=10):
        result = await db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db, user_id: int):
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db, email: str):
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db, user: User):
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete(db, user: User):
        await db.delete(user)

    @staticmethod
    async def update(db, user: User, data: dict):
        for k, v in data.items():
            setattr(user, k, v)

        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def create_from_dict(db, data: dict):
        user = User(**data)
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

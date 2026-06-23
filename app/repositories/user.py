from .base import BaseRepository
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository(BaseRepository):
    model = User

    @classmethod
    async def update(cls, db: AsyncSession, user: User, data: dict):
        for key, value in data.items():
            setattr(user, key, value)

        await db.commit()
        await db.refresh(user)
        return user

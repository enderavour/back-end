from sqlalchemy import select

class BaseRepository:
    model = None

    @classmethod
    async def create(cls, db, obj):
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    @classmethod
    async def get_by_id(cls, db, obj_id):
        result = await db.execute(
            select(cls.model).where(cls.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, db, skip=0, limit=10):
        result = await db.execute(
            select(cls.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    @classmethod
    async def delete(cls, db, obj):
        await db.delete(obj)
        await db.commit()

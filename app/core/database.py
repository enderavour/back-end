from os import getenv
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.logger import logger

engine = create_async_engine(settings.DATABASE_URL)
logger.info("Database async engine created")

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

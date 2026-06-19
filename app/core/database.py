from os import getenv
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.logger import logger

DATABASE_URL = getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)
logger.info("Database async engine created")

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

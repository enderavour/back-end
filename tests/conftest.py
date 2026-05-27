import pytest_asyncio
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(settings.DATABASE_URL)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine):
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with AsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def redis_client():
    client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )

    yield client

    await client.aclose()

import pytest_asyncio
import redis.asyncio as redis
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.main import app
from app.routers.user import get_db
from sqlalchemy import delete
from app.models.notification import Notification


async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(settings.DATABASE_URL)

    yield engine

    await engine.dispose()

@pytest_asyncio.fixture
async def clear_notifications(db_session):
    await db_session.execute(delete(Notification))
    await db_session.commit()
    yield
    await db_session.execute(delete(Notification))
    await db_session.commit()


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


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac

@pytest_asyncio.fixture(autouse=True)
async def clear_redis(redis_client):
    await redis_client.flushdb()
    yield
    await redis_client.flushdb()

from fastapi import FastAPI

from app.core.cors import setup_cors
from app.core.database import engine
from app.core.logger import logger
from app.db.base import Base
from app.routers.health import router as health_router
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.company import router as company_router
from app.routers.quiz import router as quiz_router
from app.routers.export import router as export_router
from app.routers.analytics import router as analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await redis_client.aclose()


app = FastAPI(lifespan=lifespan)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


setup_cors(app)

app.include_router(health_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(company_router)
app.include_router(quiz_router)
app.include_router(export_router)
app.include_router(analytics_router)
logger.info("Application started")

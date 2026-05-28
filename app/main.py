from fastapi import FastAPI

from app.core.cors import setup_cors
from app.core.database import engine
from app.core.logger import logger
from app.db.base import Base
from app.routers.health import router as health_router
from app.routers.user import router as user_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


setup_cors(app)

app.include_router(health_router)
app.include_router(user_router)
logger.info("Application started")

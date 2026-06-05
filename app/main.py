from fastapi import FastAPI

from app.core.cors import setup_cors
from app.core.logger import logger
from app.routers.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await redis_client.aclose()


app = FastAPI(lifespan=lifespan)

setup_cors(app)

app.include_router(health_router)
logger.info("Application started")

from app.core.cors import setup_cors
from fastapi import FastAPI

from app.routers.health import router as health_router

app = FastAPI()

setup_cors(app)

app.include_router(health_router)

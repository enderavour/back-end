from fastapi import FastAPI

from app.services.health_service import get_health

app = FastAPI()


@app.get("/")
async def health_check():
    return get_health()

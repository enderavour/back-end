from fastapi import APIRouter, status

from app.core.logger import logger

router = APIRouter()


@router.get("/")
async def health_check():
    logger.info("Health check called")
    return {"status_code": status.HTTP_200_OK, "detail": "ok", "result": "working"}

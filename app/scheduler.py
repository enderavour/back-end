from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.scheduler_service import SchedulerService
from app.core.database import AsyncSessionLocal

scheduler = AsyncIOScheduler()

async def scheduled_check():
    async with AsyncSessionLocal() as db:
        await SchedulerService.check_quizzes(db)

def setup_scheduler():
    scheduler.add_job(
        scheduled_check,
        trigger="cron",
        hour=0,
        minute=0
    )

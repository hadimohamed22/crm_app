from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .tasks import sample_task
from .config import config

def start_scheduler():
    if config.get("scheduler", "enabled", True):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(sample_task, "interval", seconds=config.get("scheduler", "interval_seconds", 60))
        scheduler.start()
        return scheduler
    return None
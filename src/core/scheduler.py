from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .tasks import sample_task
from .config import config
from .logger import logger

def start_scheduler():
    if config.get("scheduler", "enabled", True):
        scheduler = AsyncIOScheduler(logger=logger)
        scheduler.add_job(sample_task, "interval", seconds=config.get("scheduler", "interval_seconds", 60))
        scheduler.start()
        return scheduler
    return None
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .config import config

scheduler = AsyncIOScheduler()
scheduler_enabled = config.get("scheduler", {}).get("enabled", True)

def start_scheduler():
    if scheduler_enabled and not scheduler.running:
        scheduler.start()
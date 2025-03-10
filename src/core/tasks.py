from .scheduler import scheduler
from typing import Callable

class TaskManager:
    def add_task(self, func: Callable, interval: int, *args, **kwargs):
        scheduler.add_job(func, "interval", seconds=interval, args=args, kwargs=kwargs)

    def run_once(self, func: Callable, *args, **kwargs):
        scheduler.add_job(func, args=args, kwargs=kwargs)

tasks = TaskManager()
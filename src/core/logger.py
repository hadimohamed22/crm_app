import logging
import os
from .config import config

class Logger:
    def __init__(self, name: str = "app_logger"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG if config.get("app", "debug", False) else logging.INFO)
        self._setup_handlers()

    def _setup_handlers(self):
        log_dir = config.get("app", "log_dir", "logs")
        os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(f"{log_dir}/app.log")
        file_handler.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.handlers.clear()
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

logger = Logger()
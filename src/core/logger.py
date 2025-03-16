import logging
import os
from .config import config


class Colors:
    INFO = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'    
    DEBUG= '\033[94m'    
    HEADER = '\033[45m'
    BLINK = '\033[6m'
    OKCYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    TIME = '\033[100m'


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = f"{getattr(Colors, record.levelname)}{record.levelname}{Colors.ENDC}"
        record.name = f"{Colors.UNDERLINE}[{record.name}]{Colors.ENDC}"
        record.asctime = f"{Colors.UNDERLINE}{record.asctime}{Colors.ENDC}"
        record.message =  f"{Colors.HEADER}{record.message}{Colors.ENDC}"
        
        return super().format(record)
    
            
class Logger:
    def __init__(self, name: str = "app_logger"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG if config.get("app", "debug", False) else logging.INFO)
        self._setup_handlers()

    def _setup_handlers(self):
        log_dir = config.get("app", "log_dir", "logs")
        os.makedirs(log_dir, exist_ok=True)

        # File handler (no color formatting)
        file_handler = logging.FileHandler(f"{log_dir}/app.log")
        file_handler.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            "%(levelname)s:     %(asctime)s [%(name)s]   %(message)s"
        )
        file_handler.setFormatter(formatter)
        
        # Console handler (with color formatting)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            "%(levelname)s:     %(asctime)s %(name)s   %(message)s"
        )
        console_handler.setFormatter(console_formatter)

        # Clear existing handlers and add new ones
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
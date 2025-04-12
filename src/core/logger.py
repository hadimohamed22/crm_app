import logging
import os
from .config import config
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init()


class Colors:
    INFO = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    DEBUG = "\033[94m"
    HEADER = "\033[45m"
    BLINK = "\033[6m"
    OKCYAN = "\033[96m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    TIME = "\033[100m"


class FileFormatter(logging.Formatter):
    def format(self, record):
        return (
            f"{record.levelname}:{' ' * (9 - len(record.levelname))}"
            f"{self.formatTime(record)} "
            f"[{record.name}] "
            f"{record.msg}"
        )


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": Fore.BLUE,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        level_color = self.COLORS.get(record.levelname, Fore.WHITE)
        time_color = Fore.CYAN  # Separate color for time
        message_color = Fore.WHITE + Style.BRIGHT  # Default message color
        reset = Style.RESET_ALL
        logger_name_color = Style.DIM + Fore.MAGENTA

        # Format with colored sections
        return (
            f"{level_color}{record.levelname}{reset}:{' ' * (9 - len(record.levelname))}"
            f"{time_color}{self.formatTime(record)}{reset} "
            f"{logger_name_color}[{record.name}]{reset} "
            f"{message_color}{record.msg}{reset}"
        )


class Logger:
    def __init__(self, name: str = "app_logger"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(
            logging.DEBUG if config.get("app", "debug", False) else logging.INFO
        )
        self._setup_handlers()

    def _setup_handlers(self):
        log_dir = config.get("app", "log_dir", "logs")
        os.makedirs(log_dir, exist_ok=True)

        # File handler (no color formatting)
        file_handler = logging.FileHandler(f"{log_dir}/app.log")
        file_handler.setLevel(self.logger.level)
        file_formatter = FileFormatter()
        file_handler.setFormatter(file_formatter)

        # Console handler (with color formatting)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.logger.level)
        console_formatter = ColoredFormatter()
        console_handler.setFormatter(console_formatter)

        # Clear existing handlers and add new ones
        self.logger.handlers.clear()
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _format_message(self, message: str, *args, **kwargs) -> str:
        try:
            # First try %-formatting if message contains % and we have args
            if "%" in message and args:
                return message % args
        except (TypeError, ValueError):
            pass  # Fall through to concatenation if formatting fails

        # If no %-formatting or it failed, concatenate all parts
        parts = [str(message)]
        parts.extend(str(arg) for arg in args)
        parts.extend(f"{k}={v}" for k, v in kwargs.items())
        return " ".join(parts)

    def log(self, level: int, message: str, *args, **kwargs):
        """Generic log method supporting both %-formatting and concatenation."""
        formatted_msg = self._format_message(message, *args, **kwargs)
        self.logger.log(level, formatted_msg)

    def info(self, message: str, *args, **kwargs):
        """Log an info message."""
        formatted_msg = self._format_message(message, *args, **kwargs)
        self.logger.info(formatted_msg)

    def debug(self, message: str, *args, **kwargs):
        """Log a debug message."""
        formatted_msg = self._format_message(message, *args, **kwargs)
        self.logger.debug(formatted_msg)

    def error(self, message: str, *args, **kwargs):
        """Log an error message."""
        formatted_msg = self._format_message(message, *args, **kwargs)
        self.logger.error(formatted_msg)

    def warning(self, message: str, *args, **kwargs):
        """Log a warning message."""
        formatted_msg = self._format_message(message, *args, **kwargs)
        self.logger.warning(formatted_msg)


logger = Logger()

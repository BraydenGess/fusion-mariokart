import sys
import logging
from typing import Optional
from pathlib import Path
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler

class NamespaceFilter(logging.Filter):
    def __init__(self, namespaces):
        super().__init__()
        self.namespaces = namespaces

    def filter(self, record):
        #return any(
        #    record.name == ns or record.name.startswith(f"{ns}.")
        #    for ns in self.namespaces
        #)
        return any(record.name.startswith(ns) for ns in self.namespaces)

def setup_logging(
        log_level_console: int = logging.ERROR,
        log_level_file: int = logging.DEBUG,
        logfile: Optional[str] = "logs/app.log",
        app_logger_names = ["audio","src"]
    ) -> None:
    """
    Set up application-wide logging with colored console output and rotating file logs
    Args:
        log_level_console (int, optional): Logging level for console output.
            Defaults to logging.ERROR.
        log_level_file (int, optional): Logging level for file output.
            Defaults to logging.DEBUG.
        logfile (str | None, optional): File path for log file.
            If None, file logging is disabled.
            Defaults to "logs/app.log".
    """
    console_formatter = ColoredFormatter(
        fmt="%(log_color)s[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level_console)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture all logs, handlers filter levels
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)

    if logfile:
        log_path = Path(logfile).resolve()
        log_dir = log_path.parent
        if not log_dir.exists():
            raise FileNotFoundError(f"Log directory does not exist at: {log_dir}")

    file_formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = RotatingFileHandler(
        logfile,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_level_file)
    file_handler.addFilter(NamespaceFilter(app_logger_names))
    root_logger.addHandler(file_handler)
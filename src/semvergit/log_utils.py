"""Log utils."""
import sys
from enum import Enum

from loguru import logger


class LogLevel(Enum):
    """LogLevel."""

    ERROR = 0
    INFO = 1
    DEBUG = 2


LOGGER_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{message}</level>"

LOGGER_FORMAT_DEBUG = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>\n"
    "{message}"
)


def set_logger(log_level: LogLevel = LogLevel.INFO) -> None:
    """Set logger."""
    if log_level == LogLevel.DEBUG:
        logger.add(sys.stderr, format=LOGGER_FORMAT_DEBUG, level="DEBUG")
    elif log_level == LogLevel.INFO:
        logger.add(sys.stderr, format=LOGGER_FORMAT, level="INFO")
    elif log_level == LogLevel.ERROR:
        logger.add(sys.stderr, format=LOGGER_FORMAT, level="ERROR")
    else:
        raise ValueError(f"Invalid debug mode: {log_level}")

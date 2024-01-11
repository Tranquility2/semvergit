"""Log utils."""
import sys
from enum import Enum

from loguru import logger


class LogMode(Enum):
    """Log mode."""

    DEBUG = "DEBUG"
    STANDARD = "STANDARD"
    QUIET = "QUIET"


LOGGER_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{message}</level>"

LOGGER_FORMAT_DEBUG = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>\n"
    "{message}"
)


def set_logger(log_mode: LogMode = LogMode.STANDARD) -> None:
    """Set logger."""
    if log_mode == LogMode.DEBUG:
        logger.add(sys.stderr, format=LOGGER_FORMAT_DEBUG, level="DEBUG")
    elif log_mode == LogMode.STANDARD:
        logger.add(sys.stderr, format=LOGGER_FORMAT, level="INFO")
    elif log_mode == LogMode.QUIET:
        logger.add(sys.stderr, format=LOGGER_FORMAT, level="ERROR")
    else:
        raise ValueError(f"Invalid debug mode: {log_mode}")

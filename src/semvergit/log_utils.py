"""Log utils."""
import sys

from loguru import logger

LOGGER_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{message}</level>"

LOGGER_FORMAT_DEBUG = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>\n"
    "{message}"
)


def set_logger(debug: bool = False) -> None:
    """Set logger."""
    if debug:
        logger.add(sys.stderr, format=LOGGER_FORMAT_DEBUG, level="DEBUG")
    else:
        logger.add(sys.stderr, format=LOGGER_FORMAT, level="INFO")

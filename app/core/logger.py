import logging
import sys
from typing import Optional

LOG_LEVELS = {"DEBUG": "🔍", "INFO": "ℹ️", "WARNING": "⚠️", "ERROR": "❌", "CRITICAL": "🚨"}


class CustomFormatter(logging.Formatter):
    """Custom formatter adding emojis and colors to logs"""

    def format(self, record):
        level_emoji = LOG_LEVELS.get(record.levelname, "")
        record.levelname = f"{level_emoji} {record.levelname}"
        return super().format(record)


def setup_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Creates a logger with consistent formatting and configuration"""
    logger = logging.getLogger(name)

    logger.propagate = False

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)

        formatter = CustomFormatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    logger.setLevel(level or logging.INFO)

    return logger

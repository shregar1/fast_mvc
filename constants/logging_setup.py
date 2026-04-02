"""Configure loguru once from ``LOG_LEVEL`` (read after ``load_dotenv()``)."""

from __future__ import annotations

import os
import sys
from typing import Final

from loguru import logger

_VALID: Final[frozenset[str]] = frozenset(
    {"TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"}
)


def resolve_log_level() -> str:
    raw = (os.getenv("LOG_LEVEL") or "INFO").strip().upper()
    return raw if raw in _VALID else "INFO"


def configure_loguru() -> None:
    """Remove default handlers and add stderr sink filtered by ``LOG_LEVEL``."""
    level = resolve_log_level()
    logger.remove()
    logger.add(
        sys.stderr,
        level=level,
        colorize=True,
        format=(
            "<green>{time:MMMM-D-YYYY}</green> | <black>{time:HH:mm:ss}</black> | "
            "<level>{level}</level> | <cyan>{message}</cyan> | "
            "<magenta>{name}:{function}:{line}</magenta> | "
            "<yellow>{extra}</yellow>"
        ),
    )

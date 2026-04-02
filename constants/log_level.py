"""Logger method names for :func:`getattr` on ``loguru.logger`` (and similar APIs)."""

from typing import Final


class LogLevelName:
    """String names matching ``logger.<name>(...)`` on :class:`loguru.Logger`."""

    DEBUG: Final[str] = "debug"
    INFO: Final[str] = "info"
    WARNING: Final[str] = "warning"
    ERROR: Final[str] = "error"

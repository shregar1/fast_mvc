"""Structured logging helper.

Provides :func:`log_event` used by controllers and services for
structured audit / observability events.
"""

from __future__ import annotations

from typing import Any

from start_utils import logger


def log_event(
    event: str,
    *,
    level: str = "info",
    **kwargs: Any,
) -> None:
    """Emit a structured log event.

    Args:
        event: Dot-separated event name (e.g. ``login.success``).
        level: Log level – ``info``, ``warning``, ``error``, ``debug``.
        **kwargs: Arbitrary key-value pairs attached to the log record.
    """
    bound = logger.bind(event=event, **kwargs)
    getattr(bound, level, bound.info)(event)


__all__ = ["log_event"]

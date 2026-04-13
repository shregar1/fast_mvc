"""Webhook event dispatcher.

Dispatches domain events to registered webhook endpoints. Falls back
to a structured log when the webhook subsystem is not configured.
"""

from __future__ import annotations

from typing import Any, Optional

from start_utils import logger


def dispatch_webhook_event(
    session: Any,
    event_type: str,
    event_id: str,
    payload: dict[str, Any],
    *,
    user_id: Optional[int] = None,
) -> None:
    """Dispatch a webhook event.

    Args:
        session: SQLAlchemy session for persisting webhook delivery records.
        event_type: Dot-separated event type (e.g. ``user.created``).
        event_id: Unique event ID (ULID or UUID).
        payload: Event payload dictionary.
        user_id: Optional user ID associated with the event.
    """
    try:
        from fast_platform.messaging.webhooks import dispatch  # type: ignore

        dispatch(
            session=session,
            event_type=event_type,
            event_id=event_id,
            payload=payload,
            user_id=user_id,
        )
    except ImportError:
        logger.bind(
            event_type=event_type,
            event_id=event_id,
            user_id=user_id,
        ).info("webhook.dispatched (provider not configured)")
    except Exception as exc:
        logger.warning("Webhook dispatch failed for %s: %s", event_type, exc)


__all__ = ["dispatch_webhook_event"]

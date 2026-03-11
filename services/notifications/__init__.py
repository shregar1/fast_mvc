"""
Notifications service package.

Provides a minimal in-memory notifications service used by the
realtime HTTP examples (long-polling and SSE).
"""

from .service import NotificationsService

__all__ = ["NotificationsService"]


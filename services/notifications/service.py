"""
Simple in-memory notifications service used for realtime HTTP examples.

This is intentionally minimal and not meant for production-scale workloads.
"""

import asyncio
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque, List, Optional

from loguru import logger


@dataclass
class Notification:
    id: int
    message: str
    created_at: datetime


class NotificationsService:
    """
    Keeps a small in-memory buffer of notifications for demo purposes.
    """

    def __init__(self, max_items: int = 100) -> None:
        self._max_items = max_items
        self._items: Deque[Notification] = deque(maxlen=max_items)
        self._next_id: int = 1
        self._lock = asyncio.Lock()

    async def publish(self, message: str) -> Notification:
        """
        Publish a new notification.
        """
        async with self._lock:
            item = Notification(
                id=self._next_id,
                message=message,
                created_at=datetime.utcnow(),
            )
            self._next_id += 1
            self._items.append(item)
            logger.debug(f"Published notification {item.id}: {item.message}")
            return item

    async def list_since(self, last_id: int) -> List[Notification]:
        """
        Return notifications with id > last_id.
        """
        async with self._lock:
            return [n for n in self._items if n.id > last_id]

    async def long_poll(self, last_id: int, timeout_seconds: int = 25) -> List[Notification]:
        """
        Long-poll for new notifications.

        Returns as soon as there is at least one notification newer than last_id,
        or after timeout_seconds.
        """
        deadline = asyncio.get_event_loop().time() + timeout_seconds

        while True:
            items = await self.list_since(last_id)
            if items:
                return items

            remaining = deadline - asyncio.get_event_loop().time()
            if remaining <= 0:
                return []

            await asyncio.sleep(min(1.0, remaining))


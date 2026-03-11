"""
In-memory WebSocket channels hub.

Keeps track of connected clients per topic and allows broadcasting messages.
"""

from typing import Dict, Set

from fastapi import WebSocket
from loguru import logger


class ChannelsHub:
    """
    Tracks WebSocket connections per topic and dispatches messages.
    """

    def __init__(self) -> None:
        self._topics: Dict[str, Set[WebSocket]] = {}

    async def connect(self, topic: str, ws: WebSocket) -> None:
        await ws.accept()
        self._topics.setdefault(topic, set()).add(ws)
        logger.debug(f"WebSocket joined topic {topic}")

    def disconnect(self, topic: str, ws: WebSocket) -> None:
        if topic in self._topics:
            self._topics[topic].discard(ws)
            if not self._topics[topic]:
                del self._topics[topic]
        logger.debug(f"WebSocket left topic {topic}")

    async def broadcast(self, topic: str, message: str) -> None:
        for ws in list(self._topics.get(topic, set())):
            try:
                await ws.send_text(message)
            except Exception as exc:
                logger.warning(f"Failed to send message on topic {topic}: {exc}")
                self.disconnect(topic, ws)


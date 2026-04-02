"""WebSocket utility functions."""

from __future__ import annotations

from typing import Any, AsyncGenerator, Tuple, Callable

from fastapi import WebSocket, WebSocketDisconnect


class WebSocketStreamHelper:
    """Helper class for WebSocket streaming operations."""

    @staticmethod
    async def stream_frames(
        ws: WebSocket,
        gen: AsyncGenerator[Tuple[str, Any], None],
        snapshot_serializer: Callable[[Any], Any],
        update_serializer: Callable[[Any], Any],
    ) -> None:
        """Helper to stream snapshot + update frames over a WebSocket.

        Expects the generator to yield (frame_type, payload) tuples where
        frame_type is "snapshot" or "update".
        """
        await ws.accept()
        try:
            async for frame_type, payload in gen:
                if frame_type == "snapshot":
                    await ws.send_json(snapshot_serializer(payload))
                else:
                    await ws.send_json(update_serializer(payload))
        except WebSocketDisconnect:
            return


__all__ = ["WebSocketStreamHelper"]

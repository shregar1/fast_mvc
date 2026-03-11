"""
Realtime HTTP examples: long-polling and Server-Sent Events (SSE).

These endpoints are meant as reference implementations for teams that
want to build realtime APIs without WebSockets.
"""

import asyncio
from typing import Any, AsyncGenerator, Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from services.notifications import NotificationsService


router = APIRouter(prefix="/notifications", tags=["Notifications"])


def get_notifications_service() -> NotificationsService:
    # Simple singleton-ish service per process
    # In production, replace with a DI-backed instance plugged into Redis/Kafka.
    if not hasattr(get_notifications_service, "_svc"):
        setattr(get_notifications_service, "_svc", NotificationsService())
    return getattr(get_notifications_service, "_svc")


@router.get("/long-poll", summary="Long-poll for notifications")
async def long_poll_notifications(
    last_event_id: int = Query(0, ge=0),
    timeout: int = Query(25, ge=1, le=60),
    service: NotificationsService = Depends(get_notifications_service),
) -> Dict[str, Any]:
    """
    Long-poll endpoint that waits for new notifications.

    - Client sends lastEventId it has seen.
    - Server waits up to `timeout` seconds for new events.
    - Responds immediately if events are available.
    """
    items = await service.long_poll(last_event_id, timeout_seconds=timeout)
    events = [
        {
            "id": n.id,
            "message": n.message,
            "createdAt": n.created_at.isoformat() + "Z",
        }
        for n in items
    ]
    new_last_id = events[-1]["id"] if events else last_event_id
    return {
        "events": events,
        "lastEventId": new_last_id,
    }


async def _sse_stream(
    service: NotificationsService,
    last_event_id: int,
) -> AsyncGenerator[bytes, None]:
    """
    Basic SSE stream that periodically emits notifications.
    """
    current_id = last_event_id
    while True:
        items = await service.long_poll(current_id, timeout_seconds=15)
        for n in items:
            current_id = n.id
            payload = {
                "id": n.id,
                "message": n.message,
                "createdAt": n.created_at.isoformat() + "Z",
            }
            data = f"event: notification\ndata: {payload}\n\n"
            yield data.encode("utf-8")
        # Heartbeat
        if not items:
            yield b": keep-alive\n\n"
        await asyncio.sleep(1.0)


@router.get("/sse", summary="Server-Sent Events stream")
async def notifications_sse(
    last_event_id: int = Query(0, ge=0),
    service: NotificationsService = Depends(get_notifications_service),
) -> StreamingResponse:
    """
    SSE endpoint streaming notifications as they arrive.
    """
    generator = _sse_stream(service, last_event_id)
    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


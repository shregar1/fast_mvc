"""
WebSocket channels hub.

Provides a /channels/ws/{topic} endpoint where clients can connect
via WebSocket and broadcast messages to all peers subscribed to that topic.
"""

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from services.channels import ChannelsHub


router = APIRouter(prefix="/channels", tags=["Channels"])


def get_hub() -> ChannelsHub:
    if not hasattr(get_hub, "_hub"):
        setattr(get_hub, "_hub", ChannelsHub())
    return getattr(get_hub, "_hub")


@router.websocket("/ws/{topic}")
async def ws_topic(websocket: WebSocket, topic: str, hub: ChannelsHub = Depends(get_hub)) -> None:
    """
    WebSocket endpoint for topic-based channels.
    """
    await hub.connect(topic, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await hub.broadcast(topic, data)
    except WebSocketDisconnect:
        hub.disconnect(topic, websocket)


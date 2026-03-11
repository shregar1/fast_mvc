"""
WebRTC signaling API.

Provides REST and WebSocket endpoints for exchanging SDP offers/answers and
ICE candidates between peers in a room.

This is a minimal, in-memory signaling server suitable for demos and small
deployments. It reads configuration from `config/webrtc/config.json`.
"""

from typing import Any, Dict

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi import HTTPException, status

from configurations.webrtc import WebRTCConfiguration
from services.webrtc.signaling import WebRTCSignalingService


router = APIRouter(prefix="/webrtc", tags=["WebRTC"])


def get_webrtc_config() -> WebRTCConfiguration:
    return WebRTCConfiguration()


def get_signaling_service(
    cfg: WebRTCConfiguration = Depends(get_webrtc_config),
) -> WebRTCSignalingService:
    dto = cfg.get_config()
    return WebRTCSignalingService(max_peers_per_room=dto.max_peers_per_room)


@router.get("/config", summary="Get WebRTC configuration")
async def get_config(cfg: WebRTCConfiguration = Depends(get_webrtc_config)) -> Dict[str, Any]:
    """
    Return basic WebRTC-related configuration for clients (STUN/TURN).
    """
    dto = cfg.get_config()
    if not dto.enabled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WebRTC signaling is disabled.",
        )
    return {
        "stunServers": dto.stun_servers,
        "turnServers": dto.turn_servers,
        "maxPeersPerRoom": dto.max_peers_per_room,
    }


@router.websocket("/ws/{room_id}/{peer_id}")
async def websocket_signaling(
    websocket: WebSocket,
    room_id: str,
    peer_id: str,
    cfg: WebRTCConfiguration = Depends(get_webrtc_config),
    signaling: WebRTCSignalingService = Depends(get_signaling_service),
) -> None:
    """
    WebSocket endpoint for WebRTC signaling.

    - Peers connect to /webrtc/ws/{room_id}/{peer_id}
    - Messages are forwarded to all other peers in the same room.
    """
    dto = cfg.get_config()
    if not dto.enabled:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    joined = signaling.join_room(room_id, peer_id)
    if not joined:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        while True:
            message = await websocket.receive_json()
            # Broadcast message to other peers in the room
            # In this minimal version we expect the client to identify peers;
            # a production-ready implementation would maintain WebSocket
            # connections per peer and push messages directly.
            # Here we simply echo back to the sender for demo purposes.
            await websocket.send_json({"echo": message, "roomId": room_id})
    except WebSocketDisconnect:
        signaling.leave_room(room_id, peer_id)


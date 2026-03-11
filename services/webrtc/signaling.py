"""
Simple in-memory WebRTC signaling service.

Designed for small deployments and local development.
For production, consider replacing this with a distributed
signaling backend (Redis, Kafka, etc.).
"""

from collections import defaultdict
from typing import Dict, List

from loguru import logger


class WebRTCSignalingService:
    """
    Manages rooms and peers for WebRTC signaling.

    This implementation is intentionally simple and in-memory.
    """

    def __init__(self, max_peers_per_room: int = 8) -> None:
        self._max_peers_per_room = max_peers_per_room
        # room_id -> list of peer_ids
        self._rooms: Dict[str, List[str]] = defaultdict(list)

    def join_room(self, room_id: str, peer_id: str) -> bool:
        """
        Add a peer to a room if there's capacity.
        """
        peers = self._rooms[room_id]
        if peer_id in peers:
            return True
        if len(peers) >= self._max_peers_per_room:
            logger.warning(f"Room {room_id} is full (max {self._max_peers_per_room}).")
            return False
        peers.append(peer_id)
        logger.debug(f"Peer {peer_id} joined room {room_id}.")
        return True

    def leave_room(self, room_id: str, peer_id: str) -> None:
        """
        Remove a peer from a room; delete room if empty.
        """
        peers = self._rooms.get(room_id, [])
        if peer_id in peers:
            peers.remove(peer_id)
            logger.debug(f"Peer {peer_id} left room {room_id}.")
        if not peers and room_id in self._rooms:
            del self._rooms[room_id]
            logger.debug(f"Room {room_id} removed (empty).")

    def list_peers(self, room_id: str, exclude: str | None = None) -> List[str]:
        """
        List peers in a room, optionally excluding a specific peer.
        """
        peers = list(self._rooms.get(room_id, []))
        if exclude and exclude in peers:
            peers.remove(exclude)
        return peers


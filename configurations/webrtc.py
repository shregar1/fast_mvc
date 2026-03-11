"""
WebRTC Configuration Module.

Provides a singleton configuration manager for WebRTC signaling settings.
Configuration is loaded from a JSON file and exposed via a Pydantic DTO.
"""

import json
from typing import Optional

from dtos.configurations.webrtc import WebRTCConfigurationDTO
from start_utils import logger


class WebRTCConfiguration:
    """
    Singleton configuration manager for WebRTC signaling settings.

    Configuration is loaded from `config/webrtc/config.json`.
    """

    _instance: Optional["WebRTCConfiguration"] = None

    def __new__(cls) -> "WebRTCConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load WebRTC configuration from JSON file.
        """
        try:
            with open("config/webrtc/config.json") as file:
                self.config = json.load(file)
            logger.debug("WebRTC config loaded successfully.")
        except FileNotFoundError:
            logger.debug("WebRTC config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding WebRTC config file.")
            self.config = {}

    def get_config(self) -> WebRTCConfigurationDTO:
        """
        Get WebRTC configuration as a validated DTO.
        """
        return WebRTCConfigurationDTO(
            enabled=bool(self.config.get("enabled", False)),
            stun_servers=self.config.get("stun_servers", []),
            turn_servers=self.config.get("turn_servers", []),
            max_peers_per_room=self.config.get("max_peers_per_room", 8),
        )


"""
Channels Configuration Module.

Provides a singleton configuration manager for pub-sub channels settings.
"""

import json
from typing import Optional

from dtos.configurations.channels import ChannelsConfigurationDTO
from start_utils import logger


class ChannelsConfiguration:
    """
    Singleton configuration manager for channels settings.

    Configuration is loaded from `config/channels/config.json`.
    """

    _instance: Optional["ChannelsConfiguration"] = None

    def __new__(cls) -> "ChannelsConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load channels configuration from JSON file.
        """
        try:
            with open("config/channels/config.json") as file:
                self.config = json.load(file)
            logger.debug("Channels config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Channels config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding channels config file.")
            self.config = {}

    def get_config(self) -> ChannelsConfigurationDTO:
        """
        Get channels configuration as a validated DTO.
        """
        return ChannelsConfigurationDTO(
            backend=self.config.get("backend", "none"),
            topics=self.config.get("topics", []),
        )


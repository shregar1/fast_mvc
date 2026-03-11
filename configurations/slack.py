"""
Slack Configuration Module.

Provides a singleton configuration manager for Slack/chat settings.
"""

import json
from typing import Optional

from dtos.configurations.slack import SlackConfigurationDTO
from start_utils import logger


class SlackConfiguration:
    """
    Singleton configuration manager for Slack settings.

    Configuration is loaded from `config/slack/config.json`.
    """

    _instance: Optional["SlackConfiguration"] = None

    def __new__(cls) -> "SlackConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load Slack configuration from JSON file.
        """
        try:
            with open("config/slack/config.json") as file:
                self.config = json.load(file)
            logger.debug("Slack config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Slack config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding Slack config file.")
            self.config = {}

    def get_config(self) -> SlackConfigurationDTO:
        """
        Get Slack configuration as a validated DTO.
        """
        return SlackConfigurationDTO(
            enabled=bool(self.config.get("enabled", False)),
            webhook_url=self.config.get("webhook_url"),
            bot_token=self.config.get("bot_token"),
            default_channel=self.config.get("default_channel"),
        )


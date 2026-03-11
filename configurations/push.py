"""
Push Notification Configuration Module.

Provides a singleton configuration manager for push (APNS/FCM) settings.
"""

import json
from typing import Optional

from dtos.configurations.push import PushConfigurationDTO
from start_utils import logger


class PushConfiguration:
    """
    Singleton configuration manager for push notification settings.

    Configuration is loaded from `config/push/config.json`.
    """

    _instance: Optional["PushConfiguration"] = None

    def __new__(cls) -> "PushConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load push notification configuration from JSON file.
        """
        try:
            with open("config/push/config.json") as file:
                self.config = json.load(file)
            logger.debug("Push notification config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Push notification config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding push notification config file.")
            self.config = {}

    def get_config(self) -> PushConfigurationDTO:
        """
        Get push configuration as a validated DTO.
        """
        return PushConfigurationDTO(
            apns=self.config.get("apns", {}) or {},
            fcm=self.config.get("fcm", {}) or {},
        )


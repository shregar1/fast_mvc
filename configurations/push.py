"""
Push Notification Configuration Module.

Provides a singleton configuration manager for push (APNS/FCM) settings.
"""

import json
import os
from typing import Optional

from dtos.configurations.push import PushConfigurationDTO
from start_utils import logger


class PushConfiguration:
    """
    Singleton configuration manager for push notification settings.

    Configuration is loaded from `config/push/config.json` and then
    environment variable overrides are applied.
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
        Load push notification configuration from JSON file and env.
        """
        cfg: dict = {}
        try:
            with open("config/push/config.json") as file:
                cfg = json.load(file)
            logger.debug("Push notification config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Push notification config file not found.")
        except json.JSONDecodeError:
            logger.debug("Error decoding push notification config file.")

        # Apply environment overrides
        apns_cfg = cfg.setdefault("apns", {})
        if (v := os.getenv("APNS_ENABLED")) is not None:
            apns_cfg["enabled"] = v.strip().lower() in {"1", "true", "yes", "on"}
        if (v := os.getenv("APNS_KEY_ID")) is not None:
            apns_cfg["key_id"] = v
        if (v := os.getenv("APNS_TEAM_ID")) is not None:
            apns_cfg["team_id"] = v
        if (v := os.getenv("APNS_BUNDLE_ID")) is not None:
            apns_cfg["bundle_id"] = v
        if (v := os.getenv("APNS_PRIVATE_KEY_PATH")) is not None:
            apns_cfg["private_key_path"] = v
        if (v := os.getenv("APNS_USE_SANDBOX")) is not None:
            apns_cfg["use_sandbox"] = v.strip().lower() in {
                "1",
                "true",
                "yes",
                "on",
            }

        fcm_cfg = cfg.setdefault("fcm", {})
        if (v := os.getenv("FCM_ENABLED")) is not None:
            fcm_cfg["enabled"] = v.strip().lower() in {"1", "true", "yes", "on"}
        if (v := os.getenv("FCM_SERVER_KEY")) is not None:
            fcm_cfg["server_key"] = v
        if (v := os.getenv("FCM_PROJECT_ID")) is not None:
            fcm_cfg["project_id"] = v

        self.config = cfg

    def get_config(self) -> PushConfigurationDTO:
        """
        Get push configuration as a validated DTO.
        """
        return PushConfigurationDTO(
            apns=self.config.get("apns", {}) or {},
            fcm=self.config.get("fcm", {}) or {},
        )


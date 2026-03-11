"""
Datadog Configuration Module.

Provides a singleton configuration manager for Datadog settings.
"""

import json
from typing import Optional

from dtos.configurations.datadog import DatadogConfigurationDTO
from start_utils import logger


class DatadogConfiguration:
    """
    Singleton configuration manager for Datadog settings.

    Configuration is loaded from `config/datadog/config.json`.
    """

    _instance: Optional["DatadogConfiguration"] = None

    def __new__(cls) -> "DatadogConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load Datadog configuration from JSON file.
        """
        try:
            with open("config/datadog/config.json") as file:
                self.config = json.load(file)
            logger.debug("Datadog config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Datadog config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding Datadog config file.")
            self.config = {}

    def get_config(self) -> DatadogConfigurationDTO:
        """
        Get Datadog configuration as a validated DTO.
        """
        return DatadogConfigurationDTO(
            enabled=bool(self.config.get("enabled", False)),
            api_key=self.config.get("api_key"),
            app_key=self.config.get("app_key"),
            env=self.config.get("env", "development"),
            service=self.config.get("service", "fastmvc-api"),
            version=self.config.get("version"),
            agent_host=self.config.get("agent_host", "127.0.0.1"),
            agent_port=int(self.config.get("agent_port", 8126)),
        )


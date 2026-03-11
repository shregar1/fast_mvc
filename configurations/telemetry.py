"""
Telemetry Configuration Module.

Provides a singleton configuration manager for OpenTelemetry settings.
"""

import json
from typing import Optional

from dtos.configurations.telemetry import TelemetryConfigurationDTO
from start_utils import logger


class TelemetryConfiguration:
    """
    Singleton configuration manager for telemetry settings.

    Configuration is loaded from `config/telemetry/config.json`.
    """

    _instance: Optional["TelemetryConfiguration"] = None

    def __new__(cls) -> "TelemetryConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load telemetry configuration from JSON file.
        """
        try:
            with open("config/telemetry/config.json") as file:
                self.config = json.load(file)
            logger.debug("Telemetry config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Telemetry config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding telemetry config file.")
            self.config = {}

    def get_config(self) -> TelemetryConfigurationDTO:
        """
        Get telemetry configuration as a validated DTO.
        """
        return TelemetryConfigurationDTO(
            enabled=bool(self.config.get("enabled", False)),
            exporter=self.config.get("exporter", "otlp"),
            endpoint=self.config.get("endpoint"),
            protocol=self.config.get("protocol", "grpc"),
            service_name=self.config.get("service_name", "fastmvc-api"),
            environment=self.config.get("environment", "development"),
        )


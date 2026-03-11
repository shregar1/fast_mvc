"""
ScyllaDB Configuration Module.

Provides a singleton configuration manager for ScyllaDB settings.
"""

import json
from typing import Optional

from dtos.configurations.scylla import ScyllaConfigurationDTO
from start_utils import logger


class ScyllaConfiguration:
    """
    Singleton configuration manager for ScyllaDB settings.

    Configuration is loaded from `config/scylla/config.json`.
    """

    _instance: Optional["ScyllaConfiguration"] = None

    def __new__(cls) -> "ScyllaConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load Scylla configuration from JSON file.
        """
        try:
            with open("config/scylla/config.json") as file:
                self.config = json.load(file)
            logger.debug("Scylla config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Scylla config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding Scylla config file.")
            self.config = {}

    def get_config(self) -> ScyllaConfigurationDTO:
        """
        Get Scylla configuration as a validated DTO.
        """
        contact_points = self.config.get("contact_points", ["127.0.0.1"])
        if isinstance(contact_points, str):
            contact_points = [contact_points]
        return ScyllaConfigurationDTO(
            enabled=self.config.get("enabled", False),
            contact_points=contact_points,
            port=int(self.config.get("port", 9042)),
            keyspace=self.config.get("keyspace"),
        )


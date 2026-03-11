"""
Cassandra Configuration Module.

Provides a singleton configuration manager for Cassandra settings.
"""

import json
from typing import Optional

from dtos.configurations.cassandra import CassandraConfigurationDTO
from start_utils import logger


class CassandraConfiguration:
    """
    Singleton configuration manager for Cassandra settings.

    Configuration is loaded from `config/cassandra/config.json`.
    """

    _instance: Optional["CassandraConfiguration"] = None

    def __new__(cls) -> "CassandraConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load Cassandra configuration from JSON file.
        """
        try:
            with open("config/cassandra/config.json") as file:
                self.config = json.load(file)
            logger.debug("Cassandra config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Cassandra config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding Cassandra config file.")
            self.config = {}

    def get_config(self) -> CassandraConfigurationDTO:
        """
        Get Cassandra configuration as a validated DTO.
        """
        contact_points = self.config.get("contact_points", ["127.0.0.1"])
        if isinstance(contact_points, str):
            contact_points = [contact_points]
        return CassandraConfigurationDTO(
            enabled=self.config.get("enabled", False),
            contact_points=contact_points,
            port=int(self.config.get("port", 9042)),
            keyspace=self.config.get("keyspace"),
        )


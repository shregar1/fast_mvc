"""
MongoDB Configuration Module.

Provides a singleton configuration manager for MongoDB settings.
"""

import json
from typing import Optional

from dtos.configurations.mongo import MongoConfigurationDTO
from start_utils import logger


class MongoConfiguration:
    """
    Singleton configuration manager for MongoDB settings.

    Configuration is loaded from `config/mongo/config.json`.
    """

    _instance: Optional["MongoConfiguration"] = None

    def __new__(cls) -> "MongoConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load MongoDB configuration from JSON file.
        """
        try:
            with open("config/mongo/config.json") as file:
                self.config = json.load(file)
            logger.debug("MongoDB config loaded successfully.")
        except FileNotFoundError:
            logger.debug("MongoDB config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding MongoDB config file.")
            self.config = {}

    def get_config(self) -> MongoConfigurationDTO:
        """
        Get MongoDB configuration as a validated DTO.
        """
        return MongoConfigurationDTO(
            enabled=self.config.get("enabled", False),
            uri=self.config.get("uri", "mongodb://localhost:27017"),
            database=self.config.get("database", "fastmvc"),
        )


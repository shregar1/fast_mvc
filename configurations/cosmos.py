"""
Cosmos DB Configuration Module.

Provides a singleton configuration manager for Azure Cosmos DB settings.
"""

import json
from typing import Optional

from dtos.configurations.cosmos import CosmosConfigurationDTO
from start_utils import logger


class CosmosConfiguration:
    """
    Singleton configuration manager for Cosmos DB settings.

    Configuration is loaded from `config/cosmos/config.json`.
    """

    _instance: Optional["CosmosConfiguration"] = None

    def __new__(cls) -> "CosmosConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load Cosmos DB configuration from JSON file.
        """
        try:
            with open("config/cosmos/config.json") as file:
                self.config = json.load(file)
            logger.debug("Cosmos config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Cosmos config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding Cosmos config file.")
            self.config = {}

    def get_config(self) -> CosmosConfigurationDTO:
        """
        Get Cosmos DB configuration as a validated DTO.
        """
        return CosmosConfigurationDTO(
            enabled=self.config.get("enabled", False),
            account_uri=self.config.get("account_uri", ""),
            account_key=self.config.get("account_key", ""),
            database=self.config.get("database", "fastmvc"),
        )


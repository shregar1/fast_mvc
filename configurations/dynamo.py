"""
DynamoDB Configuration Module.

Provides a singleton configuration manager for DynamoDB settings.
"""

import json
from typing import Optional

from dtos.configurations.dynamo import DynamoConfigurationDTO
from start_utils import logger


class DynamoConfiguration:
    """
    Singleton configuration manager for DynamoDB settings.

    Configuration is loaded from `config/dynamo/config.json`.
    """

    _instance: Optional["DynamoConfiguration"] = None

    def __new__(cls) -> "DynamoConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load DynamoDB configuration from JSON file.
        """
        try:
            with open("config/dynamo/config.json") as file:
                self.config = json.load(file)
            logger.debug("Dynamo config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Dynamo config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding Dynamo config file.")
            self.config = {}

    def get_config(self) -> DynamoConfigurationDTO:
        """
        Get DynamoDB configuration as a validated DTO.
        """
        return DynamoConfigurationDTO(
            enabled=self.config.get("enabled", False),
            region=self.config.get("region", "us-east-1"),
            table_prefix=self.config.get("table_prefix"),
        )


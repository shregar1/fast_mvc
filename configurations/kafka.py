"""
Kafka Configuration Module.

Provides a singleton configuration manager for Kafka settings.
"""

import json
from typing import Optional

from dtos.configurations.kafka import KafkaConfigurationDTO
from start_utils import logger


class KafkaConfiguration:
    """
    Singleton configuration manager for Kafka settings.

    Configuration is loaded from `config/kafka/config.json`.
    """

    _instance: Optional["KafkaConfiguration"] = None

    def __new__(cls) -> "KafkaConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load Kafka configuration from JSON file.
        """
        try:
            with open("config/kafka/config.json") as file:
                self.config = json.load(file)
            logger.debug("Kafka config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Kafka config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding Kafka config file.")
            self.config = {}

    def get_config(self) -> KafkaConfigurationDTO:
        """
        Get Kafka configuration as a validated DTO.
        """
        return KafkaConfigurationDTO(
            enabled=self.config.get("enabled", False),
            bootstrap_servers=self.config.get("bootstrap_servers", "localhost:9092"),
            group_id=self.config.get("group_id", "fastmvc-worker"),
            topics=self.config.get("topics", ["notifications"]),
            enable_auto_commit=self.config.get("enable_auto_commit", True),
        )


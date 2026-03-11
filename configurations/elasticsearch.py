"""
Elasticsearch Configuration Module.

Provides a singleton configuration manager for Elasticsearch settings.
"""

import json
from typing import Optional

from dtos.configurations.elasticsearch import ElasticsearchConfigurationDTO
from start_utils import logger


class ElasticsearchConfiguration:
    """
    Singleton configuration manager for Elasticsearch settings.

    Configuration is loaded from `config/elasticsearch/config.json`.
    """

    _instance: Optional["ElasticsearchConfiguration"] = None

    def __new__(cls) -> "ElasticsearchConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load Elasticsearch configuration from JSON file.
        """
        try:
            with open("config/elasticsearch/config.json") as file:
                self.config = json.load(file)
            logger.debug("Elasticsearch config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Elasticsearch config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding Elasticsearch config file.")
            self.config = {}

    def get_config(self) -> ElasticsearchConfigurationDTO:
        """
        Get Elasticsearch configuration as a validated DTO.
        """
        hosts = self.config.get("hosts", ["http://localhost:9200"])
        if isinstance(hosts, str):
            hosts = [hosts]
        return ElasticsearchConfigurationDTO(
            enabled=self.config.get("enabled", False),
            hosts=hosts,
            username=self.config.get("username"),
            password=self.config.get("password"),
            verify_certs=bool(self.config.get("verify_certs", True)),
        )


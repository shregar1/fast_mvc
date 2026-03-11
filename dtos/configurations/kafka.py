"""
DTOs for Kafka configuration settings.
"""

from typing import List

from pydantic import BaseModel


class KafkaConfigurationDTO(BaseModel):
    """
    DTO for Kafka configuration.
    """

    enabled: bool = False
    bootstrap_servers: str = "localhost:9092"
    group_id: str = "fastmvc-worker"
    topics: List[str] = ["notifications"]
    enable_auto_commit: bool = True


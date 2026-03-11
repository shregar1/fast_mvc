"""
DTO for Datadog configuration settings.
"""

from typing import Optional

from pydantic import BaseModel


class DatadogConfigurationDTO(BaseModel):
    """
    DTO for Datadog APM / metrics configuration.
    """

    enabled: bool = False
    api_key: Optional[str] = None
    app_key: Optional[str] = None
    env: str = "development"
    service: str = "fastmvc-api"
    version: Optional[str] = None
    agent_host: str = "127.0.0.1"
    agent_port: int = 8126


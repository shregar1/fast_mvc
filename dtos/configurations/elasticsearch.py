"""
DTO for Elasticsearch configuration settings.
"""

from typing import List, Optional

from pydantic import BaseModel


class ElasticsearchConfigurationDTO(BaseModel):
    """
    DTO for Elasticsearch configuration.

    Fields:
        enabled (bool): Whether Elasticsearch integration is enabled.
        hosts (list[str]): List of node URLs (e.g. http://localhost:9200).
        username (str | None): Optional basic auth username.
        password (str | None): Optional basic auth password.
        verify_certs (bool): Whether to verify TLS certificates.
    """

    enabled: bool = False
    hosts: List[str] = ["http://localhost:9200"]
    username: Optional[str] = None
    password: Optional[str] = None
    verify_certs: bool = True


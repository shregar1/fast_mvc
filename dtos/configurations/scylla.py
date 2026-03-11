"""
DTO for ScyllaDB configuration settings.
"""

from typing import List, Optional

from pydantic import BaseModel


class ScyllaConfigurationDTO(BaseModel):
    """
    DTO for ScyllaDB configuration.

    Fields:
        enabled (bool): Whether ScyllaDB integration is enabled.
        contact_points (list[str]): Cluster contact points.
        port (int): CQL port.
        keyspace (str | None): Optional default keyspace.
    """

    enabled: bool = False
    contact_points: List[str] = ["127.0.0.1"]
    port: int = 9042
    keyspace: Optional[str] = None


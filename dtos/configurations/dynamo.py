"""
DTO for DynamoDB configuration settings.
"""

from typing import Optional

from pydantic import BaseModel


class DynamoConfigurationDTO(BaseModel):
    """
    DTO for DynamoDB configuration.

    Fields:
        enabled (bool): Whether DynamoDB integration is enabled.
        region (str): AWS region name.
        table_prefix (str | None): Optional prefix for logical table names.
    """

    enabled: bool = False
    region: str = "us-east-1"
    table_prefix: Optional[str] = None


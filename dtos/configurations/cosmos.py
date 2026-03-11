"""
DTO for Azure Cosmos DB configuration settings.
"""

from pydantic import BaseModel


class CosmosConfigurationDTO(BaseModel):
    """
    DTO for Cosmos DB configuration.

    Fields:
        enabled (bool): Whether Cosmos DB integration is enabled.
        account_uri (str): Account endpoint URI.
        account_key (str): Primary key or connection key.
        database (str): Default database name.
    """

    enabled: bool = False
    account_uri: str
    account_key: str
    database: str


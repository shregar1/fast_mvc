"""
DTO for MongoDB configuration settings.
"""

from pydantic import BaseModel


class MongoConfigurationDTO(BaseModel):
    """
    DTO for MongoDB configuration.

    Fields:
        enabled (bool): Whether MongoDB integration is enabled.
        uri (str): MongoDB connection URI.
        database (str): Default database name.
    """

    enabled: bool = False
    uri: str
    database: str


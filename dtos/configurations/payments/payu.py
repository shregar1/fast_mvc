"""
PayU configuration DTO.
"""

from typing import Literal, Optional

from pydantic import BaseModel


class PayUConfigDTO(BaseModel):
    """PayU configuration."""

    enabled: bool = False
    merchant_key: Optional[str] = None
    merchant_salt: Optional[str] = None
    environment: Literal["test", "production"] = "test"


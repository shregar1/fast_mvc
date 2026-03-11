"""
PayPal configuration DTO.
"""

from typing import Literal, Optional

from pydantic import BaseModel


class PaypalConfigDTO(BaseModel):
    """PayPal configuration."""

    enabled: bool = False
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    environment: Literal["sandbox", "live"] = "sandbox"


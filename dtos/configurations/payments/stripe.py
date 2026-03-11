"""
Stripe configuration DTO.
"""

from typing import Optional

from pydantic import BaseModel


class StripeConfigDTO(BaseModel):
    """Stripe configuration."""

    enabled: bool = False
    api_key: Optional[str] = None
    webhook_secret: Optional[str] = None
    default_currency: str = "usd"


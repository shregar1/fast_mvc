"""
Razorpay configuration DTO.
"""

from typing import Optional

from pydantic import BaseModel


class RazorpayConfigDTO(BaseModel):
    """Razorpay configuration."""

    enabled: bool = False
    key_id: Optional[str] = None
    key_secret: Optional[str] = None
    default_currency: str = "INR"


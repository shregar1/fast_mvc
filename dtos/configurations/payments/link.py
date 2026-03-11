"""
Generic pay-by-link configuration DTO.
"""

from typing import Optional

from pydantic import BaseModel


class LinkConfigDTO(BaseModel):
    """Generic pay-by-link configuration."""

    enabled: bool = False
    base_url: Optional[str] = None
    api_key: Optional[str] = None


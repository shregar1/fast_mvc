"""Example response payload DTO."""

from typing import Any

from pydantic import BaseModel


class ExampleResponseDataDTO(BaseModel):
    """Response payload for example API endpoints."""

    id: Any = None
    name: str | None = None
    description: str | None = None
    reference_urn: str | None = None

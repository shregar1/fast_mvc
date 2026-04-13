"""Logout request DTO."""

from uuid import uuid4

from pydantic import Field

from dtos.requests.user.abstraction import IRequestUserDTO


class UserLogoutRequestDTO(IRequestUserDTO):
    """DTO for POST /user/logout."""

    reference_urn: str = Field(default_factory=lambda: str(uuid4()))


__all__ = ["UserLogoutRequestDTO"]

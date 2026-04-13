"""Refresh token request DTO."""

from uuid import uuid4

from pydantic import Field, field_validator

from dtos.requests.user.abstraction import IRequestUserDTO


class RefreshTokenRequestDTO(IRequestUserDTO):
    """DTO for POST /user/refresh."""

    reference_urn: str = Field(default_factory=lambda: str(uuid4()))
    refreshToken: str

    @field_validator("refreshToken")
    @classmethod
    def validate_refresh_token(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Refresh token is required.")
        return v.strip()


__all__ = ["RefreshTokenRequestDTO"]

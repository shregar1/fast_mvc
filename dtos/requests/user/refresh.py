"""Refresh token request DTO."""

from pydantic import field_validator

from dtos.requests.user.abstraction import IRequestUserDTO


class RefreshTokenRequestDTO(IRequestUserDTO):
    """DTO for POST /user/refresh."""

    refreshToken: str

    @field_validator("refreshToken")
    @classmethod
    def validate_refresh_token(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Refresh token is required.")
        return v.strip()


__all__ = ["RefreshTokenRequestDTO"]

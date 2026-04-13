"""Reset-password request DTO."""

from uuid import uuid4

from pydantic import Field, field_validator

from dtos.requests.user.abstraction import IRequestUserDTO


class ResetPasswordRequestDTO(IRequestUserDTO):
    """DTO for POST /user/reset-password."""

    reference_urn: str = Field(default_factory=lambda: str(uuid4()))
    token: str
    new_password: str

    @field_validator("token")
    @classmethod
    def validate_token(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Reset token is required.")
        return v.strip()

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if not v:
            raise ValueError("New password is required.")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v


__all__ = ["ResetPasswordRequestDTO"]

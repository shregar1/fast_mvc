"""Forgot-password request DTO."""

from pydantic import field_validator

from dtos.requests.user.abstraction import IRequestUserDTO


class ForgotPasswordRequestDTO(IRequestUserDTO):
    """DTO for POST /user/forgot-password."""

    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Email is required.")
        return v.strip().lower()


__all__ = ["ForgotPasswordRequestDTO"]

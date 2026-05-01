"""Login request DTO."""

from pydantic import field_validator

from dtos.requests.user.abstraction import IRequestUserDTO


class UserLoginRequestDTO(IRequestUserDTO):
    """DTO for POST /user/login."""

    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Email is required.")
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v:
            raise ValueError("Password is required.")
        return v


__all__ = ["UserLoginRequestDTO"]

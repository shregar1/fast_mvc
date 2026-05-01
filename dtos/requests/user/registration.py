"""Registration request DTO."""

from pydantic import field_validator

from dtos.requests.user.abstraction import IRequestUserDTO


class UserRegistrationRequestDTO(IRequestUserDTO):
    """DTO for POST /user/register."""

    email: str
    password: str
    name: str = ""

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
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v


__all__ = ["UserRegistrationRequestDTO"]

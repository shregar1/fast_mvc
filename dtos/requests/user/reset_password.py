"""Reset-password request DTO."""

from pydantic import field_validator

from dtos.requests.user.abstraction import IRequestUserDTO


class ResetPasswordRequestDTO(IRequestUserDTO):
    """DTO for POST /user/reset-password."""

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

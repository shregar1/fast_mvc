"""Phone send-OTP request DTO."""

from pydantic import field_validator

from dtos.requests.user.abstraction import IRequestUserDTO


class PhoneSendOtpRequestDTO(IRequestUserDTO):
    """DTO for POST /user/phone/send-otp."""

    phone: str
    purpose: str = "login"

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Phone number is required.")
        return v.strip()

    @field_validator("purpose")
    @classmethod
    def validate_purpose(cls, v: str) -> str:
        allowed = {"login", "register", "verify_phone", "reset_password"}
        if v not in allowed:
            raise ValueError(f"Purpose must be one of: {', '.join(sorted(allowed))}")
        return v


__all__ = ["PhoneSendOtpRequestDTO"]

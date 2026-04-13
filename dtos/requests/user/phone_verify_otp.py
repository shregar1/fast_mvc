"""Phone verify-OTP request DTO."""

from uuid import uuid4

from pydantic import Field, field_validator

from dtos.requests.user.abstraction import IRequestUserDTO


class PhoneVerifyOtpRequestDTO(IRequestUserDTO):
    """DTO for POST /user/phone/verify-otp."""

    reference_urn: str = Field(default_factory=lambda: str(uuid4()))
    phone: str
    otp: str
    purpose: str = "login"

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Phone number is required.")
        return v.strip()

    @field_validator("otp")
    @classmethod
    def validate_otp(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("OTP is required.")
        return v.strip()

    @field_validator("purpose")
    @classmethod
    def validate_purpose(cls, v: str) -> str:
        allowed = {"login", "register", "verify_phone", "reset_password"}
        if v not in allowed:
            raise ValueError(f"Purpose must be one of: {', '.join(sorted(allowed))}")
        return v


__all__ = ["PhoneVerifyOtpRequestDTO"]

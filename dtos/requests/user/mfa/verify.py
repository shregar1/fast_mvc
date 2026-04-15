"""MFA verify request DTO."""

from dtos.requests.user.abstraction import IRequestUserDTO


class MFAVerifyRequestDTO(IRequestUserDTO):
    """DTO for POST /user/mfa/verify."""

    code: str


__all__ = ["MFAVerifyRequestDTO"]

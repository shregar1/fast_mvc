"""MFA disable request DTO."""

from dtos.requests.user.abstraction import IRequestUserDTO


class MFADisableRequestDTO(IRequestUserDTO):
    """DTO for POST /user/mfa/disable."""

    code: str


__all__ = ["MFADisableRequestDTO"]

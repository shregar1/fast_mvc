"""Verify-MFA request DTO (post-login challenge exchange)."""

from dtos.requests.user.abstraction import IRequestUserDTO


class VerifyMFARequestDTO(IRequestUserDTO):
    """DTO for POST /user/auth/verify-mfa."""

    mfa_challenge_token: str
    code: str


__all__ = ["VerifyMFARequestDTO"]

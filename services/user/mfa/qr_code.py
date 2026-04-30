"""MFA QR-Code Service – render the provisioning URI as a PNG."""

from __future__ import annotations

import io
from typing import Any

from fast_platform.errors import (
    BadInputError,
    NotFoundError,
    ServiceUnavailableError,
    UnauthorizedError,
)
from repositories.user.user_repository import UserRepository
from services.user.abstraction import IUserService

try:
    import qrcode  # type: ignore[import-not-found]
except ImportError:
    qrcode = None  # type: ignore


class MFAQrCodeService(IUserService):
    """Produce a PNG QR code for the user's pending MFA provisioning URI."""

    def __init__(
        self,
        *args: Any,
        user_repository: UserRepository,
        mfa_service: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._user_repository = user_repository
        self._mfa_service = mfa_service

    async def run(self, request_dto: Any = None) -> tuple[bytes, str]:
        """Return ``(png_bytes, mime_type)`` for the pending setup secret."""
        if self.user_id is None:
            raise UnauthorizedError(
                httpStatusCode=401,
                responseMessage="Unauthorized.",
                responseKey="error_authentication_error",
            )
        user = self._user_repository.retrieve_record_by_id(self.user_id)
        if not user:
            raise NotFoundError(
                httpStatusCode=404,
                responseMessage="User not found.",
                responseKey="error_user_not_found",
            )
        if user.mfa_enabled:
            raise BadInputError(
                httpStatusCode=400,
                responseMessage="MFA is already enabled.",
                responseKey="error_bad_input",
            )

        secret = user.mfa_secret
        if not secret:
            raise BadInputError(
                httpStatusCode=400,
                responseMessage="Call POST /mfa/setup first.",
                responseKey="error_bad_input",
            )

        if qrcode is None:
            raise ServiceUnavailableError(
                httpStatusCode=503,
                responseMessage=(
                    "QR code generation not available. Use the provisioningUri from "
                    "POST /mfa/setup to generate a QR client-side."
                ),
                responseKey="error_service_unavailable",
            )

        uri = self._mfa_service.get_provisioning_uri(secret, user.email or "user")
        img = qrcode.make(uri)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf.read(), "image/png"


__all__ = ["MFAQrCodeService"]

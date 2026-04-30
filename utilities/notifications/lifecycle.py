"""Lifecycle email helpers – welcome, verification, password reset.

Functions are ``async`` so controllers can ``await`` them. When the
notification provider is not configured the calls log a warning and
return silently (fire-and-forget semantics).
"""

from __future__ import annotations

from typing import Any, Optional

from constants.default import Default
from fastx_platform.errors import ServiceUnavailableError
from start_utils import logger


async def _send(
    *,
    email: str,
    template: str,
    subject: str,
    kind: str,
    fail_key: str = "error_notification_send_failed",
    **template_vars: Any,
) -> None:
    """Shared send envelope: import provider, dispatch, translate errors."""
    try:
        from fastx_platform.notifications import send_email  # type: ignore

        await send_email(to=email, template=template, subject=subject, **template_vars)
    except ImportError:
        logger.warning(
            "Notification provider not available – skipping %s email to %s", kind, email
        )
        return
    except Exception as err:
        logger.exception("%s email send failed for %s", kind, email)
        raise ServiceUnavailableError(
            httpStatusCode=503,
            responseMessage="Failed to send notification email.",
            responseKey=fail_key,
        ) from err


async def send_welcome_email(email: str) -> None:
    """Send a welcome / onboarding email after registration."""
    await _send(
        email=email,
        template="welcome",
        subject="Welcome!",
        kind="welcome",
    )


async def send_password_reset_email(
    email: str,
    reset_link: str,
    *,
    expires_minutes: int = Default.EMAIL_TOKEN_EXPIRY_MINUTES,
) -> None:
    """Send a password-reset link email."""
    await _send(
        email=email,
        template="password_reset",
        subject="Reset your password",
        kind="password reset",
        context={"reset_link": reset_link, "expires_minutes": expires_minutes},
    )


async def send_verification_email(
    email: str,
    verify_link: str,
    *,
    expires_minutes: int = Default.EMAIL_TOKEN_EXPIRY_MINUTES,
) -> None:
    """Send an email-verification link."""
    await _send(
        email=email,
        template="email_verification",
        subject="Verify your email",
        kind="verification",
        context={"verify_link": verify_link, "expires_minutes": expires_minutes},
    )


# Alias used by controllers/auth/user/account/send_verification_email.py
send_verify_email = send_verification_email

__all__ = [
    "send_welcome_email",
    "send_password_reset_email",
    "send_verification_email",
    "send_verify_email",
]

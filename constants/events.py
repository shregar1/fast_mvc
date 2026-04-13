"""Webhook / domain event type constants."""

from typing import Final


class WebhookEventType:
    """Constants for webhook event types dispatched by the application."""

    USER_CREATED: Final[str] = "user.created"
    USER_UPDATED: Final[str] = "user.updated"
    USER_DELETED: Final[str] = "user.deleted"
    USER_LOGIN: Final[str] = "user.login"
    USER_LOGOUT: Final[str] = "user.logout"
    USER_PASSWORD_RESET: Final[str] = "user.password_reset"
    USER_EMAIL_VERIFIED: Final[str] = "user.email_verified"
    USER_MFA_ENABLED: Final[str] = "user.mfa_enabled"
    USER_MFA_DISABLED: Final[str] = "user.mfa_disabled"


__all__ = ["WebhookEventType"]

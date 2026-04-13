"""Re-export MFA sub-router."""

from controllers.auth.user.mfa import router

__all__ = ["router"]

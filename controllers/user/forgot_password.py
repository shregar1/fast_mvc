"""Re-export forgot password handler."""

from controllers.auth.user.forgot_password import ForgotPasswordController as forgot_password

__all__ = ["forgot_password"]

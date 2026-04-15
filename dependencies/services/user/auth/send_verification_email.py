"""Send-verification-email dependency for /user/auth/* routes.

Re-exports the account-scoped dependency; implementation lives under
``dependencies.services.user.account``.
"""

from dependencies.services.user.account.send_verification_email import (
    SendVerificationEmailServiceDependency,
)

__all__ = ["SendVerificationEmailServiceDependency"]

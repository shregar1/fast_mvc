"""User auth service dependencies."""

from . import forgot_password
from . import reset_password
from dependencies.services.user.login import UserLoginServiceDependency
from dependencies.services.user.logout import UserLogoutServiceDependency
from dependencies.services.user.register import UserRegistrationServiceDependency
from dependencies.services.user.refresh_token import UserRefreshTokenServiceDependency
from dependencies.services.user.subscription import UserSubscriptionServiceDependency

__all__ = [
    "forgot_password",
    "reset_password",
    "UserLoginServiceDependency",
    "UserLogoutServiceDependency",
    "UserRegistrationServiceDependency",
    "UserRefreshTokenServiceDependency",
    "UserSubscriptionServiceDependency",
]

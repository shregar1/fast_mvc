"""Re-export user controller abstraction."""

from controllers.auth.user.abstraction import IUserController
from controllers.apis.json_api_controller import JSONAPIController

__all__ = ["IUserController", "JSONAPIController"]

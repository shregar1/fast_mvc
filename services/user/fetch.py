"""FetchUser Service."""

from typing import Any

from services.user.abstraction import IUserService
from dtos.requests.apis.v1.user.fetch import FetchUserRequestDTO
from repositories.user.fetch import FetchUserRepository


class FetchUserService(IUserService):
    """Represents the FetchUserService class."""

    def __init__(self, repo: FetchUserRepository, *args: Any, **kwargs: Any):
        """Execute __init__ operation.

        Args:
            repo: The repo parameter.
            *args: Additional positional arguments forwarded to parent.
            **kwargs: Additional keyword arguments forwarded to parent.
        """
        super().__init__(*args, **kwargs)
        self.repo = repo

    def run(self, request_dto: FetchUserRequestDTO) -> dict:
        """Execute run operation.

        Args:
            request_dto: The request_dto parameter.

        Returns:
            The result of the operation.
        """
        self.logger.info("Executing fetch service")
        return {"item": {"id": "1"}, "message": "Success"}

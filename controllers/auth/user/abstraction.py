"""
User Controller Abstraction Module.

This module defines the base abstraction for all user-related controllers.
It extends :class:`~controllers.apis.json_api_controller.JSONAPIController`
so ``/user/*`` handlers share the same JSON error envelope and
:meth:`invoke_with_exception_handling` template as v1 APIs.

Example:
    >>> class MyUserController(IUserController):
    ...     async def post(self, request: Request):
    ...         async def _run():
    ...             return JSONResponse(...)
    ...         return await self.invoke_with_exception_handling(request, _run)
"""

from typing import Any

from start_utils import logger

from controllers.apis.json_api_controller import JSONAPIController


class IUserController(JSONAPIController):
    """
    Base abstraction for all user controllers.

    Inherits structured JSON responses and exception handling from
    :class:`JSONAPIController`. All controllers handling ``/user/*`` routes
    should inherit from this class.
    """

    def __init__(
        self,
        urn: str | None = None,
        user_urn: str | None = None,
        api_name: str | None = None,
        user_id: int | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        logger.debug("Initializing IUserController")
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            *args,
            **kwargs,
        )


__all__ = ["IUserController", "JSONAPIController"]

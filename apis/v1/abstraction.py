"""
API Version 1 Controller Abstraction Module.
"""

from apis.json_api_controller import JSONAPIController

class IV1APIController(JSONAPIController):
    """
    Base abstraction for all API v1 controllers.
    """

    def __init__(
        self,
        urn: str | None = None,
        user_urn: str | None = None,
        api_name: str | None = None,
        user_id: int | None = None,
        *args,
        **kwargs
    ) -> None:
        super().__init__(urn=urn, user_urn=user_urn, api_name=api_name, user_id=user_id, *args, **kwargs)



__all__ = ["IV1APIController", "JSONAPIController"]

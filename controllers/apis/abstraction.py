"""Abstraction for REST API controllers."""

from __future__ import annotations

from collections.abc import Callable
from http import HTTPStatus
from typing import Any, Optional

from fastapi import Request
from fastapi.responses import JSONResponse

from controllers.apis.json_api_controller import JSONAPIController


class IAPIController(JSONAPIController):
    """Interface for controllers under ``controllers/apis``.

    Inherits :meth:`handle_exception`, :meth:`build_json_response`, and the
    common property surface from the JSON API stack. Adds
    :meth:`invoke_with_exception_handling` for callback-style handlers and
    :meth:`_handle_controller_exception` as a thin backward-compatible wrapper.
    """

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            *args,
            **kwargs,
        )

    async def invoke_with_exception_handling(
        self,
        request: Request,
        handler: Callable,
        *,
        event_name: str | None = None,
        session: Any = None,
        force_http_ok: bool = False,
    ) -> JSONResponse:
        """Run *handler* and translate any exception into a JSON error envelope
        via :meth:`handle_exception`.
        """
        try:
            return await handler()
        except Exception as err:
            response_dto, http_status = self.handle_exception(
                err,
                request,
                event_name=event_name or self.__class__.__name__,
                session=session,
                force_http_ok=force_http_ok,
            )
            return JSONResponse(
                content=response_dto.model_dump(),
                status_code=http_status,
            )

    def _handle_controller_exception(
        self,
        err: Exception,
        request: Request | None = None,
        *,
        urn: str = "",
        http_status: int = HTTPStatus.INTERNAL_SERVER_ERROR,
    ) -> JSONResponse:
        """Backward-compatible shim. Prefer :meth:`handle_exception`."""
        if request is None:
            class _Stub:
                state = type("S", (), {"urn": urn})()
            request = _Stub()  # type: ignore[assignment]
        response_dto, status_code = self.handle_exception(
            err,
            request,  # type: ignore[arg-type]
            event_name=self.__class__.__name__,
            force_http_ok=False,
        )
        return JSONResponse(
            content=response_dto.model_dump(),
            status_code=status_code,
        )

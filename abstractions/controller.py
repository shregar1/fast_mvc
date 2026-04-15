"""Controller abstraction.

Defines :class:`IController`, the root base class every API controller in this
application extends. Inheritance: concrete controller → layered ``controllers.*``
interface → :class:`IController` → :class:`core.utils.context.ContextMixin`.

``ContextMixin`` supplies the ``urn``/``user_urn``/``api_name``/``user_id``/``logger``
properties. This class layers on top:

- ``dictionary_utility`` / ``jwt_utility`` accessors for per-request utilities.
- :meth:`bind_request_context` — lifts request.state fields, rebinds the logger,
  instantiates per-request utilities.
- :meth:`handle_exception` — uniform envelope for client/transient/unknown errors.
- :meth:`validate_request` — default no-op hook subclasses can extend.
"""

from __future__ import annotations

from abc import ABC
from http import HTTPStatus
from typing import Any, Optional

from fastapi import Request

from constants.api_status import APIStatus
from core.utils.context import ContextMixin
from dtos.responses.base import BaseResponseDTO
from fast_platform.errors import (
    BadInputError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
    UnauthorizedError,
    UnexpectedResponseError,
)
from structured_log import log_event
from utilities.audit import log_audit
from utilities.request_utils import get_client_ip

_CLIENT_ERRORS = (
    BadInputError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)
_TRANSIENT_ERRORS = (
    RateLimitError,
    ServiceUnavailableError,
    UnexpectedResponseError,
)


class IController(ContextMixin, ABC):
    """Root controller interface; all controllers extend this or a nested interface."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the controller with request context.

        Args:
            urn: Unique Request Number for tracing.
            user_urn: User's unique resource name.
            api_name: Name of the API endpoint.
            user_id: User's database identifier.
            *args: Forwarded to parent classes.
            **kwargs: Forwarded to parent classes.
        """
        # Call ``ContextMixin.__init__`` explicitly so the type checker does not
        # merge this with other ``ContextMixin`` implementations (e.g. in
        # ``fast_platform``) that may use a different ``user_id`` type.
        ContextMixin.__init__(
            self,
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            *args,
            **kwargs,
        )

    @property
    def dictionary_utility(self) -> Any:
        """DictionaryUtility: per-request dictionary utility for response formatting."""
        return getattr(self, "_dictionary_utility", None)

    @dictionary_utility.setter
    def dictionary_utility(self, value: Any) -> None:
        """Set the dictionary utility."""
        self._dictionary_utility = value

    @property
    def jwt_utility(self) -> Any:
        """JWTUtility: per-request JWT utility for token operations."""
        return getattr(self, "_jwt_utility", None)

    @jwt_utility.setter
    def jwt_utility(self, value: Any) -> None:
        """Set the JWT utility."""
        self._jwt_utility = value

    def bind_request_context(
        self,
        request: Request,
        *,
        dictionary_utility_factory: Any = None,
        jwt_utility_factory: Any = None,
    ) -> None:
        """Lift ``urn``/``user_id``/``user_urn`` off ``request.state``, rebind the
        structured logger, and (optionally) instantiate per-request utilities.

        Called at the top of every controller handler so each one stops repeating
        the same 10-line boilerplate. Factories — when passed — are invoked with
        the standard context tuple ``(urn, user_urn, api_name, user_id)``.

        Args:
            request: The incoming FastAPI request (must carry ``state.urn``).
            dictionary_utility_factory: Optional factory from
                ``DictionaryUtilityDependency.derive``. If provided, builds
                ``self.dictionary_utility``.
            jwt_utility_factory: Optional factory from ``JWTUtilityDependency.derive``.
                If provided, builds ``self.jwt_utility``.
        """
        self.urn = getattr(request.state, "urn", "") or ""
        self.user_id = getattr(request.state, "user_id", None)
        self.user_urn = getattr(request.state, "user_urn", "") or ""
        self.logger = self.logger.bind(
            urn=self.urn,
            user_urn=self.user_urn,
            api_name=self.api_name,
            user_id=self.user_id,
        )
        if dictionary_utility_factory is not None:
            self.dictionary_utility = dictionary_utility_factory(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
            )
        if jwt_utility_factory is not None:
            self.jwt_utility = jwt_utility_factory(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
            )

    def handle_exception(
        self,
        err: Exception,
        request: Request,
        event_name: str,
        *,
        session: Any = None,
        force_http_ok: bool = True,
        fallback_message: str = "Request failed.",
        fallback_key: str = "error_internal_server_error",
    ) -> tuple[BaseResponseDTO, int]:
        """Translate any controller exception into a structured response envelope.

        Handles the three classes of errors uniformly (client, transient, unknown),
        emits a structured ``log_event`` and a best-effort audit row, and returns a
        ``(BaseResponseDTO, http_status_code)`` tuple ready for ``JSONResponse``.

        Args:
            err: The exception raised inside the controller's ``try`` block.
            request: The incoming FastAPI request (used for URN + client IP).
            event_name: Logical event name — e.g. ``"login"``. Emits ``"<event>.failed"``.
            session: Optional DB session for audit logging. Audit is skipped if ``None``.
            force_http_ok: If True, always return HTTP 200 (required for auth endpoints
                whose contract tests expect 200 with a FAILED envelope). If False, use
                the error's own ``httpStatusCode``.
            fallback_message: Message for unknown exceptions.
            fallback_key: Response key for unknown exceptions.

        Returns:
            ``(response_dto, http_status_code)`` — drop straight into ``JSONResponse``.
        """
        txn_urn = (
            getattr(request.state, "urn", None)
            or getattr(self, "_urn", None)
            or ""
        )

        if isinstance(err, _CLIENT_ERRORS):
            level = "warning"
            response_message = err.responseMessage
            response_key = err.responseKey
            http_status = HTTPStatus.OK if force_http_ok else err.httpStatusCode
        elif isinstance(err, _TRANSIENT_ERRORS):
            level = "warning"
            response_message = err.responseMessage
            response_key = err.responseKey
            http_status = HTTPStatus.OK if force_http_ok else err.httpStatusCode
        else:
            level = "error"
            response_message = fallback_message
            response_key = fallback_key
            http_status = HTTPStatus.OK if force_http_ok else HTTPStatus.INTERNAL_SERVER_ERROR

        self.logger.error(
            f"{err.__class__.__name__} error during {event_name}: {err}"
        )
        log_event(
            f"{event_name}.failed",
            level=level,
            urn=txn_urn,
            reason=response_key,
            status_code=getattr(err, "httpStatusCode", None),
        )

        if session is not None:
            try:
                log_audit(
                    session,
                    f"{event_name}.failed",
                    "user",
                    metadata={"reason": response_key},
                    ip=get_client_ip(request),
                )
            except Exception:
                pass

        response_dto = BaseResponseDTO(
            transactionUrn=txn_urn,
            status=APIStatus.FAILED,
            responseMessage=response_message,
            responseKey=response_key,
            data={},
        )
        return response_dto, http_status

    async def validate_request(
        self,
        urn: str | None,
        user_urn: str | None,
        request_payload: dict,
        request_headers: dict,
        api_name: str | None,
        user_id: int | None,
    ) -> None:
        """Default request validation hook — subclasses override and extend.

        Assigns the provided context fields onto the controller. Concrete
        controllers typically call ``await super().validate_request(...)`` and
        then raise ``BadInputError`` on anything invalid in their payload.
        """
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name
        self.user_id = user_id
        return

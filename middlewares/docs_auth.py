"""HTTP Basic authentication for OpenAPI UI and schema (developer-only surfaces).

When ``DOCS_USERNAME`` and ``DOCS_PASSWORD`` are both set in the environment,
all Swagger/ReDoc/OpenAPI routes require valid ``Authorization: Basic …`` credentials,
including subpaths (e.g. ``/docs/oauth2-redirect``) and any configured OpenAPI URL.
If either variable is unset or empty, these routes stay open (typical local development).

Environment:

* ``OPENAPI_URL`` — Must match :class:`fastapi.FastAPI` ``openapi_url`` (default ``/openapi.json``).
* ``DOCS_EXTRA_PROTECTED_PATHS`` — Comma-separated extra paths to require the same auth (legacy aliases).
"""

from __future__ import annotations

import os
from collections.abc import Awaitable, Callable
from http import HTTPStatus

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response

from constants.default import Default
from constants.http_header import HttpHeader
from utilities.auth import constant_time_compare, parse_basic_authorization
from utilities.string import StringUtility


class DocsAuthConfig:
    """Configuration class for OpenAPI documentation authentication settings."""

    @staticmethod
    def normalized_openapi_url() -> str:
        """Return the OpenAPI JSON path; keep in sync with ``FastAPI(openapi_url=...)``."""
        raw = os.environ.get("OPENAPI_URL", "/openapi.json").strip() or "/openapi.json"
        return StringUtility.normalize_path(raw)

    @classmethod
    def resolve_openapi_url_paths(cls) -> frozenset[str]:
        """All URL paths that expose the OpenAPI schema (for auth + logging excludes)."""
        out: set[str] = {cls.normalized_openapi_url()}
        extra_paths = StringUtility.split_csv(
            os.environ.get("DOCS_EXTRA_PROTECTED_PATHS"), default=[]
        )
        for p in extra_paths:
            out.add(StringUtility.normalize_path(p))
        return frozenset(out)

    @classmethod
    def docs_logging_exclude_paths(cls) -> frozenset[str]:
        """Paths to skip in request logging (doc UI + schema URLs)."""
        base = frozenset(
            {
                "/",
                "/health",
                "/docs",
                "/redoc",
                *cls.resolve_openapi_url_paths(),
            }
        )
        return base

    @staticmethod
    def is_auth_configured() -> bool:
        """Return True when Basic auth should be enforced for documentation routes."""
        u = os.environ.get("DOCS_USERNAME", "").strip()
        p = os.environ.get("DOCS_PASSWORD", "").strip()
        return bool(u and p)

    @staticmethod
    def unauthorized_response() -> PlainTextResponse:
        """Return 401 Unauthorized response for documentation routes."""
        return PlainTextResponse(
            "Authentication required for API documentation.",
            status_code=HTTPStatus.UNAUTHORIZED,
            headers={
                HttpHeader.WWW_AUTHENTICATE: f'Basic realm="{Default.APP_NAME} API Documentation"'
            },
        )

    @classmethod
    def path_requires_auth(cls, path: str) -> bool:
        """Return True if ``path`` is a documentation or OpenAPI schema surface."""
        np = path.rstrip("/") or "/"
        for o in cls.resolve_openapi_url_paths():
            if np == (o.rstrip("/") or "/"):
                return True
        pl = path.lower()
        if pl == "/docs" or pl.startswith("/docs/"):
            return True
        if pl == "/redoc" or pl.startswith("/redoc/"):
            return True
        return False


class DocsBasicAuthMiddleware(BaseHTTPMiddleware):
    """Require HTTP Basic auth for OpenAPI-related routes when credentials are configured."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if not DocsAuthConfig.is_auth_configured():
            return await call_next(request)
        # CORS preflight must reach CORSMiddleware without a 401 challenge.
        if request.method == "OPTIONS":
            return await call_next(request)
        if not DocsAuthConfig.path_requires_auth(request.url.path):
            return await call_next(request)

        expected_user = os.environ["DOCS_USERNAME"].strip()
        expected_pass = os.environ["DOCS_PASSWORD"].strip()
        parsed = parse_basic_authorization(
            request.headers.get(HttpHeader.AUTHORIZATION)
        )
        if parsed is None:
            return DocsAuthConfig.unauthorized_response()
        username, password = parsed
        if not (
            constant_time_compare(username, expected_user)
            and constant_time_compare(password, expected_pass)
        ):
            return DocsAuthConfig.unauthorized_response()
        return await call_next(request)


__all__ = [
    "DocsAuthConfig",
    "DocsBasicAuthMiddleware",
]

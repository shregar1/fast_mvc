"""Well-known application URL paths (path only; used by auth allowlists and docs)."""

from typing import Any, Final


class RouteConstant:
    """Paths that commonly bypass JWT or appear in OpenAPI / probes."""

    ROOT: Final[str] = "/"
    HEALTH: Final[str] = "/health"
    HEALTH_LIVE: Final[str] = "/health/live"
    HEALTH_READY: Final[str] = "/health/ready"
    USER_LOGIN: Final[str] = "/user/login"
    USER_REGISTER: Final[str] = "/user/register"
    USER_REFRESH: Final[str] = "/user/refresh"
    DOCS: Final[str] = "/docs"
    REDOC: Final[str] = "/redoc"
    OPENAPI_JSON: Final[str] = "/openapi.json"


    UNPROTECTED_ROUTES: Final[set[str]] = {
        ROOT,
        HEALTH,
        HEALTH_LIVE,
        HEALTH_READY,
        USER_LOGIN,
        USER_REGISTER,
        USER_REFRESH,
        DOCS,
        REDOC,
        OPENAPI_JSON,
    }

    CALLBACK_ROUTES: Final[set] = set[Any]()

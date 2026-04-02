"""Machine-readable ``responseKey`` values for API JSON envelopes."""

from typing import Final


class ResponseKey:
    """Canonical keys for :class:`~dtos.responses.apis.abstraction.IResponseAPIDTO`."""

    ERROR_INTERNAL_SERVER_ERROR: Final[str] = "error_internal_server_error"

    SUCCESS_HEALTH: Final[str] = "success_health"
    ERROR_HEALTH_UNHEALTHY: Final[str] = "error_health_unhealthy"

    SUCCESS_HEALTH_LIVE: Final[str] = "success_health_live"

    SUCCESS_HEALTH_READY: Final[str] = "success_health_ready"
    ERROR_HEALTH_NOT_READY: Final[str] = "error_health_not_ready"

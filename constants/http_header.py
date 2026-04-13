"""Standard HTTP header names and helpers for API responses."""

from typing import ClassVar, Optional


class HttpHeader:
    """Canonical HTTP header names used by the API and CORS defaults."""

    CACHE_CONTROL: ClassVar[str] = "Cache-Control"
    CACHE_CONTROL_VALUE_NO_CACHE: ClassVar[str] = "no-cache"

    X_REQUEST_ID: ClassVar[str] = "X-Request-ID"
    X_PROCESS_TIME: ClassVar[str] = "X-Process-Time"
    X_REFERENCE_URN: ClassVar[str] = "x-reference-urn"
    X_TRANSACTION_URN: ClassVar[str] = "x-transaction-urn"

    AUTHORIZATION: ClassVar[str] = "Authorization"
    CONTENT_TYPE: ClassVar[str] = "Content-Type"
    CONTENT_TYPE_JSON: ClassVar[str] = "application/json"
    WWW_AUTHENTICATE: ClassVar[str] = "WWW-Authenticate"
    AUTHORIZATION_BEARER_PREFIX: ClassVar[str] = "Bearer "
    AUTHORIZATION_BASIC_PREFIX: ClassVar[str] = "Basic "
    AUTHORIZATION_BEARER_PREFIX_LENGTH: ClassVar[int] = 7
    AUTHORIZATION_BASIC_PREFIX_LENGTH: ClassVar[int] = 6
    ENCODING_UTF8: ClassVar[str] = "utf-8"
    ACCEPT: ClassVar[str] = "Accept"

    def get_reference_urn_header(
        self,
        *,
        reference_urn: Optional[str] = None,
    ) -> dict[str, str]:
        """Build response headers including ``x-reference-urn`` when a value is present."""
        if reference_urn is None or reference_urn == "":
            return {}
        return {self.X_REFERENCE_URN: reference_urn}


    def correlation_response_headers(
        self,
        *,
        reference_urn: Optional[str] = None,
        transaction_urn: Optional[str] = None,
    ) -> dict[str, str]:
        """Merge optional client reference echo and server transaction URN for API responses."""
        headers: dict[str, str] = {}
        if reference_urn:
            headers[self.X_REFERENCE_URN] = reference_urn
        if transaction_urn:
            headers[self.X_TRANSACTION_URN] = transaction_urn
        return headers

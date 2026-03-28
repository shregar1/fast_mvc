"""Standard HTTP header names and helpers for API responses."""

from typing import Final

# Custom correlation header (request → response echo)
X_REFERENCE_URN: Final[str] = "x-reference-urn"


def x_reference_urn_headers(reference_urn: str | None) -> dict[str, str]:
    """Build response headers including ``x-reference-urn`` when a value is present."""
    if reference_urn is None or reference_urn == "":
        return {}
    return {X_REFERENCE_URN: reference_urn}

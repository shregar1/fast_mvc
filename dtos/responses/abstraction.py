"""Standard API response envelope DTO."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from abstractions.dto import IDTO
from utilities.datetime import DateTimeUtility


class IResponseDTO(BaseModel, IDTO):
    """Standard response DTO for all API endpoints.

    Combines :class:`pydantic.BaseModel` and :class:`abstractions.dto.IDTO`.

    Controllers use DictionaryUtility (or similar) to emit camelCase keys in JSON.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=False)

    transactionUrn: str | None = ""
    """Unique identifier for request tracing and correlation."""

    status: str
    """Operation status: ``SUCCESS`` or ``FAILED``."""

    responseMessage: str
    """Human-readable message describing the result."""

    responseKey: str
    """Machine-readable key for programmatic handling and i18n."""

    data: list | dict | None = None
    """Main response payload (success data or empty dict on error)."""

    errors: list | dict | None = None
    """Error details when status is FAILED."""

    metadata: dict[str, Any] | None = Field(
        default=None,
        description=(
            "Optional envelope metadata (pagination, timings, version, "
            "feature flags). Distinct from `data`, which holds the main payload."
        ),
    )

    timestamp: datetime = Field(
        default_factory=DateTimeUtility.utc_now,
        description="Server time (UTC) when this response envelope was generated.",
    )

    reference_urn: str | None = Field(
        default=None,
        description=(
            "Echo of the client correlation id when provided "
            "via the x-reference-urn request header."
        ),
    )

    reference_number: str | None = Field(
        default=None,
        description=(
            "Echo of the client reference number when provided "
            "via the X-Reference-Number request header."
        ),
    )

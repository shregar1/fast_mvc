"""Base Response DTO – thin alias kept for backward compatibility."""

from typing import Any

from pydantic import ConfigDict

from dtos.responses.abstraction import IResponseDTO


class BaseResponseDTO(IResponseDTO):
    """Concrete response envelope used by controllers.

    Overrides ``extra="forbid"`` from the parent to ``extra="ignore"``
    so controllers can safely call ``model_dump()`` on instances that
    may carry additional fields without raising validation errors.

    ``model_dump()`` defaults to ``mode="json"`` so datetime fields
    are automatically serialized to ISO-8601 strings.
    """

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=False)

    def model_dump(self, *, mode: str = "json", **kwargs: Any) -> dict[str, Any]:
        return super().model_dump(mode=mode, **kwargs)


__all__ = ["BaseResponseDTO"]

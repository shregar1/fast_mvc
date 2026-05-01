"""DELETE — correlation payload using :class:`ExampleDeleteRequestDTO`."""

from __future__ import annotations

from typing import Any

from dtos.requests.example.delete import ExampleDeleteRequestDTO



class ExampleDeleteRequestFactory:
    """Body for delete requests (optional overrides)."""

    @classmethod
    def build(cls, **overrides: Any) -> dict[str, Any]:
        base: dict[str, Any] = {}
        return {**base, **overrides}

    @classmethod
    def build_dto(cls, **overrides: Any) -> ExampleDeleteRequestDTO:
        return ExampleDeleteRequestDTO(**cls.build(**overrides))

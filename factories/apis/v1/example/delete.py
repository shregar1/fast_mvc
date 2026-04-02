"""DELETE — correlation payload using :class:`ExampleDeleteRequestDTO`."""

from __future__ import annotations

from typing import Any

from dtos.requests.example.delete import ExampleDeleteRequestDTO

from factories.common import ReferenceUrnFactory


class ExampleDeleteRequestFactory:
    """Body for delete requests that only carry ``reference_urn`` (plus optional overrides)."""

    @classmethod
    def build(cls, **overrides: Any) -> dict[str, Any]:
        base: dict[str, Any] = {"reference_urn": ReferenceUrnFactory.new_reference_urn()}
        return {**base, **overrides}

    @classmethod
    def build_dto(cls, **overrides: Any) -> ExampleDeleteRequestDTO:
        return ExampleDeleteRequestDTO(**cls.build(**overrides))

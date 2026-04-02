"""Generic update body — :class:`ExampleUpdateRequestDTO` (use :mod:`patch` / :mod:`put` for presets)."""

from __future__ import annotations

from typing import Any

from dtos.requests.example.update import ExampleUpdateRequestDTO

from factories.common import ReferenceUrnFactory


class ExampleUpdateRequestFactory:
    """Build payloads for updating an example resource (PUT/PATCH) with explicit fields."""

    @classmethod
    def build(cls, **overrides: Any) -> dict[str, Any]:
        base: dict[str, Any] = {"reference_urn": ReferenceUrnFactory.new_reference_urn()}
        return {**base, **overrides}

    @classmethod
    def build_dto(cls, **overrides: Any) -> ExampleUpdateRequestDTO:
        return ExampleUpdateRequestDTO(**cls.build(**overrides))

"""POST / create — :class:`ExampleCreateRequestDTO`."""

from __future__ import annotations

from typing import Any

from dtos.requests.example.create import ExampleCreateRequestDTO

from factories.common import ReferenceUrnFactory


class ExampleCreateRequestFactory:
    """Build payloads for creating an example resource (POST)."""

    DEFAULT_NAME = "Created Example"
    DEFAULT_DESCRIPTION = "Factory-generated create description"

    @classmethod
    def build(cls, **overrides: Any) -> dict[str, Any]:
        base: dict[str, Any] = {
            "reference_urn": ReferenceUrnFactory.new_reference_urn(),
            "name": cls.DEFAULT_NAME,
            "description": cls.DEFAULT_DESCRIPTION,
        }
        return {**base, **overrides}

    @classmethod
    def build_dto(cls, **overrides: Any) -> ExampleCreateRequestDTO:
        return ExampleCreateRequestDTO(**cls.build(**overrides))

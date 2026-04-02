"""PATCH — partial update using :class:`ExampleUpdateRequestDTO`."""

from __future__ import annotations

from typing import Any

from dtos.requests.example.update import ExampleUpdateRequestDTO

from factories.common import ReferenceUrnFactory


class ExamplePatchRequestFactory:
    """Typical PATCH body: change one field, leave others unset / null."""

    DEFAULT_NAME = "patched-name-only"

    @classmethod
    def build(cls, **overrides: Any) -> dict[str, Any]:
        base: dict[str, Any] = {
            "reference_urn": ReferenceUrnFactory.new_reference_urn(),
            "name": cls.DEFAULT_NAME,
            "description": None,
        }
        return {**base, **overrides}

    @classmethod
    def build_dto(cls, **overrides: Any) -> ExampleUpdateRequestDTO:
        return ExampleUpdateRequestDTO(**cls.build(**overrides))

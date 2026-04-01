"""Factory for v1 example fetch request payloads (tests and local tooling).

Still builds :class:`~dtos.requests.apis.v1.user.fetch.FetchUserRequestDTO` (DTOs remain under
``dtos/requests/apis/v1/user``). This package path is ``factories/apis/v1/example`` to mirror
the preferred factories layout (``example`` segment instead of ``user``).
"""

from __future__ import annotations

from typing import Any

from dtos.requests.apis.v1.user.fetch import FetchUserRequestDTO

from factories.apis.v1.example.common import new_reference_urn


class ExampleFetchRequestFactory:
    """Build valid :class:`FetchUserRequestDTO` payloads and model instances.

    ``reference_urn`` must be a valid UUID string (see :class:`dtos.requests.abstraction.IRequestDTO`).
    A fresh UUID is generated on each :meth:`build` unless you pass ``reference_urn``.

    Example:
        >>> payload = ExampleFetchRequestFactory.build(name="Alice")
        >>> dto = ExampleFetchRequestFactory.build_dto(name="Alice")
    """

    DEFAULT_NAME = "Test User"
    DEFAULT_DESCRIPTION = "Factory-generated description"

    @classmethod
    def build(cls, **overrides: Any) -> dict[str, Any]:
        """Return a dict suitable for ``FetchUserRequestDTO(**payload)``."""
        base: dict[str, Any] = {
            "reference_urn": new_reference_urn(),
            "name": cls.DEFAULT_NAME,
            "description": cls.DEFAULT_DESCRIPTION,
        }
        merged = {**base, **overrides}
        return merged

    @classmethod
    def build_dto(cls, **overrides: Any) -> FetchUserRequestDTO:
        """Return a validated :class:`FetchUserRequestDTO` instance."""
        return FetchUserRequestDTO(**cls.build(**overrides))

"""Shared helpers for example API request factories."""

from __future__ import annotations

import uuid


class ReferenceUrnFactory:
    """Factory class for generating reference URNs."""

    @staticmethod
    def new_reference_urn() -> str:
        """Return a new UUID string suitable for :class:`dtos.requests.abstraction.IRequestDTO`."""
        return str(uuid.uuid4())


# Backward compatibility: module-level functions delegate to the class
new_reference_urn = ReferenceUrnFactory.new_reference_urn


__all__ = [
    "ReferenceUrnFactory",
    "new_reference_urn",
]

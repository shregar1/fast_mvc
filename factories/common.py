"""Shared helpers for example API request factories."""

from __future__ import annotations

import uuid


class ReferenceUrnFactory:
    """Factory class for generating reference URNs."""

    @staticmethod
    def new_reference_urn() -> str:
        """Return a new UUID string suitable for :class:`dtos.requests.abstraction.IRequestDTO`."""
        return str(uuid.uuid4())


__all__ = ["ReferenceUrnFactory"]

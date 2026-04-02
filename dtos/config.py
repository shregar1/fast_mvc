"""DTO Configuration utilities."""

from __future__ import annotations

from typing import Any

from pydantic import ConfigDict


class DtoConfigBuilder:
    """Builder for DTO configuration with default settings."""

    _ENHANCED_DEFAULTS: dict[str, Any] = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True,
    }

    @classmethod
    def build_config(cls, **overrides: Any) -> ConfigDict:
        """Build a :class:`~pydantic.ConfigDict` by merging *overrides* into the
        defaults used by :class:`~dtos.base.ApplicationBaseModel`.

        Common overrides: ``title``, ``str_strip_whitespace``, ``populate_by_name``,
        ``frozen``, ``validate_default``, ``json_schema_extra``, etc.
        """
        merged = {**cls._ENHANCED_DEFAULTS, **overrides}
        return ConfigDict(**merged)


__all__ = ["DtoConfigBuilder"]

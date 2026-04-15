"""Dictionary utility – camelCase conversion and helpers."""

from __future__ import annotations

import re
from typing import Any, Optional

from start_utils import logger


class DictionaryUtility:
    """Utility for dictionary key transformations (snake_case ↔ camelCase)."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> None:
        self._urn = urn
        self._user_urn = user_urn
        self._api_name = api_name
        self._user_id = user_id
        self._logger = logger.bind(urn=urn, user_urn=user_urn, api_name=api_name)

    @staticmethod
    def _to_camel(snake: str) -> str:
        parts = snake.split("_")
        return parts[0] + "".join(p.capitalize() for p in parts[1:])

    def convert_dict_keys_to_camel_case(self, data: Any) -> Any:
        """Recursively convert all dict keys from snake_case to camelCase."""
        if isinstance(data, dict):
            return {
                self._to_camel(k): self.convert_dict_keys_to_camel_case(v)
                for k, v in data.items()
            }
        if isinstance(data, list):
            return [self.convert_dict_keys_to_camel_case(item) for item in data]
        return data

    @staticmethod
    def _to_snake(camel: str) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", camel).lower()

    def convert_dict_keys_to_snake_case(self, data: Any) -> Any:
        """Recursively convert all dict keys from camelCase to snake_case."""
        if isinstance(data, dict):
            return {
                self._to_snake(k): self.convert_dict_keys_to_snake_case(v)
                for k, v in data.items()
            }
        if isinstance(data, list):
            return [self.convert_dict_keys_to_snake_case(item) for item in data]
        return data


__all__ = ["DictionaryUtility"]

"""Helper utilities for Item API tests."""

from __future__ import annotations

import asyncio
from uuid import uuid4

from fastapi.testclient import TestClient

from models.item import Item


class ItemTestHelper:
    """Helper class for Item API test operations."""

    @staticmethod
    def item_from_api_json(data: dict) -> Item:
        """Convert API JSON response to Item entity."""
        return Item.from_dict(
            {
                "id": data["id"],
                "name": data["name"],
                "description": data["description"],
                "completed": data["completed"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
            }
        )

    @staticmethod
    def post_item(
        client: TestClient,
        *,
        name: str,
        description: str = "",
        completed: bool = False,
    ) -> Item:
        """Post a new item and return the created Item entity."""
        r = client.post(
            "/items",
            json={
                "reference_urn": str(uuid4()),
                "name": name,
                "description": description,
                "completed": completed,
            },
        )
        assert r.status_code == 201, r.text
        return ItemTestHelper.item_from_api_json(r.json())

    @staticmethod
    def clear_app_item_storage() -> None:
        """Clear the in-memory item storage between tests."""
        try:
            from controllers.apis.v1.item.item_controller import _controller

            repo = _controller._service._repository
            asyncio.run(repo.clear())
        except (ImportError, ModuleNotFoundError, AttributeError):
            pass


# Backward compatibility: module-level functions delegate to the class
_item_from_api_json = ItemTestHelper.item_from_api_json
_post_item = ItemTestHelper.post_item
_clear_app_item_storage = ItemTestHelper.clear_app_item_storage


__all__ = [
    "ItemTestHelper",
    "_item_from_api_json",
    "_post_item",
    "_clear_app_item_storage",
]

"""Test item builders (replaces legacy ``testing.item.factories``)."""

from __future__ import annotations

from uuid import uuid4

from models.item import Item


class ItemFactory:
    """Build :class:`models.item.Item` instances for unit tests."""

    @staticmethod
    def create(
        *,
        name: str | None = None,
        description: str = "",
        completed: bool = False,
        id: str | None = None,
    ) -> Item:
        return Item(
            id=id,
            name=name or f"Item {uuid4().hex[:8]}",
            description=description,
            completed=completed,
        )

    @classmethod
    def create_batch(cls, count: int, **kwargs: object) -> list[Item]:
        return [cls.create(**kwargs) for _ in range(count)]

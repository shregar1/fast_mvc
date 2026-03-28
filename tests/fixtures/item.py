"""Pytest fixtures for Item API tests (replaces ``testing.item.fixtures``)."""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator, Generator
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from fastapi.testclient import TestClient

from app import app as fastapi_app
from models.item import Item


def _item_from_api_json(data: dict) -> Item:
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


def _clear_app_item_storage() -> None:
    from controllers.apis.v1.item.item_controller import _controller

    repo = _controller._service._repository
    asyncio.run(repo.clear())


@pytest.fixture(autouse=True)
def _reset_item_storage_between_tests(request: pytest.FixtureRequest) -> Generator[None]:
    """Keep in-memory item store isolated per test."""
    if request.node.get_closest_marker("no_item_reset"):
        yield
        return
    _clear_app_item_storage()
    yield
    _clear_app_item_storage()


@pytest.fixture(scope="session")
def app():
    """FastAPI application used by TestClient."""
    return fastapi_app


@pytest.fixture
def item_client(app):
    return TestClient(app)


@pytest.fixture
async def async_item_client(app) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def authenticated_client(item_client):
    return item_client


@pytest.fixture
def item_db():
    """Placeholder (sample stack uses in-memory repository)."""
    return None


@pytest.fixture
def item_repository():
    from repositories.item import ItemRepository

    return ItemRepository()


@pytest.fixture
def mock_user() -> dict:
    return {"id": "1", "email": "test@example.com"}


@pytest.fixture
def mock_admin_user() -> dict:
    return {"id": "2", "email": "admin@example.com"}


@pytest.fixture
def mock_auth():
    """Auth middleware is often a no-op in dev; use an open context."""
    return contextlib.nullcontext()


@pytest.fixture
def mock_invalid_auth():
    return contextlib.nullcontext()


@pytest.fixture
def mock_expired_token():
    return contextlib.nullcontext()


@pytest.fixture
def create_item_payload() -> dict:
    return {
        "reference_number": str(uuid4()),
        "name": "Test Item",
        "description": "Test Description",
        "completed": False,
    }


@pytest.fixture
def update_item_payload() -> dict:
    return {
        "reference_number": str(uuid4()),
        "name": "Updated Name",
        "description": "Updated description",
    }


@pytest.fixture
def invalid_item_payloads() -> list[dict]:
    return [{"name": ""}, {"name": "x" * 101}]


@pytest.fixture
def test_item(item_client: TestClient, create_item_payload: dict) -> Item:
    r = item_client.post("/items", json=create_item_payload)
    assert r.status_code == 201, r.text
    return _item_from_api_json(r.json())


@pytest.fixture
def test_items(item_client: TestClient, mock_auth) -> list[Item]:
    names = ["Alpha Search Me", "Beta Other", "Gamma Third"]
    out: list[Item] = []
    with mock_auth:
        for name in names:
            payload = {
                "reference_number": str(uuid4()),
                "name": name,
                "description": "d",
                "completed": False,
            }
            r = item_client.post("/items", json=payload)
            assert r.status_code == 201, r.text
            out.append(_item_from_api_json(r.json()))
    return out


@pytest.fixture
def completed_items(item_client: TestClient, mock_auth) -> list[Item]:
    with mock_auth:
        payload = {
            "reference_number": str(uuid4()),
            "name": "Done Item",
            "description": "",
            "completed": True,
        }
        r = item_client.post("/items", json=payload)
        assert r.status_code == 201, r.text
        return [_item_from_api_json(r.json())]


@pytest.fixture
def pending_items(item_client: TestClient, mock_auth) -> list[Item]:
    with mock_auth:
        payload = {
            "reference_number": str(uuid4()),
            "name": "Todo Item",
            "description": "",
            "completed": False,
        }
        r = item_client.post("/items", json=payload)
        assert r.status_code == 201, r.text
        return [_item_from_api_json(r.json())]


@pytest.fixture
def freezer():
    yield None


@pytest.fixture
def reset_factories():
    yield

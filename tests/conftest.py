"""Pytest Configuration and Shared Fixtures.

This file is automatically loaded by pytest and provides:
- Path setup for imports
- Shared fixtures for all tests
- Custom markers and configuration

Usage:
    Fixtures are automatically available in all test files.

    def test_something(item_client, test_item):
        # item_client and test_item are automatically injected
        pass

    def test_factories(fetch_example_request_payload):
        # Top-level factories package (see factories/README.md)
        assert "reference_urn" in fetch_example_request_payload
"""

import os
import sys
from pathlib import Path

# =============================================================================
# PATH SETUP
# =============================================================================

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Monorepo: local ``fastx_platform`` (and optional packages) for imports like ``fastx_platform.errors``
_REPO_ROOT = PROJECT_ROOT.parent
for _extra in (
    _REPO_ROOT / "fastx_platform" / "src",
    _REPO_ROOT / "fastx_dashboards" / "src",
):
    if _extra.is_dir():
        sys.path.insert(0, str(_extra))

import asyncio
import contextlib
from collections.abc import AsyncIterator, Generator
from uuid import uuid4

from httpx import ASGITransport, AsyncClient
from fastapi.testclient import TestClient

from app import app as fastapi_app

# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================


def pytest_configure(config):
    """Configure pytest with custom markers.

    These markers can be used to categorize and filter tests.
    """
    config.addinivalue_line("markers", "unit: Unit tests (fast, isolated)")
    config.addinivalue_line(
        "markers", "integration: Integration tests (may use database)"
    )
    config.addinivalue_line("markers", "e2e: End-to-end tests (full flow)")
    config.addinivalue_line("markers", "slow: Slow tests (skip in fast mode)")
    config.addinivalue_line("markers", "auth: Authentication-related tests")
    config.addinivalue_line("markers", "api: API endpoint tests")
    config.addinivalue_line("markers", "db: DataI-related tests")


# =============================================================================
# CUSTOM FIXTURES SPECIFIC TO TESTS
# =============================================================================

import pytest


# =============================================================================
# ITEM API FIXTURES
# =============================================================================

@pytest.fixture(autouse=True)
def _reset_item_storage_between_tests(request: pytest.FixtureRequest) -> Generator[None]:
    """Keep in-memory item store isolated per test."""
    if request.node.get_closest_marker("no_item_reset"):
        yield
        return
    ItemTestHelper.clear_app_item_storage()
    yield
    ItemTestHelper.clear_app_item_storage()


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
        "reference_urn": str(uuid4()),
        "name": "Test Item",
        "description": "Test Description",
        "completed": False,
    }


@pytest.fixture
def update_item_payload() -> dict:
    return {
        "reference_urn": str(uuid4()),
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
    return ItemTestHelper.item_from_api_json(r.json())


@pytest.fixture
def test_items(item_client: TestClient, mock_auth) -> list[Item]:
    names = ["Alpha Search Me", "Beta Other", "Gamma Third"]
    with mock_auth:
        return [
            ItemTestHelper.post_item(item_client, name=n, description="d", completed=False)
            for n in names
        ]


@pytest.fixture
def completed_items(item_client: TestClient, mock_auth) -> list[Item]:
    with mock_auth:
        return [ItemTestHelper.post_item(item_client, name="Done Item", completed=True)]


@pytest.fixture
def pending_items(item_client: TestClient, mock_auth) -> list[Item]:
    with mock_auth:
        return [ItemTestHelper.post_item(item_client, name="Todo Item", completed=False)]


@pytest.fixture
def freezer():
    yield None


@pytest.fixture
def reset_factories():
    yield


# =============================================================================
# SHARED SETTINGS & ENV
# =============================================================================


@pytest.fixture(scope="session")
def test_settings():
    """Provide test-specific settings.

    Returns:
        Dictionary with test configuration.

    """
    return {
        "dataI_url": "sqlite:///./test.db",
        "jwt_secret": "test-secret-key-minimum-32-characters-long",
        "jwt_algorithm": "HS256",
        "jwt_expiration_hours": 24,
        "debug": True,
        "log_level": "DEBUG",
    }


@pytest.fixture(autouse=True)
def setup_test_env(test_settings, monkeypatch):
    """Set up environment for each test.

    Automatically configures environment variables for testing.
    """
    # Set test environment variables
    for key, value in test_settings.items():
        env_key = key.upper()
        monkeypatch.setenv(env_key, str(value))

    yield

    # Cleanup is handled by monkeypatch


@pytest.fixture
def captured_logs(caplog):
    """Provide captured log output for testing.

    Example:
        def test_logs(captured_logs):
            # Run code that logs
            assert "Expected message" in captured_logs.text

    """
    import logging

    caplog.set_level(logging.DEBUG)
    return caplog


# =============================================================================
# TOP-LEVEL FACTORIES (see factories/README.md)
# =============================================================================

from factories import ExampleFetchRequestFactory


@pytest.fixture
def fetch_example_request_payload() -> dict:
    """Valid ``FetchUserRequestDTO`` body fields as a dict (includes ``reference_urn``)."""
    return ExampleFetchRequestFactory.build()

"""Pytest Configuration and Shared Fixtures.

This file is automatically loaded by pytest and provides:
- Path setup for imports
- Shared fixtures for all tests
- Custom markers and configuration

Usage:
    Fixtures are automatically available in all test files.

    def test_something(client):
        # client is automatically injected
        pass

    def test_factories(fetch_example_request_payload):
        # Top-level factories package (see factories/README.md)
        assert "name" in fetch_example_request_payload
"""

import os
import sys
from pathlib import Path

# =============================================================================
# PATH SETUP
# =============================================================================

# Add project root to Python path (``__file__`` can be relative when pytest loads conftest).
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Monorepo: local ``fastx_platform`` (and optional packages) for imports like ``fastx_platform.errors``
_REPO_ROOT = PROJECT_ROOT.parent
for _extra in (
    _REPO_ROOT / "fastx_platform" / "src",
    _REPO_ROOT / "fastx_middleware" / "src",
    _REPO_ROOT / "fastx_database" / "src",
    _REPO_ROOT / "fastx_dashboards" / "src",
    _REPO_ROOT / "fastx_channels" / "src",
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
# CUSTOM FIXTURES
# =============================================================================

import pytest


@pytest.fixture(scope="session")
def app():
    """FastAPI application used by TestClient."""
    return fastapi_app


@pytest.fixture
def client(app):
    """Synchronous test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
async def async_client(app) -> AsyncIterator[AsyncClient]:
    """Async test client for the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
def authenticated_client(client):
    return client


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
    """Valid ``FetchUserRequestDTO`` body fields as a dict."""
    return ExampleFetchRequestFactory.build()

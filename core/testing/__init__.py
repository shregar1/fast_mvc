"""Test Fixtures and Utilities.

Provides common fixtures and test utilities for FastMVC applications.
"""

from core.testing.app_factory import TestAppFactory, create_test_app
from core.testing.async_utils import AsyncTestUtil, run_async
from core.testing.fixtures import (
    DataITestCase,
    AsyncDataITestCase,
    FixtureRegistry,
    TestClient,
    fixtures,
)
from core.testing.mocks import mock_external

__all__ = [
    # App Factory
    "TestAppFactory",
    "create_test_app",
    # Async Utils
    "AsyncTestUtil",
    "run_async",
    # Fixtures
    "DataITestCase",
    "AsyncDataITestCase",
    "FixtureRegistry",
    "TestClient",
    "fixtures",
    # Mocks
    "mock_external",
]

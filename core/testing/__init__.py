"""Test Fixtures and Utilities.

Provides common fixtures and test utilities for FastMVC applications.
"""

from core.testing.app_factory import TestAppFactory
from core.testing.async_utils import AsyncTestUtil
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
    # Async Utils
    "AsyncTestUtil",
    # Fixtures
    "DataITestCase",
    "AsyncDataITestCase",
    "FixtureRegistry",
    "TestClient",
    "fixtures",
    # Mocks
    "mock_external",
]

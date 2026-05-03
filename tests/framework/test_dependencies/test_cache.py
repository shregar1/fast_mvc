"""Tests for cache dependencies."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from dependencies.cache import CacheDependency


class TestCacheDependency:
    """Tests for CacheDependency class."""

    def test_derive_returns_redis_session(self):
        """derive() proxies to application redis_session."""
        fake_redis = MagicMock(name="redis_session")
        with patch("dependencies.cache.redis_session", fake_redis):
            assert CacheDependency.derive() is fake_redis

    def test_derive_callable(self):
        """derive is a usable FastAPI dependency."""
        assert callable(CacheDependency.derive)

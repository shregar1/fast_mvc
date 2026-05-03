"""Tests for auth dependencies."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi import Request

from dependencies.auth import AuthDependency


class TestAuthDependency:
    """Tests for AuthDependency class."""

    def test_class_exists(self):
        """AuthDependency is importable."""
        assert AuthDependency is not None

    def test_get_current_user_raises_when_anonymous(self):
        """Unauthenticated request raises UnauthorizedError."""
        from fastx_platform.errors import UnauthorizedError

        req = MagicMock(spec=Request)
        req.state = MagicMock(user=None)
        with pytest.raises(UnauthorizedError):
            AuthDependency.get_current_user(req)

    def test_get_current_user_returns_state_user(self):
        """Authenticated request returns user from state."""
        req = MagicMock(spec=Request)
        req.state = MagicMock(user={"id": "u1"})
        assert AuthDependency.get_current_user(req) == {"id": "u1"}

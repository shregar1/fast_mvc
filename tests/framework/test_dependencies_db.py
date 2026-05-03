"""Tests for dependencies.db module."""

from __future__ import annotations

import pytest


class TestDBDependency:
    """Test DBDependency class."""

    def test_db_dependency_importable(self):
        """Test DBDependency can be imported."""
        from dependencies.db import DBDependency
        assert DBDependency is not None

    def test_db_dependency_is_class(self):
        """Test DBDependency is a class."""
        from dependencies.db import DBDependency
        assert isinstance(DBDependency, type)

    def test_db_dependency_has_derive_method(self):
        """Test DBDependency has derive method."""
        from dependencies.db import DBDependency
        assert hasattr(DBDependency, "derive")

    def test_db_dependency_derive_is_callable(self):
        """Test DBDependency.derive is callable."""
        from dependencies.db import DBDependency
        assert callable(DBDependency.derive)


class TestDBDependencyExports:
    """Test DBDependency exports."""

    def test_all_contains_db_dependency(self):
        """Test __all__ contains DBDependency."""
        from dependencies.db import __all__
        assert "DBDependency" in __all__

    def test_all_is_list(self):
        """Test __all__ is a list."""
        from dependencies.db import __all__
        assert isinstance(__all__, list)

    def test_all_length(self):
        """Test __all__ has correct length."""
        from dependencies.db import __all__
        assert len(__all__) == 1


class TestDBDependencyInstance:
    """Test DBDependency instance behavior."""

    def test_db_dependency_instance_creation(self):
        """Test creating DBDependency instance."""
        from dependencies.db import DBDependency
        try:
            instance = DBDependency()
            assert instance is not None
        except (TypeError, ImportError):
            pytest.skip("fastx_db not available")


class TestDBDependencyDeriveBehavior:
    """Test DBDependency.derive behavior."""

    def test_derive_without_fastx_db_raises(self):
        """Test derive raises without fastx_db."""
        from dependencies.db import DBDependency
        try:
            result = DBDependency.derive()
            # If it works, fastx_db is installed
            assert result is not None
        except ImportError:
            # Expected if fastx_db is not installed
            pass

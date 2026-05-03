"""Example developer test file.

This is an example test file for developers to use as a template.
Delete or replace these tests with your own application tests.
"""

from __future__ import annotations


class TestExampleFeature:
    """Example test class for your feature."""

    def test_example_passes(self):
        """An example test that passes."""
        assert True

    def test_example_math(self):
        """An example test with math."""
        assert 1 + 1 == 2

    def test_example_string(self):
        """An example test with strings."""
        result = "hello" + " world"
        assert result == "hello world"

    def test_example_list(self):
        """An example test with lists."""
        items = [1, 2, 3]
        assert len(items) == 3

    def test_example_dict(self):
        """An example test with dicts."""
        data = {"key": "value"}
        assert data["key"] == "value"


class TestYourService:
    """Template for testing your service — replace stubs when you add services."""

    def test_service_import(self):
        """Placeholder: add ``from services.your_service import YourService`` when ready."""
        assert True

    def test_service_instantiation(self):
        """Placeholder: instantiate your service here when implemented."""
        assert True

    def test_service_method(self):
        """Placeholder: call your service methods here when implemented."""
        assert True


class TestYourRepository:
    """Template for testing your repository."""

    def test_repository_import(self):
        """Placeholder: import your repository when implemented."""
        assert True

    def test_repository_crud(self):
        """Placeholder: exercise CRUD when implemented."""
        assert True


class TestYourController:
    """Template for testing your controller."""

    def test_controller_import(self):
        """Placeholder: import your controller when implemented."""
        assert True

    def test_controller_endpoint(self):
        """Placeholder: hit HTTP routes when implemented."""
        assert True

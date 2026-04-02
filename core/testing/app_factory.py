"""Test application factory utilities."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI


class TestAppFactory:
    """Factory for creating FastAPI apps configured for testing."""

    @staticmethod
    def create_app(**kwargs: Any) -> FastAPI:
        """Create a FastAPI app configured for testing.

        Usage:
            app = TestAppFactory.create_app()
            client = TestClient(app)
        """
        app = FastAPI(
            title="Test App",
            docs_url=None,  # Disable docs in tests
            redoc_url=None,
            **kwargs,
        )

        return app


__all__ = ["TestAppFactory"]

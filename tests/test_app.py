"""
Tests for FastMVC application.
"""

from fastapi.testclient import TestClient
from pydantic import BaseModel

from app import app
from errors.unexpected_response_error import UnexpectedResponseError


class TestAppConfiguration:
    """Tests for app configuration."""

    def test_app_exists(self):
        """Test app instance exists."""
        assert app is not None

    def test_app_has_title(self):
        """Test app has proper title."""
        assert app.title == "FastMVC API"

    def test_app_has_docs_url(self):
        """Test app has docs URL configured."""
        assert app.docs_url == "/docs"

    def test_app_has_redoc_url(self):
        """Test app has redoc URL configured."""
        assert app.redoc_url == "/redoc"


class TestMiddlewareStack:
    """Tests for middleware configuration."""

    def test_middleware_is_configured(self):
        """Test middleware stack is configured."""
        # App should have middleware
        assert len(app.user_middleware) > 0


class TestRouterConfiguration:
    """Tests for router configuration."""

    def test_user_router_included(self):
        """Test user router is included."""
        routes = [route.path for route in app.routes]

        # User routes should be included
        assert "/user/login" in routes or any("/user" in r for r in routes)


class TestEnvironmentVariables:
    """Tests for environment variable loading."""

    def test_rate_limit_variables_loaded(self):
        """Test rate limit environment variables are loaded."""
        from app import (
            RATE_LIMIT_BURST_LIMIT,
            RATE_LIMIT_REQUESTS_PER_HOUR,
            RATE_LIMIT_REQUESTS_PER_MINUTE,
        )
        assert isinstance(RATE_LIMIT_REQUESTS_PER_MINUTE, int)
        assert isinstance(RATE_LIMIT_REQUESTS_PER_HOUR, int)
        assert isinstance(RATE_LIMIT_BURST_LIMIT, int)


class TestAppRuntime:
    """Runtime tests using TestClient to cover handlers."""

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

    def test_health_endpoint_returns_ok(self):
        """Health endpoint should return 200 and status ok."""
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_unexpected_response_error_handler(self):
        """UnexpectedResponseError should be handled with its status and key."""

        @app.get("/__test_unexpected_error")
        def _unexpected_error_route():
            raise UnexpectedResponseError(
                responseMessage="Something went wrong.",
                responseKey="error_unexpected",
                httpStatusCode=422,
            )

        # Mark this test route as unprotected so auth middleware doesn't short‑circuit
        from start_utils import unprotected_routes

        unprotected_routes.add("/__test_unexpected_error")

        response = self.client.get("/__test_unexpected_error")
        assert response.status_code == 422
        body = response.json()
        assert body["responseKey"] == "error_unexpected"
        assert body["status"] == "FAILED"

    def test_validation_exception_handler_for_bad_input(self):
        """RequestValidationError should be transformed into error_bad_input."""

        class _TestItem(BaseModel):
            name: str

        @app.post("/__test_validation")
        def _validation_route(item: _TestItem):
            return {"name": item.name}

        # Mark validation test route as unprotected to bypass auth
        from start_utils import unprotected_routes

        unprotected_routes.add("/__test_validation")

        response = self.client.post("/__test_validation", json={})
        assert response.status_code == 400
        body = response.json()
        assert body["responseKey"] == "error_bad_input"

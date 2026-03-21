"""
Tests for middleware classes.

Uses fastmvc-middleware package for request context, security headers, rate limit,
CORS, logging, timing, and trusted host. AuthenticationMiddleware remains app-specific.
"""

from unittest.mock import MagicMock, patch

import pytest

from fastmiddleware import (
    CORSMiddleware,
    LoggingMiddleware,
    RateLimitConfig,
    RateLimitMiddleware,
    RequestContextMiddleware,
    SecurityHeadersConfig,
    SecurityHeadersMiddleware,
    TimingMiddleware,
    TrustedHostMiddleware,
)


# =============================================================================
# fastmiddleware Package Tests (app uses these directly)
# =============================================================================

class TestfastmiddlewareSecurityHeaders:
    """Tests for fastmiddleware SecurityHeadersMiddleware."""

    def test_config_initialization(self):
        """Test SecurityHeadersConfig from fastmiddleware."""
        config = SecurityHeadersConfig(
            enable_hsts=True,
            hsts_max_age=31536000,
            x_frame_options="DENY",
        )
        assert config.enable_hsts is True
        assert config.hsts_max_age == 31536000
        assert config.x_frame_options == "DENY"

    def test_middleware_creation(self):
        """Test SecurityHeadersMiddleware can be created."""
        app = MagicMock()
        config = SecurityHeadersConfig()
        middleware = SecurityHeadersMiddleware(app, config=config)
        assert middleware is not None


class TestfastmiddlewareRateLimit:
    """Tests for fastmiddleware RateLimitMiddleware."""

    def test_config_initialization(self):
        """Test RateLimitConfig from fastmiddleware."""
        config = RateLimitConfig(
            requests_per_minute=60,
            requests_per_hour=1000,
            burst_limit=10,
            strategy="sliding",
        )
        assert config.requests_per_minute == 60
        assert config.requests_per_hour == 1000
        assert config.burst_limit == 10
        assert config.strategy == "sliding"

    @pytest.mark.asyncio
    async def test_middleware_creation(self):
        """Test RateLimitMiddleware can be created."""
        app = MagicMock()
        config = RateLimitConfig()
        middleware = RateLimitMiddleware(app, config=config)
        assert middleware is not None


class TestfastmiddlewareRequestContext:
    """Tests for fastmiddleware RequestContextMiddleware."""

    def test_middleware_creation(self):
        """Test RequestContextMiddleware can be created."""
        app = MagicMock()
        middleware = RequestContextMiddleware(app)
        assert middleware is not None


class TestfastmiddlewareTiming:
    """Tests for fastmiddleware TimingMiddleware."""

    def test_middleware_creation(self):
        """Test TimingMiddleware can be created."""
        app = MagicMock()
        middleware = TimingMiddleware(app)
        assert middleware is not None

    def test_custom_header_name(self):
        """Test custom header name."""
        app = MagicMock()
        middleware = TimingMiddleware(app, header_name="X-Custom-Time")
        assert middleware is not None


class TestfastmiddlewareLogging:
    """Tests for fastmiddleware LoggingMiddleware."""

    def test_middleware_creation(self):
        """Test LoggingMiddleware can be created."""
        app = MagicMock()
        middleware = LoggingMiddleware(app)
        assert middleware is not None

    def test_exclude_paths(self):
        """Test exclude paths option."""
        app = MagicMock()
        middleware = LoggingMiddleware(
            app,
            exclude_paths={"/health", "/docs"}
        )
        assert middleware is not None


class TestfastmiddlewareCORS:
    """Tests for fastmiddleware CORSMiddleware."""

    def test_middleware_creation(self):
        """Test CORSMiddleware can be created."""
        app = MagicMock()
        middleware = CORSMiddleware(
            app,
            allow_origins=["*"],
            allow_methods=["GET", "POST"],
        )
        assert middleware is not None


class TestfastmiddlewareTrustedHost:
    """Tests for fastmiddleware TrustedHostMiddleware."""

    def test_middleware_creation(self):
        """Test TrustedHostMiddleware can be created."""
        app = MagicMock()
        middleware = TrustedHostMiddleware(app, allowed_hosts=["*"])
        assert middleware is not None


class TestAuthenticationMiddleware:
    """Tests for custom AuthenticationMiddleware (app-specific)."""

    @pytest.fixture
    def mock_app(self):
        """Create mock app."""
        return MagicMock()

    @pytest.mark.asyncio
    @patch('middlewares.authentication.unprotected_routes', {'/health', '/docs'})
    @patch('middlewares.authentication.callback_routes', set())
    @patch('middlewares.authentication.logger')
    async def test_unprotected_route_passes_through(self, mock_logger, mock_app):
        """Test unprotected routes pass through without auth."""
        from middlewares import AuthenticationMiddleware

        middleware = AuthenticationMiddleware(mock_app)

        request = MagicMock()
        request.state = MagicMock()
        request.state.urn = "test-urn"
        request.url.path = "/health"
        request.method = "GET"

        expected_response = MagicMock()

        async def call_next(req):
            return expected_response

        result = await middleware.dispatch(request, call_next)

        assert result == expected_response

    @pytest.mark.asyncio
    @patch('middlewares.authentication.unprotected_routes', set())
    @patch('middlewares.authentication.callback_routes', set())
    @patch('middlewares.authentication.logger')
    async def test_options_request_passes_through(self, mock_logger, mock_app):
        """Test OPTIONS requests pass through."""
        from middlewares import AuthenticationMiddleware

        middleware = AuthenticationMiddleware(mock_app)

        request = MagicMock()
        request.state = MagicMock()
        request.state.urn = "test-urn"
        request.url.path = "/api/protected"
        request.method = "OPTIONS"

        expected_response = MagicMock()

        async def call_next(req):
            return expected_response

        result = await middleware.dispatch(request, call_next)

        assert result == expected_response

    @pytest.mark.asyncio
    @patch('middlewares.authentication.unprotected_routes', set())
    @patch('middlewares.authentication.callback_routes', set())
    @patch('middlewares.authentication.logger')
    async def test_missing_authorization_header_returns_401(
        self,
        mock_logger,
        mock_app,
    ):
        """Test 401 is returned when Authorization header is missing."""
        from middlewares import AuthenticationMiddleware

        middleware = AuthenticationMiddleware(mock_app)

        request = MagicMock()
        request.state = MagicMock()
        request.state.urn = "test-urn"
        request.url.path = "/api/protected"
        request.method = "GET"
        request.headers = {}

        async def call_next(req):
            return MagicMock()

        response = await middleware.dispatch(request, call_next)

        assert response.status_code == 401
        body = response.body.decode()
        assert "error_authetication_error" in body

    @pytest.mark.asyncio
    @patch('middlewares.authentication.unprotected_routes', set())
    @patch('middlewares.authentication.callback_routes', set())
    @patch('middlewares.authentication.JWTUtility')
    @patch('middlewares.authentication.logger')
    async def test_invalid_token_payload_returns_401(
        self,
        mock_logger,
        mock_jwt_utility,
        mock_app,
    ):
        """Test invalid token payload returns 401."""
        from middlewares import AuthenticationMiddleware

        # Configure JWTUtility to raise ValueError when decoding
        instance = mock_jwt_utility.return_value
        instance.decode_token.side_effect = ValueError("bad token")

        middleware = AuthenticationMiddleware(mock_app)

        request = MagicMock()
        request.state = MagicMock()
        request.state.urn = "test-urn"
        request.url.path = "/api/protected"
        request.method = "GET"
        request.headers = {"authorization": "Bearer badtoken"}

        async def call_next(req):
            return MagicMock()

        response = await middleware.dispatch(request, call_next)

        assert response.status_code == 401
        body = response.body.decode()
        assert "error_authetication_error" in body

    @pytest.mark.asyncio
    @patch('middlewares.authentication.unprotected_routes', set())
    @patch('middlewares.authentication.callback_routes', set())
    @patch('middlewares.authentication.UserRepository')
    @patch('middlewares.authentication.JWTUtility')
    @patch('middlewares.authentication.logger')
    async def test_user_not_found_returns_session_expired(
        self,
        mock_logger,
        mock_jwt_utility,
        mock_user_repository,
        mock_app,
    ):
        """Test when user is not found, session expired response is returned."""
        from middlewares import AuthenticationMiddleware

        # JWT decodes successfully
        jwt_instance = mock_jwt_utility.return_value
        jwt_instance.decode_token.return_value = {"user_id": 1, "user_urn": "urn"}

        # UserRepository returns no user
        repo_instance = mock_user_repository.return_value
        repo_instance.retrieve_record_by_id_and_is_logged_in.return_value = None

        middleware = AuthenticationMiddleware(mock_app)

        request = MagicMock()
        request.state = MagicMock()
        request.state.urn = "test-urn"
        request.url.path = "/api/protected"
        request.method = "GET"
        request.headers = {"authorization": "Bearer sometoken"}

        async def call_next(req):
            return MagicMock()

        response = await middleware.dispatch(request, call_next)

        assert response.status_code == 401
        body = response.body.decode()
        assert "error_session_expiry" in body

    @pytest.mark.asyncio
    @patch('middlewares.authentication.unprotected_routes', set())
    @patch('middlewares.authentication.callback_routes', set())
    @patch('middlewares.authentication.UserRepository')
    @patch('middlewares.authentication.JWTUtility')
    @patch('middlewares.authentication.logger')
    async def test_successful_authentication_calls_next(
        self,
        mock_logger,
        mock_jwt_utility,
        mock_user_repository,
        mock_app,
    ):
        """Test successful authentication proceeds to next handler."""
        from middlewares import AuthenticationMiddleware

        jwt_instance = mock_jwt_utility.return_value
        jwt_instance.decode_token.return_value = {"user_id": 1, "user_urn": "urn"}

        user = MagicMock()
        repo_instance = mock_user_repository.return_value
        repo_instance.retrieve_record_by_id_and_is_logged_in.return_value = user

        middleware = AuthenticationMiddleware(mock_app)

        request = MagicMock()
        request.state = MagicMock()
        request.state.urn = "test-urn"
        request.url.path = "/api/protected"
        request.method = "GET"
        request.headers = {"authorization": "Bearer validtoken"}

        expected_response = MagicMock()

        async def call_next(req):
            return expected_response

        response = await middleware.dispatch(request, call_next)

        assert response == expected_response
        assert request.state.user_id == 1
        assert request.state.user_urn == "urn"

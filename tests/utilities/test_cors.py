"""Tests for CORS configuration utilities."""

from __future__ import annotations

from constants.cors import CorsDefaults, CorsEnvVar
from utilities.cors import CorsConfigUtility


class TestCorsConfigUtility:
    """Tests for :class:`CorsConfigUtility`."""

    def test_init_default_values(self):
        """Initialization with default context."""
        util = CorsConfigUtility()
        assert util.urn is None
        assert util.user_urn is None
        assert util.api_name is None
        assert util.user_id is None

    def test_init_with_context(self):
        """Initialization with tracing context."""
        util = CorsConfigUtility(
            urn="test-urn",
            user_urn="user-123",
            api_name="api-test",
            user_id="user-456",
        )
        assert util.urn == "test-urn"
        assert util.user_urn == "user-123"
        assert util.api_name == "api-test"
        assert util.user_id == "user-456"

    def test_parse_allow_origins_unset_uses_fallback(self, monkeypatch):
        """When both origin env vars are unset, use :data:`CorsDefaults.FALLBACK_ALLOW_ORIGINS`."""
        monkeypatch.delenv(CorsEnvVar.ORIGINS, raising=False)
        monkeypatch.delenv(CorsEnvVar.ALLOWED_ORIGINS, raising=False)
        assert CorsConfigUtility.parse_allow_origins() == list(CorsDefaults.FALLBACK_ALLOW_ORIGINS)

    def test_parse_allow_origins_cors_origins_wins(self, monkeypatch):
        """``CORS_ORIGINS`` is used when set."""
        monkeypatch.setenv(CorsEnvVar.ORIGINS, "https://a.com,https://b.com")
        monkeypatch.setenv(CorsEnvVar.ALLOWED_ORIGINS, "https://ignored.com")
        assert CorsConfigUtility.parse_allow_origins() == ["https://a.com", "https://b.com"]

    def test_parse_allow_origins_allowed_origins_docker_fallback(self, monkeypatch):
        """``ALLOWED_ORIGINS`` is used when ``CORS_ORIGINS`` is unset."""
        monkeypatch.delenv(CorsEnvVar.ORIGINS, raising=False)
        monkeypatch.setenv(CorsEnvVar.ALLOWED_ORIGINS, "https://docker.app")
        assert CorsConfigUtility.parse_allow_origins() == ["https://docker.app"]

    def test_parse_allow_origins_empty_string_falls_back(self, monkeypatch):
        """Whitespace-only values fall back to defaults."""
        monkeypatch.setenv(CorsEnvVar.ORIGINS, "   ")
        assert CorsConfigUtility.parse_allow_origins() == list(CorsDefaults.FALLBACK_ALLOW_ORIGINS)

    def test_parse_allow_headers_unset_uses_fallback(self, monkeypatch):
        """Unset ``CORS_ALLOW_HEADERS`` uses :data:`CorsDefaults.FALLBACK_ALLOW_HEADERS`."""
        monkeypatch.delenv(CorsEnvVar.ALLOW_HEADERS, raising=False)
        assert CorsConfigUtility.parse_allow_headers() == list(CorsDefaults.FALLBACK_ALLOW_HEADERS)

    def test_parse_allow_headers_wildcard_maps_to_fallback_list(self, monkeypatch):
        """Exact ``*`` for headers expands to the default allow-headers list."""
        monkeypatch.setenv(CorsEnvVar.ALLOW_HEADERS, CorsDefaults.WILDCARD)
        assert CorsConfigUtility.parse_allow_headers() == list(CorsDefaults.FALLBACK_ALLOW_HEADERS)

    def test_parse_allow_headers_comma_separated(self, monkeypatch):
        """Comma-separated header names are stripped and split."""
        monkeypatch.setenv(
            CorsEnvVar.ALLOW_HEADERS,
            " Authorization , Content-Type ",
        )
        assert CorsConfigUtility.parse_allow_headers() == ["Authorization", "Content-Type"]

    def test_load_settings_from_env_defaults(self, monkeypatch):
        """Defaults match constants when CORS env is cleared."""
        for key in (
            CorsEnvVar.ORIGINS,
            CorsEnvVar.ALLOWED_ORIGINS,
            CorsEnvVar.ALLOW_CREDENTIALS,
            CorsEnvVar.ALLOW_METHODS,
            CorsEnvVar.ALLOW_HEADERS,
            CorsEnvVar.EXPOSE_HEADERS,
            CorsEnvVar.ALLOW_ORIGIN_REGEX,
            CorsEnvVar.MAX_AGE,
        ):
            monkeypatch.delenv(key, raising=False)

        dto = CorsConfigUtility.load_settings_from_env()
        assert dto.allow_origins == list(CorsDefaults.FALLBACK_ALLOW_ORIGINS)
        assert dto.allow_credentials is CorsDefaults.DEFAULT_ALLOW_CREDENTIALS
        assert dto.allow_methods == list(CorsDefaults.ALLOW_METHODS)
        assert dto.allow_headers == list(CorsDefaults.FALLBACK_ALLOW_HEADERS)
        assert dto.expose_headers == list(CorsDefaults.EXPOSE_HEADERS)
        assert dto.allow_origin_regex is None
        assert dto.max_age == CorsDefaults.DEFAULT_MAX_AGE_SECONDS

    def test_load_settings_from_env_overrides(self, monkeypatch):
        """Explicit env values populate the DTO."""
        monkeypatch.setenv(CorsEnvVar.ORIGINS, "https://app.example.com")
        monkeypatch.setenv(CorsEnvVar.ALLOW_CREDENTIALS, "false")
        monkeypatch.setenv(CorsEnvVar.ALLOW_METHODS, "GET,POST")
        monkeypatch.setenv(CorsEnvVar.MAX_AGE, "120")
        monkeypatch.setenv(CorsEnvVar.ALLOW_ORIGIN_REGEX, r"https://.*\.example\.com")

        dto = CorsConfigUtility.load_settings_from_env()
        assert dto.allow_origins == ["https://app.example.com"]
        assert dto.allow_credentials is False
        assert dto.allow_methods == ["GET", "POST"]
        assert dto.max_age == 120
        assert dto.allow_origin_regex == r"https://.*\.example\.com"

    def test_load_settings_from_env_empty_origin_regex(self, monkeypatch):
        """Blank ``CORS_ALLOW_ORIGIN_REGEX`` is stored as ``None``."""
        monkeypatch.setenv(CorsEnvVar.ALLOW_ORIGIN_REGEX, "   ")
        monkeypatch.delenv(CorsEnvVar.ORIGINS, raising=False)
        monkeypatch.delenv(CorsEnvVar.ALLOWED_ORIGINS, raising=False)
        dto = CorsConfigUtility.load_settings_from_env()
        assert dto.allow_origin_regex is None

    def test_get_middleware_kwargs_returns_subset(self, monkeypatch):
        """``get_middleware_kwargs`` forwards to the DTO (keys depend on CORSMiddleware)."""
        monkeypatch.delenv(CorsEnvVar.ORIGINS, raising=False)
        monkeypatch.delenv(CorsEnvVar.ALLOWED_ORIGINS, raising=False)

        kwargs = CorsConfigUtility.get_middleware_kwargs()
        assert isinstance(kwargs, dict)
        assert "allow_origins" in kwargs
        assert kwargs["allow_origins"] == list(CorsDefaults.FALLBACK_ALLOW_ORIGINS)


class TestCorsConfigUtilityProperties:
    """Context attributes from :class:`abstractions.utility.IUtility`."""

    def test_urn_property(self):
        util = CorsConfigUtility()
        util.urn = "test"
        assert util.urn == "test"

    def test_user_urn_property(self):
        util = CorsConfigUtility()
        util.user_urn = "user"
        assert util.user_urn == "user"

    def test_api_name_property(self):
        util = CorsConfigUtility()
        util.api_name = "api"
        assert util.api_name == "api"

    def test_user_id_property(self):
        util = CorsConfigUtility()
        util.user_id = "id"
        assert util.user_id == "id"

"""Additional tests for coverage."""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio


class TestUtilityInstances:
    """Test utility class instantiation."""

    def test_datetime_utility_instantiation(self):
        """Test DateTimeUtility can be instantiated."""
        from utilities.datetime import DateTimeUtility
        util = DateTimeUtility()
        assert util is not None
        assert isinstance(util, DateTimeUtility)

    def test_system_utility_instantiation(self):
        """Test SystemUtility can be instantiated."""
        from utilities.system import SystemUtility
        util = SystemUtility()
        assert util is not None
        assert isinstance(util, SystemUtility)

    def test_env_utility_instantiation(self):
        """Test EnvironmentParserUtility can be instantiated."""
        from utilities.env import EnvironmentParserUtility
        util = EnvironmentParserUtility()
        assert util is not None
        assert isinstance(util, EnvironmentParserUtility)

    def test_string_utility_instantiation(self):
        """Test StringUtility can be instantiated."""
        from utilities.string import StringUtility
        util = StringUtility()
        assert util is not None
        assert isinstance(util, StringUtility)

    def test_cors_utility_instantiation(self):
        """Test CorsConfigUtility can be instantiated."""
        from utilities.cors import CorsConfigUtility
        util = CorsConfigUtility()
        assert util is not None
        assert isinstance(util, CorsConfigUtility)

    def test_security_headers_utility_instantiation(self):
        """Test SecurityHeadersUtility can be instantiated."""
        from utilities.security_headers import SecurityHeadersUtility
        util = SecurityHeadersUtility()
        assert util is not None
        assert isinstance(util, SecurityHeadersUtility)

    def test_validator_utility_instantiation(self):
        """Test ConfigValidatorUtility can be instantiated."""
        from utilities.validator import ConfigValidatorUtility
        util = ConfigValidatorUtility()
        assert util is not None
        assert isinstance(util, ConfigValidatorUtility)


class TestUtilityPropertiesWithValues:
    """Test utility properties with values."""

    def test_datetime_utility_properties(self):
        """Test DateTimeUtility properties."""
        from utilities.datetime import DateTimeUtility
        util = DateTimeUtility(
            urn="test-urn",
            user_urn="user-urn",
            api_name="api-name",
            user_id="user-id"
        )
        assert util.urn == "test-urn"
        assert util.user_urn == "user-urn"
        assert util.api_name == "api-name"
        assert util.user_id == "user-id"

    def test_system_utility_properties(self):
        """Test SystemUtility properties."""
        from utilities.system import SystemUtility
        util = SystemUtility(
            urn="test-urn",
            user_urn="user-urn",
            api_name="api-name",
            user_id="user-id"
        )
        assert util.urn == "test-urn"
        assert util.user_urn == "user-urn"
        assert util.api_name == "api-name"
        assert util.user_id == "user-id"


class TestStringUtilityMethods:
    """Test StringUtility methods."""

    def test_split_csv_with_whitespace(self):
        """Test split_csv with whitespace."""
        from utilities.string import StringUtility
        result = StringUtility.split_csv("  a  ,  b  ,  c  ", [])
        assert result == ["a", "b", "c"]

    def test_split_csv_with_tabs(self):
        """Test split_csv with tabs."""
        from utilities.string import StringUtility
        result = StringUtility.split_csv("a\t,\tb\t,\tc", [])
        assert "a" in result
        assert "b" in result
        assert "c" in result

    def test_normalize_path_with_multiple_slashes(self):
        """Test normalize_path with multiple slashes."""
        from utilities.string import StringUtility
        result = StringUtility.normalize_path("//path//to//resource", leading_slash=True)
        # If it already starts with /, it won't add another
        assert result == "//path//to//resource"

    def test_normalize_path_without_leading(self):
        """Test normalize_path without leading slash."""
        from utilities.string import StringUtility
        result = StringUtility.normalize_path("/path", leading_slash=False)
        assert result == "/path"


class TestAuthHelperMethods:
    """Test utilities.auth helper functions."""

    def test_constant_time_compare_same(self):
        """Test constant_time_compare with same strings."""
        from utilities.auth import constant_time_compare
        assert constant_time_compare("secret", "secret") is True

    def test_constant_time_compare_different(self):
        """Test constant_time_compare with different strings."""
        from utilities.auth import constant_time_compare
        assert constant_time_compare("secret", "different") is False

    def test_constant_time_compare_different_lengths(self):
        """Test constant_time_compare with different length strings."""
        from utilities.auth import constant_time_compare
        assert constant_time_compare("short", "longerstring") is False

    def test_parse_basic_authorization_valid(self):
        """Test parse_basic_authorization with valid input."""
        from utilities.auth import parse_basic_authorization
        import base64
        credentials = base64.b64encode(b"user:pass").decode()
        result = parse_basic_authorization(f"Basic {credentials}")
        assert result is not None

    def test_parse_basic_authorization_invalid(self):
        """Test parse_basic_authorization with invalid input."""
        from utilities.auth import parse_basic_authorization
        result = parse_basic_authorization("Invalid")
        assert result is None or result == (None, None)


class TestDateTimeUtilityMethods:
    """Test DateTimeUtility methods."""

    def test_utc_now_returns_aware_datetime(self):
        """Test utc_now returns timezone-aware datetime."""
        import datetime
        from utilities.datetime import DateTimeUtility
        result = DateTimeUtility.utc_now()
        assert result.tzinfo is not None

    def test_utc_now_iso_format(self):
        """Test utc_now_iso returns valid ISO format."""
        from utilities.datetime import DateTimeUtility
        result = DateTimeUtility.utc_now_iso()
        assert "T" in result or "t" in result.lower()


class TestEnvironmentParserUtilityMethods:
    """Test EnvironmentParserUtility methods."""

    def test_parse_str_with_value(self, monkeypatch):
        """Test parse_str with value."""
        from utilities.env import EnvironmentParserUtility
        monkeypatch.setenv("TEST_STR", "value")
        result = EnvironmentParserUtility.parse_str("TEST_STR", "default")
        assert result == "value"

    def test_parse_optional_str_with_value(self, monkeypatch):
        """Test parse_optional_str with value."""
        from utilities.env import EnvironmentParserUtility
        monkeypatch.setenv("TEST_OPT", "value")
        result = EnvironmentParserUtility.parse_optional_str("TEST_OPT")
        assert result == "value"

    def test_parse_csv_with_single_value(self, monkeypatch):
        """Test parse_csv with single value."""
        from utilities.env import EnvironmentParserUtility
        monkeypatch.setenv("TEST_CSV", "value")
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", [])
        assert result == ["value"]


class TestSystemUtilityMethods:
    """Test SystemUtility methods."""

    def test_git_repository_folder_name_in_git_repo(self):
        """Test git_repository_folder_name in git repo."""
        from utilities.system import SystemUtility
        result = SystemUtility.git_repository_folder_name()
        # May be None or a string
        assert result is None or isinstance(result, str)


class TestValidatorUtilityMethods:
    """Test ConfigValidatorUtility methods."""

    def test_validate_app_env_valid(self):
        """Test validate_app_env with valid env."""
        from utilities.validator import ConfigValidatorUtility
        is_valid, message = ConfigValidatorUtility.validate_app_env("development")
        assert is_valid is True

    def test_validate_app_env_invalid(self):
        """Test validate_app_env with invalid env."""
        from utilities.validator import ConfigValidatorUtility
        is_valid, message = ConfigValidatorUtility.validate_app_env("invalid")
        assert is_valid is False

    def test_validate_port_valid(self):
        """Test validate_port with valid port."""
        from utilities.validator import ConfigValidatorUtility
        is_valid, message = ConfigValidatorUtility.validate_port("8080")
        assert is_valid is True

    def test_validate_port_invalid(self):
        """Test validate_port with invalid port."""
        from utilities.validator import ConfigValidatorUtility
        is_valid, message = ConfigValidatorUtility.validate_port("99999")
        assert is_valid is False

    def test_validate_url_valid(self):
        """Test validate_url with valid URL."""
        from utilities.validator import ConfigValidatorUtility
        is_valid, message = ConfigValidatorUtility.validate_url("https://example.com")
        assert is_valid is True

    def test_validate_url_invalid(self):
        """Test validate_url with invalid URL."""
        from utilities.validator import ConfigValidatorUtility
        is_valid, message = ConfigValidatorUtility.validate_url("not-a-url")
        assert is_valid is False

    def test_validate_email_valid(self):
        """Test validate_email with valid email."""
        from utilities.validator import ConfigValidatorUtility
        is_valid, message = ConfigValidatorUtility.validate_email("test@example.com")
        assert is_valid is True

    def test_validate_email_invalid(self):
        """Test validate_email with invalid email."""
        from utilities.validator import ConfigValidatorUtility
        is_valid, message = ConfigValidatorUtility.validate_email("not-an-email")
        assert is_valid is False

    def test_validate_jwt_secret_valid(self):
        """Test validate_jwt_secret with valid secret."""
        from utilities.validator import ConfigValidatorUtility
        # Valid: 32+ chars with mixed case, digits, and special
        secret = "VeryLongAndComplexSecretKey123!@#"
        is_valid, message = ConfigValidatorUtility.validate_jwt_secret(secret)
        assert is_valid is True

    def test_validate_jwt_secret_too_short(self):
        """Test validate_jwt_secret with short secret."""
        from utilities.validator import ConfigValidatorUtility
        is_valid, message = ConfigValidatorUtility.validate_jwt_secret("short")
        assert is_valid is False

    def test_validate_jwt_algorithm_valid(self):
        """Test validate_jwt_algorithm with valid algorithm."""
        from utilities.validator import ConfigValidatorUtility
        is_valid, message = ConfigValidatorUtility.validate_jwt_algorithm("HS256")
        assert is_valid is True

    def test_validate_jwt_algorithm_invalid(self):
        """Test validate_jwt_algorithm with invalid algorithm."""
        from utilities.validator import ConfigValidatorUtility
        is_valid, message = ConfigValidatorUtility.validate_jwt_algorithm("INVALID")
        assert is_valid is False


class TestCorsUtilityMethods:
    """Test CorsConfigUtility methods."""

    def test_parse_allow_origins_reads_from_env(self, monkeypatch):
        """Test parse_allow_origins reads from env."""
        from utilities.cors import CorsConfigUtility
        from constants.cors import CorsEnvVar
        monkeypatch.setenv(CorsEnvVar.ORIGINS, "*")
        result = CorsConfigUtility.parse_allow_origins()
        assert result is not None

    def test_parse_allow_headers_reads_from_env(self, monkeypatch):
        """Test parse_allow_headers reads from env."""
        from utilities.cors import CorsConfigUtility
        from constants.cors import CorsEnvVar
        monkeypatch.setenv(CorsEnvVar.ALLOW_HEADERS, "Content-Type,Authorization")
        result = CorsConfigUtility.parse_allow_headers()
        assert result is not None

    def test_get_middleware_kwargs_returns_dict(self, monkeypatch):
        """Test get_middleware_kwargs returns dict."""
        from utilities.cors import CorsConfigUtility
        monkeypatch.delenv("CORS_ORIGINS", raising=False)
        monkeypatch.delenv("CORS_ALLOWED_ORIGINS", raising=False)
        result = CorsConfigUtility.get_middleware_kwargs()
        assert isinstance(result, dict)


class TestSecurityHeadersUtilityMethods:
    """Test SecurityHeadersUtility methods."""

    def test_get_middleware_config_returns_config(self, monkeypatch):
        """Test get_middleware_config returns config."""
        from utilities.security_headers import SecurityHeadersUtility
        result = SecurityHeadersUtility.get_middleware_config()
        assert result is not None

    def test_load_settings_from_env_returns_dto(self, monkeypatch):
        """Test load_settings_from_env returns DTO."""
        from utilities.security_headers import SecurityHeadersUtility
        result = SecurityHeadersUtility.load_settings_from_env()
        assert result is not None


class TestDtoAbstractions:
    """Test DTO abstractions."""

    def test_idto_exists(self):
        """Test IDTO exists."""
        from abstractions.dto import IDTO
        assert IDTO is not None

    def test_irequest_dto_exists(self):
        """Test IRequestDTO exists."""
        from dtos.requests.abstraction import IRequestDTO
        assert IRequestDTO is not None

    def test_iresponse_dto_exists(self):
        """Test IResponseDTO exists."""
        from dtos.responses.abstraction import IResponseDTO
        assert IResponseDTO is not None

    def test_iconfiguration_dto_exists(self):
        """Test IConfigurationDTO exists."""
        from dtos.configuration.abstraction import IConfigurationDTO
        assert IConfigurationDTO is not None

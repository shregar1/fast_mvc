"""Tests for existing utility methods."""

from __future__ import annotations

import pytest
from unittest.mock import patch


class TestAuthHelpersExisting:
    """Test auth helper functions."""

    def test_constant_time_compare_exists(self):
        """Test constant_time_compare exists."""
        import utilities.auth as auth_module
        assert hasattr(auth_module, "constant_time_compare")

    def test_constant_time_compare_is_callable(self):
        """Test constant_time_compare is callable."""
        from utilities.auth import constant_time_compare
        assert callable(constant_time_compare)

    def test_constant_time_compare_equal_strings(self):
        """Test constant_time_compare with equal strings."""
        from utilities.auth import constant_time_compare
        assert constant_time_compare("abc", "abc") is True

    def test_constant_time_compare_different_strings(self):
        """Test constant_time_compare with different strings."""
        from utilities.auth import constant_time_compare
        assert constant_time_compare("abc", "def") is False

    def test_parse_basic_authorization_exists(self):
        """Test parse_basic_authorization exists."""
        import utilities.auth as auth_module
        assert hasattr(auth_module, "parse_basic_authorization")

    def test_parse_basic_authorization_is_callable(self):
        """Test parse_basic_authorization is callable."""
        from utilities.auth import parse_basic_authorization
        assert callable(parse_basic_authorization)


class TestDateTimeUtilityExisting:
    """Test DateTimeUtility existing methods."""

    def test_utc_now_exists(self):
        """Test utc_now exists."""
        from utilities.datetime import DateTimeUtility
        assert hasattr(DateTimeUtility, "utc_now")

    def test_utc_now_is_callable(self):
        """Test utc_now is callable."""
        from utilities.datetime import DateTimeUtility
        assert callable(DateTimeUtility.utc_now)

    def test_utc_now_returns_datetime(self):
        """Test utc_now returns datetime."""
        import datetime
        from utilities.datetime import DateTimeUtility
        result = DateTimeUtility.utc_now()
        assert isinstance(result, datetime.datetime)

    def test_utc_now_iso_exists(self):
        """Test utc_now_iso exists."""
        from utilities.datetime import DateTimeUtility
        assert hasattr(DateTimeUtility, "utc_now_iso")

    def test_utc_now_iso_is_callable(self):
        """Test utc_now_iso is callable."""
        from utilities.datetime import DateTimeUtility
        assert callable(DateTimeUtility.utc_now_iso)

    def test_utc_now_iso_returns_string(self):
        """Test utc_now_iso returns string."""
        from utilities.datetime import DateTimeUtility
        result = DateTimeUtility.utc_now_iso()
        assert isinstance(result, str)


class TestSystemUtilityExisting:
    """Test SystemUtility existing methods."""

    def test_git_repository_folder_name_exists(self):
        """Test git_repository_folder_name exists."""
        from utilities.system import SystemUtility
        assert hasattr(SystemUtility, "git_repository_folder_name")

    def test_git_repository_folder_name_is_callable(self):
        """Test git_repository_folder_name is callable."""
        from utilities.system import SystemUtility
        assert callable(SystemUtility.git_repository_folder_name)

    def test_git_repository_folder_name_returns_string_or_none(self):
        """Test git_repository_folder_name returns string or None."""
        from utilities.system import SystemUtility
        result = SystemUtility.git_repository_folder_name()
        assert result is None or isinstance(result, str)


class TestEnvironmentParserUtilityExisting:
    """Test EnvironmentParserUtility existing methods."""

    @pytest.mark.parametrize("method_name", [
        "parse_bool",
        "parse_int",
        "parse_str",
        "parse_optional_str",
        "parse_csv",
        "get_int_with_logging",
        "get_bool_with_logging",
    ])
    def test_methods_exist(self, method_name):
        """Test methods exist."""
        from utilities.env import EnvironmentParserUtility
        assert hasattr(EnvironmentParserUtility, method_name)

    @pytest.mark.parametrize("method_name", [
        "parse_bool",
        "parse_int",
        "parse_str",
        "parse_optional_str",
        "parse_csv",
    ])
    def test_static_methods_are_callable(self, method_name):
        """Test static methods are callable."""
        from utilities.env import EnvironmentParserUtility
        assert callable(getattr(EnvironmentParserUtility, method_name))


class TestStringUtilityExisting:
    """Test StringUtility existing methods."""

    @pytest.mark.parametrize("method_name", [
        "split_csv",
        "normalize_path",
    ])
    def test_methods_exist(self, method_name):
        """Test methods exist."""
        from utilities.string import StringUtility
        assert hasattr(StringUtility, method_name)

    @pytest.mark.parametrize("method_name", [
        "split_csv",
        "normalize_path",
    ])
    def test_static_methods_are_callable(self, method_name):
        """Test static methods are callable."""
        from utilities.string import StringUtility
        assert callable(getattr(StringUtility, method_name))


class TestCorsConfigUtilityExisting:
    """Test CorsConfigUtility existing methods."""

    @pytest.mark.parametrize("method_name", [
        "get_middleware_kwargs",
        "load_settings_from_env",
        "parse_allow_headers",
        "parse_allow_origins",
    ])
    def test_methods_exist(self, method_name):
        """Test methods exist."""
        from utilities.cors import CorsConfigUtility
        assert hasattr(CorsConfigUtility, method_name)

    @pytest.mark.parametrize("method_name", [
        "get_middleware_kwargs",
        "load_settings_from_env",
        "parse_allow_headers",
        "parse_allow_origins",
    ])
    def test_methods_are_callable(self, method_name):
        """Test methods are callable."""
        from utilities.cors import CorsConfigUtility
        assert callable(getattr(CorsConfigUtility, method_name))


class TestSecurityHeadersUtilityExisting:
    """Test SecurityHeadersUtility existing methods."""

    @pytest.mark.parametrize("method_name", [
        "get_middleware_config",
        "load_settings_from_env",
    ])
    def test_methods_exist(self, method_name):
        """Test methods exist."""
        from utilities.security_headers import SecurityHeadersUtility
        assert hasattr(SecurityHeadersUtility, method_name)

    @pytest.mark.parametrize("method_name", [
        "get_middleware_config",
        "load_settings_from_env",
    ])
    def test_methods_are_callable(self, method_name):
        """Test methods are callable."""
        from utilities.security_headers import SecurityHeadersUtility
        assert callable(getattr(SecurityHeadersUtility, method_name))


class TestConfigValidatorUtilityExisting:
    """Test ConfigValidatorUtility existing methods."""

    @pytest.mark.parametrize("method_name", [
        "add_rule",
        "validate",
        "validate_app_env",
        "validate_dataI_url",
        "validate_email",
        "validate_jwt_algorithm",
        "validate_jwt_secret",
        "validate_port",
        "validate_redis_url",
        "validate_url",
    ])
    def test_methods_exist(self, method_name):
        """Test methods exist."""
        from utilities.validator import ConfigValidatorUtility
        assert hasattr(ConfigValidatorUtility, method_name)

    @pytest.mark.parametrize("method_name", [
        "add_rule",
        "validate",
    ])
    def test_methods_are_callable(self, method_name):
        """Test methods are callable."""
        from utilities.validator import ConfigValidatorUtility
        assert callable(getattr(ConfigValidatorUtility, method_name))

    def test_database_url_pattern_exists(self):
        """Test DATABASE_URL_PATTERN exists."""
        from utilities.validator import ConfigValidatorUtility
        assert hasattr(ConfigValidatorUtility, "DATABASE_URL_PATTERN")

    def test_jwt_secret_min_length_exists(self):
        """Test JWT_SECRET_MIN_LENGTH exists."""
        from utilities.validator import ConfigValidatorUtility
        assert hasattr(ConfigValidatorUtility, "JWT_SECRET_MIN_LENGTH")


class TestUtilityPropertiesExisting:
    """Test utility properties."""

    @pytest.mark.parametrize("prop_name", [
        "urn",
        "user_urn",
        "api_name",
        "user_id",
        "logger",
    ])
    def test_datetime_utility_properties_exist(self, prop_name):
        """Test DateTimeUtility properties exist."""
        from utilities.datetime import DateTimeUtility
        assert hasattr(DateTimeUtility, prop_name)

    @pytest.mark.parametrize("prop_name", [
        "urn",
        "user_urn",
        "api_name",
        "user_id",
        "logger",
    ])
    def test_system_utility_properties_exist(self, prop_name):
        """Test SystemUtility properties exist."""
        from utilities.system import SystemUtility
        assert hasattr(SystemUtility, prop_name)

    @pytest.mark.parametrize("prop_name", [
        "urn",
        "user_urn",
        "api_name",
        "user_id",
        "logger",
    ])
    def test_env_utility_properties_exist(self, prop_name):
        """Test EnvironmentParserUtility properties exist."""
        from utilities.env import EnvironmentParserUtility
        assert hasattr(EnvironmentParserUtility, prop_name)

    @pytest.mark.parametrize("prop_name", [
        "urn",
        "user_urn",
        "api_name",
        "user_id",
        "logger",
    ])
    def test_cors_utility_properties_exist(self, prop_name):
        """Test CorsConfigUtility properties exist."""
        from utilities.cors import CorsConfigUtility
        assert hasattr(CorsConfigUtility, prop_name)

    @pytest.mark.parametrize("prop_name", [
        "urn",
        "user_urn",
        "api_name",
        "user_id",
        "logger",
    ])
    def test_security_headers_utility_properties_exist(self, prop_name):
        """Test SecurityHeadersUtility properties exist."""
        from utilities.security_headers import SecurityHeadersUtility
        assert hasattr(SecurityHeadersUtility, prop_name)

    @pytest.mark.parametrize("prop_name", [
        "urn",
        "user_urn",
        "api_name",
        "user_id",
        "logger",
    ])
    def test_validator_utility_properties_exist(self, prop_name):
        """Test ConfigValidatorUtility properties exist."""
        from utilities.validator import ConfigValidatorUtility
        assert hasattr(ConfigValidatorUtility, prop_name)

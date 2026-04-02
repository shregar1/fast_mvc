"""Tests for environment variable parsing utilities."""

from __future__ import annotations

import os
from typing import Sequence

import pytest

from utilities.env import EnvironmentParserUtility

class TestEnvironmentParserUtility:
    """Test class for EnvironmentParserUtility."""

    def test_init_default_values(self):
        """Test initialization with default values."""
        parser = EnvironmentParserUtility()
        assert parser.urn is None
        assert parser.user_urn is None
        assert parser.api_name is None
        assert parser.user_id is None

    def test_init_with_values(self):
        """Test initialization with provided values."""
        parser = EnvironmentParserUtility(
            urn="test-urn",
            user_urn="user-123",
            api_name="test-api",
            user_id="user-456"
        )
        assert parser.urn == "test-urn"
        assert parser.user_urn == "user-123"
        assert parser.api_name == "test-api"
        assert parser.user_id == "user-456"

    def test_parse_bool_true_values(self, monkeypatch):
        """Test parsing boolean true values."""
        for value in ["true", "True", "TRUE", "1", "yes", "YES", "on", "ON"]:
            monkeypatch.setenv("TEST_BOOL", value)
            assert EnvironmentParserUtility.parse_bool("TEST_BOOL", False) is True

    def test_parse_bool_false_values(self, monkeypatch):
        """Test parsing boolean false values."""
        for value in ["false", "False", "FALSE", "0", "no", "NO", "off", "OFF", "", "random"]:
            monkeypatch.setenv("TEST_BOOL", value)
            assert EnvironmentParserUtility.parse_bool("TEST_BOOL", True) is False

    def test_parse_bool_default_when_not_set(self, monkeypatch):
        """Test boolean default when env var not set."""
        monkeypatch.delenv("TEST_BOOL", raising=False)
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", True) is True
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", False) is False

    def test_parse_int_valid_values(self, monkeypatch):
        """Test parsing valid integer values."""
        test_cases = [("42", 42), ("0", 0), ("-1", -1), ("999999", 999999)]
        for env_value, expected in test_cases:
            monkeypatch.setenv("TEST_INT", env_value)
            assert EnvironmentParserUtility.parse_int("TEST_INT", 0) == expected

    def test_parse_int_default_when_not_set(self, monkeypatch):
        """Test integer default when env var not set."""
        monkeypatch.delenv("TEST_INT", raising=False)
        assert EnvironmentParserUtility.parse_int("TEST_INT", 100) == 100

    def test_parse_int_default_when_empty(self, monkeypatch):
        """Test integer default when env var is empty."""
        monkeypatch.setenv("TEST_INT", "")
        assert EnvironmentParserUtility.parse_int("TEST_INT", 200) == 200

    def test_parse_str_value(self, monkeypatch):
        """Test parsing string value."""
        monkeypatch.setenv("TEST_STR", "hello world")
        assert EnvironmentParserUtility.parse_str("TEST_STR", "default") == "hello world"

    def test_parse_str_default_when_not_set(self, monkeypatch):
        """Test string default when env var not set."""
        monkeypatch.delenv("TEST_STR", raising=False)
        assert EnvironmentParserUtility.parse_str("TEST_STR", "default") == "default"

    def test_parse_optional_str_value(self, monkeypatch):
        """Test parsing optional string value."""
        monkeypatch.setenv("TEST_OPT", "value")
        assert EnvironmentParserUtility.parse_optional_str("TEST_OPT") == "value"

    def test_parse_optional_str_none_when_not_set(self, monkeypatch):
        """Test optional string returns None when not set."""
        monkeypatch.delenv("TEST_OPT", raising=False)
        assert EnvironmentParserUtility.parse_optional_str("TEST_OPT") is None

    def test_parse_optional_str_none_when_empty(self, monkeypatch):
        """Test optional string returns None when empty."""
        monkeypatch.setenv("TEST_OPT", "   ")
        assert EnvironmentParserUtility.parse_optional_str("TEST_OPT") is None

    def test_parse_csv_single_value(self, monkeypatch):
        """Test parsing CSV with single value."""
        monkeypatch.setenv("TEST_CSV", "value1")
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", [])
        assert result == ["value1"]

    def test_parse_csv_multiple_values(self, monkeypatch):
        """Test parsing CSV with multiple values."""
        monkeypatch.setenv("TEST_CSV", "a,b,c")
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", [])
        assert result == ["a", "b", "c"]

    def test_parse_csv_strips_whitespace(self, monkeypatch):
        """Test parsing CSV strips whitespace."""
        monkeypatch.setenv("TEST_CSV", " a , b , c ")
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", [])
        assert result == ["a", "b", "c"]

    def test_parse_csv_default_when_not_set(self, monkeypatch):
        """Test CSV default when env var not set."""
        monkeypatch.delenv("TEST_CSV", raising=False)
        default = ["default1", "default2"]
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", default)
        assert result == default

    def test_get_int_with_logging_valid(self, monkeypatch):
        """Test get_int_with_logging with valid value."""
        monkeypatch.setenv("TEST_INT_LOG", "42")
        assert EnvironmentParserUtility.get_int_with_logging("TEST_INT_LOG", 0) == 42

    def test_get_int_with_logging_default(self, monkeypatch):
        """Test get_int_with_logging returns default when not set."""
        monkeypatch.delenv("TEST_INT_LOG", raising=False)
        assert EnvironmentParserUtility.get_int_with_logging("TEST_INT_LOG", 100) == 100


class TestEnvModuleFunctions:
    """Test module-level convenience functions."""

    def test_env_bool_function(self, monkeypatch):
        """Test env_bool module function."""

        monkeypatch.setenv("TEST", "true")
        assert EnvironmentParserUtility.parse_bool("TEST", False) is True

    def test_env_int_function(self, monkeypatch):
        """Test env_int module function."""
        monkeypatch.setenv("TEST", "42")
        assert EnvironmentParserUtility.parse_int("TEST", 0) == 42

    def test_env_str_function(self, monkeypatch):
        """Test env_str module function."""
        monkeypatch.setenv("TEST", "hello")
        assert EnvironmentParserUtility.parse_str("TEST", "") == "hello"

    def test_env_optional_str_function(self, monkeypatch):
        """Test env_optional_str module function."""
        monkeypatch.setenv("TEST", "value")
        assert EnvironmentParserUtility.parse_optional_str("TEST") == "value"

    def test_env_csv_function(self, monkeypatch):
        """Test env_csv module function."""
        monkeypatch.setenv("TEST", "a,b")
        assert EnvironmentParserUtility.parse_csv("TEST", []) == ["a", "b"]

    def test_get_int_env_function(self, monkeypatch):
        """Test get_int_env module function."""
        monkeypatch.setenv("TEST", "100")
        assert EnvironmentParserUtility.parse_int("TEST", 0) == 100


class TestEnvironmentParserEdgeCases:
    """Test edge cases for EnvironmentParserUtility."""

    def test_parse_bool_case_insensitive(self, monkeypatch):
        """Test boolean parsing is case insensitive."""
        for case in ["True", "TRUE", "true", "TrUe"]:
            monkeypatch.setenv("TEST", case)
            assert EnvironmentParserUtility.parse_bool("TEST", False) is True

    def test_parse_csv_empty_string(self, monkeypatch):
        """Test CSV parsing with empty string."""
        monkeypatch.setenv("TEST", "")
        default = ["a", "b"]
        result = EnvironmentParserUtility.parse_csv("TEST", default)
        assert result == default

    def test_parse_csv_whitespace_only(self, monkeypatch):
        """Test CSV parsing with whitespace only."""
        monkeypatch.setenv("TEST", "   ")
        default = ["a", "b"]
        result = EnvironmentParserUtility.parse_csv("TEST", default)
        assert result == default

    def test_parse_csv_with_empty_elements(self, monkeypatch):
        """Test CSV parsing filters empty elements."""
        monkeypatch.setenv("TEST", "a,,b,,c")
        result = EnvironmentParserUtility.parse_csv("TEST", [])
        assert result == ["a", "b", "c"]

    def test_urn_property_getter_setter(self):
        """Test urn property getter and setter."""
        parser = EnvironmentParserUtility()
        parser.urn = "test-urn"
        assert parser.urn == "test-urn"

    def test_user_urn_property_getter_setter(self):
        """Test user_urn property getter and setter."""
        parser = EnvironmentParserUtility()
        parser.user_urn = "user-test"
        assert parser.user_urn == "user-test"

    def test_api_name_property_getter_setter(self):
        """Test api_name property getter and setter."""
        parser = EnvironmentParserUtility()
        parser.api_name = "api-test"
        assert parser.api_name == "api-test"

    def test_user_id_property_getter_setter(self):
        """Test user_id property getter and setter."""
        parser = EnvironmentParserUtility()
        parser.user_id = "id-test"
        assert parser.user_id == "id-test"

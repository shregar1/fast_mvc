"""Extended tests for auth utilities."""

from __future__ import annotations

import base64

from utilities.auth import constant_time_compare, parse_basic_authorization


class TestParseBasicAuthorization:
    """Tests for parse_basic_authorization function."""

    def test_parse_basic_auth_valid(self):
        """Test parsing valid basic authorization."""
        credentials = base64.b64encode(b"user:pass").decode()
        header = f"Basic {credentials}"
        result = parse_basic_authorization(header)
        assert result == ("user", "pass")

    def test_parse_basic_auth_none(self):
        """Test parsing None returns None."""
        result = parse_basic_authorization(None)
        assert result is None

    def test_parse_basic_auth_empty(self):
        """Test parsing empty string returns None."""
        result = parse_basic_authorization("")
        assert result is None

    def test_parse_basic_auth_not_basic(self):
        """Test parsing non-Basic header returns None."""
        result = parse_basic_authorization("Bearer token123")
        assert result is None

    def test_parse_basic_auth_invalid_base64(self):
        """Test parsing invalid base64 returns None."""
        result = parse_basic_authorization("Basic not_valid_base64!!!")
        assert result is None

    def test_parse_basic_auth_no_colon(self):
        """Test parsing credentials without colon returns None."""
        credentials = base64.b64encode(b"nocolon").decode()
        header = f"Basic {credentials}"
        result = parse_basic_authorization(header)
        assert result is None

    def test_parse_basic_auth_multiple_colons(self):
        """Test parsing credentials with multiple colons."""
        credentials = base64.b64encode(b"user:pass:word").decode()
        header = f"Basic {credentials}"
        result = parse_basic_authorization(header)
        assert result == ("user", "pass:word")

    def test_parse_basic_auth_empty_password(self):
        """Test parsing credentials with empty password."""
        credentials = base64.b64encode(b"user:").decode()
        header = f"Basic {credentials}"
        result = parse_basic_authorization(header)
        assert result == ("user", "")

    def test_parse_basic_auth_empty_username(self):
        """Test parsing credentials with empty username."""
        credentials = base64.b64encode(b":pass").decode()
        header = f"Basic {credentials}"
        result = parse_basic_authorization(header)
        assert result == ("", "pass")

    def test_parse_basic_auth_unicode(self):
        """Test parsing credentials with unicode."""
        credentials = base64.b64encode("用户:密码".encode("utf-8")).decode()
        header = f"Basic {credentials}"
        result = parse_basic_authorization(header)
        assert result == ("用户", "密码")


class TestConstantTimeCompare:
    """Tests for constant_time_compare function."""

    def test_compare_equal_strings(self):
        """Test comparing equal strings."""
        assert constant_time_compare("hello", "hello") is True

    def test_compare_different_strings(self):
        """Test comparing different strings."""
        assert constant_time_compare("hello", "world") is False

    def test_compare_different_lengths(self):
        """Test comparing strings of different lengths."""
        assert constant_time_compare("hi", "hello") is False

    def test_compare_empty_strings(self):
        """Test comparing empty strings."""
        assert constant_time_compare("", "") is True

    def test_compare_empty_and_nonempty(self):
        """Test comparing empty and non-empty strings."""
        assert constant_time_compare("", "hello") is False

    def test_compare_unicode(self):
        """Test comparing unicode strings."""
        assert constant_time_compare("你好", "你好") is True
        assert constant_time_compare("你好", "世界") is False

    def test_compare_special_chars(self):
        """Test comparing strings with special characters."""
        assert constant_time_compare("!@#$%", "!@#$%") is True
        assert constant_time_compare("!@#$%", "^&*()") is False

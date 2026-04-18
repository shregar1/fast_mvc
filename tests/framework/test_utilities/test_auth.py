"""Tests for :mod:`utilities.auth` module-level helpers."""

from __future__ import annotations

import base64

from utilities.auth import constant_time_compare, parse_basic_authorization


class TestParseBasicAuthorization:
    def test_parse_basic_authorization_valid(self) -> None:
        raw = base64.b64encode(b"user:secret").decode("ascii")
        parsed = parse_basic_authorization(f"Basic {raw}")
        assert parsed == ("user", "secret")

    def test_parse_basic_authorization_invalid(self) -> None:
        assert parse_basic_authorization(None) is None
        assert parse_basic_authorization("Bearer x") is None
        assert parse_basic_authorization("Basic !!!") is None


class TestConstantTimeCompare:
    def test_constant_time_compare_equal(self) -> None:
        assert constant_time_compare("hello", "hello") is True

    def test_constant_time_compare_different(self) -> None:
        assert constant_time_compare("hello", "world") is False

    def test_constant_time_compare_different_lengths(self) -> None:
        assert constant_time_compare("hello", "hello world") is False

    def test_constant_time_compare_empty_strings(self) -> None:
        assert constant_time_compare("", "") is True

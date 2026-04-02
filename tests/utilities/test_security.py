"""Tests for security headers utilities."""

from __future__ import annotations

from typing import Dict, List, Optional
from unittest.mock import patch, MagicMock

import pytest

from utilities.security import SecurityHeadersUtility


class TestSecurityHeadersUtility:
    """Test class for SecurityHeadersUtility."""

    def test_init_default_values(self):
        """Test initialization with default values."""
        util = SecurityHeadersUtility()
        assert util.urn is None
        assert util.user_urn is None

    def test_init_with_context(self):
        """Test initialization with context."""
        util = SecurityHeadersUtility(
            urn="test",
            user_urn="user",
            api_name="api",
            user_id="id"
        )
        assert util.urn == "test"
        assert util.user_urn == "user"

    def test_get_default_headers(self):
        """Test getting default security headers."""
        headers = SecurityHeadersUtility.get_default_headers()
        assert isinstance(headers, dict)
        assert len(headers) > 0

    def test_get_default_headers_x_frame_options(self):
        """Test default headers include X-Frame-Options."""
        headers = SecurityHeadersUtility.get_default_headers()
        assert "X-Frame-Options" in headers

    def test_get_default_headers_x_content_type(self):
        """Test default headers include X-Content-Type-Options."""
        headers = SecurityHeadersUtility.get_default_headers()
        assert "X-Content-Type-Options" in headers

    def test_get_default_headers_x_xss_protection(self):
        """Test default headers include X-XSS-Protection."""
        headers = SecurityHeadersUtility.get_default_headers()
        assert "X-XSS-Protection" in headers

    def test_get_default_headers_strict_transport(self):
        """Test default headers include Strict-Transport-Security."""
        headers = SecurityHeadersUtility.get_default_headers()
        assert "Strict-Transport-Security" in headers

    def test_get_default_headers_referrer_policy(self):
        """Test default headers include Referrer-Policy."""
        headers = SecurityHeadersUtility.get_default_headers()
        assert "Referrer-Policy" in headers

    def test_get_default_headers_permissions_policy(self):
        """Test default headers include Permissions-Policy."""
        headers = SecurityHeadersUtility.get_default_headers()
        assert "Permissions-Policy" in headers

    def test_get_production_headers(self):
        """Test getting production security headers."""
        headers = SecurityHeadersUtility.get_production_headers()
        assert isinstance(headers, dict)
        assert len(headers) > 0

    def test_get_development_headers(self):
        """Test getting development security headers."""
        headers = SecurityHeadersUtility.get_development_headers()
        assert isinstance(headers, dict)
        assert len(headers) > 0

    def test_add_csp_header(self):
        """Test adding Content-Security-Policy header."""
        headers = SecurityHeadersUtility.add_csp_header({}, "default-src 'self'")
        assert headers["Content-Security-Policy"] == "default-src 'self'"

    def test_add_csp_header_with_existing(self):
        """Test adding CSP header with existing headers."""
        existing = {"X-Frame-Options": "DENY"}
        headers = SecurityHeadersUtility.add_csp_header(existing, "default-src 'self'")
        assert "X-Frame-Options" in headers
        assert "Content-Security-Policy" in headers

    def test_build_csp_policy_basic(self):
        """Test building basic CSP policy."""
        policy = SecurityHeadersUtility.build_csp_policy(
            default_src=["'self'"]
        )
        assert "default-src 'self'" in policy

    def test_build_csp_policy_multiple_directives(self):
        """Test building CSP with multiple directives."""
        policy = SecurityHeadersUtility.build_csp_policy(
            default_src=["'self'"],
            script_src=["'self'", "'unsafe-inline'"],
            style_src=["'self'"]
        )
        assert "default-src" in policy
        assert "script-src" in policy
        assert "style-src" in policy

    def test_build_csp_policy_empty(self):
        """Test building empty CSP policy."""
        policy = SecurityHeadersUtility.build_csp_policy()
        assert policy == ""

    def test_add_feature_policy(self):
        """Test adding feature policy header."""
        headers = SecurityHeadersUtility.add_feature_policy(
            {},
            camera="'none'",
            microphone="'self'"
        )
        assert "Permissions-Policy" in headers
        assert "camera" in headers["Permissions-Policy"]

    def test_merge_headers(self):
        """Test merging header dictionaries."""
        headers1 = {"X-Frame-Options": "DENY"}
        headers2 = {"X-Content-Type-Options": "nosniff"}
        merged = SecurityHeadersUtility.merge_headers(headers1, headers2)
        assert "X-Frame-Options" in merged
        assert "X-Content-Type-Options" in merged

    def test_merge_headers_overwrite(self):
        """Test merging headers with overwrite."""
        headers1 = {"X-Frame-Options": "DENY"}
        headers2 = {"X-Frame-Options": "SAMEORIGIN"}
        merged = SecurityHeadersUtility.merge_headers(headers1, headers2)
        assert merged["X-Frame-Options"] == "SAMEORIGIN"

    def test_remove_header(self):
        """Test removing a header."""
        headers = {"X-Frame-Options": "DENY", "X-Content-Type-Options": "nosniff"}
        result = SecurityHeadersUtility.remove_header(headers, "X-Frame-Options")
        assert "X-Frame-Options" not in result
        assert "X-Content-Type-Options" in result

    def test_set_header(self):
        """Test setting a header."""
        headers = {"X-Frame-Options": "DENY"}
        result = SecurityHeadersUtility.set_header(headers, "Custom-Header", "value")
        assert result["Custom-Header"] == "value"
        assert result["X-Frame-Options"] == "DENY"

    def test_set_header_overwrite(self):
        """Test setting a header overwrites existing."""
        headers = {"X-Frame-Options": "DENY"}
        result = SecurityHeadersUtility.set_header(headers, "X-Frame-Options", "SAMEORIGIN")
        assert result["X-Frame-Options"] == "SAMEORIGIN"

    def test_validate_headers(self):
        """Test validating headers."""
        headers = {"X-Frame-Options": "DENY"}
        assert SecurityHeadersUtility.validate_headers(headers) is True

    def test_validate_headers_empty(self):
        """Test validating empty headers."""
        assert SecurityHeadersUtility.validate_headers({}) is True

    def test_sanitize_header_value(self):
        """Test sanitizing header value."""
        result = SecurityHeadersUtility.sanitize_header_value("value\nwith\nnewlines")
        assert "\n" not in result

    def test_sanitize_header_value_removes_carriage(self):
        """Test sanitizing removes carriage returns."""
        result = SecurityHeadersUtility.sanitize_header_value("value\r\n")
        assert "\r" not in result


class TestSecurityHeadersUtilityProperties:
    """Test properties."""

    def test_urn_property(self):
        """Test urn property."""
        util = SecurityHeadersUtility()
        util.urn = "test"
        assert util.urn == "test"

    def test_user_urn_property(self):
        """Test user_urn property."""
        util = SecurityHeadersUtility()
        util.user_urn = "user"
        assert util.user_urn == "user"

    def test_api_name_property(self):
        """Test api_name property."""
        util = SecurityHeadersUtility()
        util.api_name = "api"
        assert util.api_name == "api"

    def test_user_id_property(self):
        """Test user_id property."""
        util = SecurityHeadersUtility()
        util.user_id = "id"
        assert util.user_id == "id"

    def test_logger_access(self):
        """Test logger is accessible."""
        util = SecurityHeadersUtility()
        assert util.logger is not None


class TestSecurityHeadersUtilityEdgeCases:
    """Test edge cases."""

    def test_add_csp_header_empty_policy(self):
        """Test adding empty CSP policy."""
        headers = SecurityHeadersUtility.add_csp_header({}, "")
        assert headers.get("Content-Security-Policy") == ""

    def test_build_csp_policy_none_values(self):
        """Test building CSP with None values."""
        policy = SecurityHeadersUtility.build_csp_policy(
            default_src=None,
            script_src=["'self'"]
        )
        assert "default-src" not in policy
        assert "script-src" in policy

    def test_merge_headers_empty_dictionaries(self):
        """Test merging empty dictionaries."""
        result = SecurityHeadersUtility.merge_headers({}, {})
        assert result == {}

    def test_remove_header_nonexistent(self):
        """Test removing nonexistent header."""
        headers = {"X-Frame-Options": "DENY"}
        result = SecurityHeadersUtility.remove_header(headers, "Non-Existent")
        assert result == headers

    def test_sanitize_header_value_empty(self):
        """Test sanitizing empty header value."""
        result = SecurityHeadersUtility.sanitize_header_value("")
        assert result == ""

    def test_validate_headers_none(self):
        """Test validating None headers."""
        with pytest.raises((TypeError, AttributeError)):
            SecurityHeadersUtility.validate_headers(None)

    def test_get_development_headers_less_strict(self):
        """Test development headers are less strict."""
        dev = SecurityHeadersUtility.get_development_headers()
        prod = SecurityHeadersUtility.get_production_headers()
        # Development should have at least as many headers
        assert len(dev) >= len(prod)

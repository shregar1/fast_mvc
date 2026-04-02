"""Tests for auth utilities."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Optional, Tuple
from unittest.mock import patch, MagicMock

import pytest

from utilities.auth import AuthUtility


class TestAuthUtility:
    """Test class for AuthUtility."""

    def test_init_default_values(self):
        """Test initialization with default values."""
        util = AuthUtility()
        assert util.urn is None
        assert util.user_urn is None

    def test_init_with_context(self):
        """Test initialization with context."""
        util = AuthUtility(urn="test", user_urn="user")
        assert util.urn == "test"
        assert util.user_urn == "user"

    def test_hash_password_returns_string(self):
        """Test hash_password returns a string."""
        result = AuthUtility.hash_password("mypassword")
        assert isinstance(result, str)

    def test_hash_password_different_salts(self):
        """Test hash_password returns different hashes for same password."""
        hash1 = AuthUtility.hash_password("mypassword")
        hash2 = AuthUtility.hash_password("mypassword")
        assert hash1 != hash2  # Different salts

    def test_verify_password_correct(self):
        """Test verify_password with correct password."""
        hashed = AuthUtility.hash_password("mypassword")
        assert AuthUtility.verify_password("mypassword", hashed) is True

    def test_verify_password_incorrect(self):
        """Test verify_password with incorrect password."""
        hashed = AuthUtility.hash_password("mypassword")
        assert AuthUtility.verify_password("wrongpassword", hashed) is False

    def test_generate_token_length(self):
        """Test generate_token returns token of correct length."""
        token = AuthUtility.generate_token(32)
        # Hex representation is 2x the byte length
        assert len(token) == 64

    def test_generate_token_uniqueness(self):
        """Test generate_token returns unique tokens."""
        tokens = {AuthUtility.generate_token(32) for _ in range(100)}
        assert len(tokens) == 100

    def test_generate_secure_random(self):
        """Test generate_secure_random returns bytes."""
        result = AuthUtility.generate_secure_random(32)
        assert isinstance(result, bytes)
        assert len(result) == 32

    def test_generate_api_key_format(self):
        """Test generate_api_key returns correct format."""
        api_key = AuthUtility.generate_api_key()
        assert isinstance(api_key, str)
        assert len(api_key) > 20

    def test_generate_api_key_prefix(self):
        """Test generate_api_key includes prefix."""
        api_key = AuthUtility.generate_api_key(prefix="test")
        assert api_key.startswith("test_")

    def test_generate_api_key_unique(self):
        """Test generate_api_key returns unique keys."""
        keys = {AuthUtility.generate_api_key() for _ in range(100)}
        assert len(keys) == 100

    def test_generate_secret_key(self):
        """Test generate_secret_key."""
        key = AuthUtility.generate_secret_key()
        assert isinstance(key, str)
        assert len(key) >= 32

    def test_create_jwt_payload(self):
        """Test creating JWT payload."""
        payload = AuthUtility.create_jwt_payload(user_id="123", roles=["admin"])
        assert payload["sub"] == "123"
        assert "admin" in payload["roles"]
        assert "exp" in payload
        assert "iat" in payload

    def test_create_jwt_payload_with_custom_claims(self):
        """Test creating JWT payload with custom claims."""
        payload = AuthUtility.create_jwt_payload(user_id="123", custom_claim={"key": "value"})
        assert payload["custom_claim"]["key"] == "value"

    def test_generate_hmac(self):
        """Test generating HMAC."""
        message = "hello world"
        secret = "mysecret"
        hmac_result = AuthUtility.generate_hmac(message, secret)
        assert isinstance(hmac_result, str)
        assert len(hmac_result) > 0

    def test_verify_hmac_valid(self):
        """Test verifying valid HMAC."""
        message = "hello world"
        secret = "mysecret"
        hmac_value = AuthUtility.generate_hmac(message, secret)
        assert AuthUtility.verify_hmac(message, secret, hmac_value) is True

    def test_verify_hmac_invalid(self):
        """Test verifying invalid HMAC."""
        message = "hello world"
        secret = "mysecret"
        assert AuthUtility.verify_hmac(message, secret, "invalid_hmac") is False

    def test_hash_sha256(self):
        """Test SHA256 hashing."""
        result = AuthUtility.hash_sha256("hello")
        expected = hashlib.sha256("hello".encode()).hexdigest()
        assert result == expected

    def test_hash_sha512(self):
        """Test SHA512 hashing."""
        result = AuthUtility.hash_sha512("hello")
        expected = hashlib.sha512("hello".encode()).hexdigest()
        assert result == expected

    def test_base64_encode(self):
        """Test base64 encoding."""
        result = AuthUtility.base64_encode("hello")
        assert isinstance(result, str)
        assert result == "aGVsbG8="

    def test_base64_decode(self):
        """Test base64 decoding."""
        result = AuthUtility.base64_decode("aGVsbG8=")
        assert result == "hello"

    def test_base64_urlsafe_encode(self):
        """Test URL-safe base64 encoding."""
        result = AuthUtility.base64_urlsafe_encode("hello+world/")
        assert "+" not in result
        assert "/" not in result

    def test_base64_urlsafe_decode(self):
        """Test URL-safe base64 decoding."""
        encoded = AuthUtility.base64_urlsafe_encode("hello")
        result = AuthUtility.base64_urlsafe_decode(encoded)
        assert result == "hello"

    def test_constant_time_compare_equal(self):
        """Test constant time compare with equal strings."""
        assert AuthUtility.constant_time_compare("hello", "hello") is True

    def test_constant_time_compare_different(self):
        """Test constant time compare with different strings."""
        assert AuthUtility.constant_time_compare("hello", "world") is False

    def test_constant_time_compare_different_lengths(self):
        """Test constant time compare with different length strings."""
        assert AuthUtility.constant_time_compare("hello", "hello world") is False

    def test_generate_totp_secret(self):
        """Test generating TOTP secret."""
        secret = AuthUtility.generate_totp_secret()
        assert isinstance(secret, str)
        assert len(secret) > 0

    def test_generate_backup_codes(self):
        """Test generating backup codes."""
        codes = AuthUtility.generate_backup_codes(count=5)
        assert isinstance(codes, list)
        assert len(codes) == 5
        assert len(set(codes)) == 5  # All unique

    def test_generate_backup_codes_length(self):
        """Test backup codes are correct length."""
        codes = AuthUtility.generate_backup_codes(count=1, length=8)
        assert len(codes[0]) == 8


class TestAuthUtilityProperties:
    """Test properties."""

    def test_urn_property(self):
        """Test urn property."""
        util = AuthUtility()
        util.urn = "test"
        assert util.urn == "test"

    def test_user_urn_property(self):
        """Test user_urn property."""
        util = AuthUtility()
        util.user_urn = "user"
        assert util.user_urn == "user"

    def test_api_name_property(self):
        """Test api_name property."""
        util = AuthUtility()
        util.api_name = "api"
        assert util.api_name == "api"

    def test_user_id_property(self):
        """Test user_id property."""
        util = AuthUtility()
        util.user_id = "id"
        assert util.user_id == "id"

    def test_logger_access(self):
        """Test logger is accessible."""
        util = AuthUtility()
        assert util.logger is not None


class TestAuthUtilityEdgeCases:
    """Test edge cases."""

    def test_hash_password_empty(self):
        """Test hashing empty password."""
        hashed = AuthUtility.hash_password("")
        assert isinstance(hashed, str)
        assert AuthUtility.verify_password("", hashed) is True

    def test_verify_password_malformed_hash(self):
        """Test verify_password with malformed hash."""
        assert AuthUtility.verify_password("password", "malformed") is False

    def test_generate_token_zero_length(self):
        """Test generate_token with zero length."""
        token = AuthUtility.generate_token(0)
        assert token == ""

    def test_base64_decode_invalid(self):
        """Test base64 decode with invalid input."""
        with pytest.raises(Exception):
            AuthUtility.base64_decode("!!!invalid!!!")

    def test_hmac_with_empty_message(self):
        """Test HMAC with empty message."""
        hmac_result = AuthUtility.generate_hmac("", "secret")
        assert isinstance(hmac_result, str)
        assert len(hmac_result) > 0

    def test_constant_time_compare_empty_strings(self):
        """Test constant time compare with empty strings."""
        assert AuthUtility.constant_time_compare("", "") is True

    def test_create_jwt_payload_no_roles(self):
        """Test JWT payload without roles."""
        payload = AuthUtility.create_jwt_payload(user_id="123")
        assert "roles" not in payload or payload["roles"] == []

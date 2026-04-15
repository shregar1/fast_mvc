"""JWT utility – token generation and validation."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import jwt as pyjwt

from constants.default import Default
from start_utils import logger


class JWTUtility:
    """Stateless helper for encoding / decoding JSON Web Tokens."""

    def __init__(
        self,
        secret_key: str = "",
        algorithm: str = "HS256",
        *,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._urn = urn
        self._user_urn = user_urn
        self._api_name = api_name
        self._user_id = user_id
        self._logger = logger.bind(urn=urn, user_urn=user_urn, api_name=api_name)

    def generate_token(
        self,
        payload: dict[str, Any],
        *,
        expires_minutes: int = Default.ACCESS_TOKEN_EXPIRE_MINUTES_SHORT,
    ) -> str:
        """Generate a signed JWT with UTC expiry."""
        data = {**payload}
        data["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
        data["iat"] = datetime.now(timezone.utc)
        token = pyjwt.encode(data, self._secret_key, algorithm=self._algorithm)
        return token if isinstance(token, str) else token.decode(Default.ENCODING_UTF8)

    def decode_token(self, token: str) -> dict[str, Any]:
        """Decode and verify a JWT. Raises on expiry / bad signature."""
        return pyjwt.decode(token, self._secret_key, algorithms=[self._algorithm])

    def generate_refresh_token(
        self,
        payload: dict[str, Any],
        *,
        expires_days: int = Default.REFRESH_TOKEN_EXPIRE_DAYS,
    ) -> str:
        """Generate a long-lived refresh token with UTC expiry."""
        data = {**payload}
        data["exp"] = datetime.now(timezone.utc) + timedelta(days=expires_days)
        data["iat"] = datetime.now(timezone.utc)
        data["type"] = "refresh"
        token = pyjwt.encode(data, self._secret_key, algorithm=self._algorithm)
        return token if isinstance(token, str) else token.decode(Default.ENCODING_UTF8)


__all__ = ["JWTUtility"]

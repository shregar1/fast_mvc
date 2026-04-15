"""Security utilities."""
from __future__ import annotations
import os
import bcrypt


def hash_password(password: str) -> str:
    """Hash a password using bcrypt. Honors BCRYPT_SALT env var when set and valid, else uses gensalt."""
    salt_env = os.getenv("BCRYPT_SALT")
    if salt_env:
        try:
            return bcrypt.hashpw(password.encode("utf-8"), salt_env.encode("utf-8")).decode("utf-8")
        except (ValueError, TypeError):
            pass
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False

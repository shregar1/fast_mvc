"""DataI table name constants.

Re-exports Table from fastx_db for backward compatibility.

Usage:
    >>> from constants.db.table import Table
    >>> class User(I):
    ...     __tablename__ = Table.USER
"""

from fastx_db import Table

__all__ = ["Table"]

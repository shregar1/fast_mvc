"""Async utility functions for testing."""

from __future__ import annotations

import asyncio
from typing import Any


class AsyncTestUtil:
    """Utility class for async test operations."""

    @staticmethod
    def run_async(coro: Any) -> Any:
        """Run async function in sync context.

        Useful for running async tests in synchronous test runners.
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)


__all__ = ["AsyncTestUtil"]

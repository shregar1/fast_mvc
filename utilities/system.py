"""System and process utilities."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Optional

from abstractions.utility import IUtility


class SystemUtility(IUtility):
    """Utility class for system and process operations."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the system utility.

        Args:
            urn: Unique Request Number for tracing.
            user_urn: User's unique resource name.
            api_name: Name of the API endpoint.
            user_id: Database identifier of the user.
            *args: Additional positional arguments forwarded to parent.
            **kwargs: Additional keyword arguments forwarded to parent.
        """
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            *args,
            **kwargs,
        )

    @staticmethod
    def git_repository_folder_name() -> Optional[str]:
        """Return the git work tree root directory name, or None if unavailable.

        Attempts to find the git repository root by running git commands
        from multiple candidate directories.

        Returns:
            The git repository folder name, or None if not in a git repository.
        """
        candidates: list[Path] = []
        try:
            candidates.append(Path.cwd().resolve())
        except OSError:
            pass
        try:
            # Get parent of the directory containing this file
            candidates.append(Path(__file__).resolve().parents[2])
        except IndexError:
            pass
        seen: set[Path] = set()
        for cwd in candidates:
            if cwd in seen:
                continue
            seen.add(cwd)
            try:
                proc = subprocess.run(
                    ["git", "rev-parse", "--show-toplevel"],
                    cwd=str(cwd),
                    capture_output=True,
                    text=True,
                    timeout=3,
                    check=False,
                )
            except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
                continue
            if proc.returncode != 0 or not proc.stdout.strip():
                continue
            return Path(proc.stdout.strip()).name
        return None


__all__ = [
    "SystemUtility",
]

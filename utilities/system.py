"""System and process utilities."""

from __future__ import annotations

import subprocess
from pathlib import Path


class SystemUtil:
    """Utility class for system and process operations."""

    @staticmethod
    def git_repository_folder_name() -> str | None:
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


# Backward compatibility: module-level functions delegate to the class
git_repository_folder_name = SystemUtil.git_repository_folder_name


__all__ = [
    "SystemUtil",
    "git_repository_folder_name",
]

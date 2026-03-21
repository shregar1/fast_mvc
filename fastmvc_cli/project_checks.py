"""Shared filesystem checks for FastMVC CLI commands."""

from __future__ import annotations

import sys
from pathlib import Path

import click

_DEFAULT_MSG = (
    "✗ Not in a FastMVC project directory. "
    "Run this command from your project root (where app.py lives)."
)


def require_fastmvc_project_root(msg: str | None = None) -> Path:
    """Return cwd if ``app.py`` exists; otherwise print *msg* and exit."""
    project_path = Path.cwd()
    if not (project_path / "app.py").is_file():
        click.secho(msg or _DEFAULT_MSG, fg="red")
        sys.exit(1)
    return project_path

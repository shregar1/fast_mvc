"""
Resolve ``alembic.ini`` for projects in subdirectories and build Alembic argv.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def find_alembic_ini(start: Path | None = None) -> Path | None:
    """
    Walk ``start`` (default: cwd) and parents for ``alembic.ini``.
    """
    cur = (start or Path.cwd()).resolve()
    for directory in [cur, *cur.parents]:
        candidate = directory / "alembic.ini"
        if candidate.is_file():
            return candidate
    return None


def alembic_base_args(ini: Path | None) -> list[str]:
    """``alembic`` plus optional ``-c`` path."""
    cmd = ["alembic"]
    if ini is not None:
        cmd.extend(["-c", str(ini)])
    return cmd


def alembic_cwd(ini: Path | None) -> Path | None:
    """Working directory for Alembic (directory containing ``alembic.ini``)."""
    return ini.parent if ini is not None else None


def run_alembic(argv: list[str]) -> subprocess.CompletedProcess:
    """
    Run ``alembic`` with argv, resolving ``alembic.ini`` from cwd upward.

    Raises:
        FileNotFoundError: If the ``alembic`` executable is not on PATH.
    """
    ini = find_alembic_ini()
    cwd = alembic_cwd(ini)
    cmd = alembic_base_args(ini) + argv
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

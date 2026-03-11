"""
End-to-end smoke test for the FastMVC project generator.

This test verifies that a generated project can:
- Be created successfully into a temporary directory
- Run Alembic migrations
- Run its unit test suite
"""

import os
import subprocess
from pathlib import Path

import pytest

from fastmvc_cli.generator import ProjectGenerator


@pytest.mark.slow
def test_smoke_generate_migrate_and_test(tmp_path: Path) -> None:
    """
    Full smoke test:

    1. Generate a new project using ProjectGenerator
    2. Configure it to use SQLite (file-based DB) to avoid external services
    3. Run Alembic migrations
    4. Run pytest in the generated project
    """
    project_name = "smoke_project"
    output_dir = tmp_path

    # 1) Generate project (keep options simple to avoid external dependencies)
    generator = ProjectGenerator(
        project_name=project_name,
        output_dir=str(output_dir),
        init_git=False,
        create_venv=False,
        install_deps=False,
    )

    # Force SQLite to avoid requiring a running Postgres instance
    generator.db_backend = "sqlite"
    generator.db_name = project_name
    generator.db_host = ""
    generator.db_port = ""
    generator.use_redis = False

    generator.generate()

    project_path = output_dir / project_name
    assert (project_path / "app.py").exists()
    assert (project_path / "alembic.ini").exists()
    assert (project_path / "migrations").exists()

    # Ensure DB config exists and has been customized
    db_config = project_path / "config" / "db" / "config.json"
    assert db_config.exists()

    env = os.environ.copy()
    # Make sure Python can import from the generated project
    env.setdefault("PYTHONPATH", str(project_path))

    # 3) Run Alembic migrations
    alembic_result = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=project_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert (
        alembic_result.returncode == 0
    ), f"Alembic failed:\nSTDOUT:\n{alembic_result.stdout}\nSTDERR:\n{alembic_result.stderr}"

    # 4) Run pytest unit tests in the generated project
    pytest_result = subprocess.run(
        ["pytest", "tests/unit", "-q"],
        cwd=project_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert (
        pytest_result.returncode == 0
    ), f"pytest failed:\nSTDOUT:\n{pytest_result.stdout}\nSTDERR:\n{pytest_result.stderr}"


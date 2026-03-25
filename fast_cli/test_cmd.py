"""
`fastmvc test` — Run tests with coverage and reporting.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_tests(
    project_dir: Path,
    paths: list[str] | None = None,
    pattern: str | None = None,
    verbose: bool = False,
    coverage: bool = False,
    coverage_html: bool = False,
    coverage_xml: bool = False,
    failfast: bool = False,
    markers: list[str] | None = None,
    parallel: bool = False,
    watch: bool = False,
    maxfail: int | None = None,
    no_header: bool = False,
) -> int:
    """
    Run tests with pytest.
    
    Args:
        project_dir: Project root directory
        paths: Specific test paths to run
        pattern: Test name pattern to match
        verbose: Verbose output
        coverage: Enable coverage reporting
        coverage_html: Generate HTML coverage report
        coverage_xml: Generate XML coverage report
        failfast: Stop on first failure
        markers: Pytest markers to filter by
        parallel: Run tests in parallel
        watch: Watch for changes and re-run
        maxfail: Stop after N failures
        no_header: Suppress pytest header
    
    Returns:
        pytest exit code
    """
    cmd = [sys.executable, "-m", "pytest"]
    
    # Build pytest arguments
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-v" if not no_header else "--tb=short")
    
    if failfast:
        cmd.append("-x")
    
    if maxfail:
        cmd.extend(["--maxfail", str(maxfail)])
    
    if pattern:
        cmd.extend(["-k", pattern])
    
    if markers:
        for marker in markers:
            cmd.extend(["-m", marker])
    
    # Coverage options
    if coverage or coverage_html or coverage_xml:
        cmd.extend(["--cov=.", "--cov-report=term-missing"])
        
        if coverage_html:
            cmd.append("--cov-report=html:htmlcov")
        
        if coverage_xml:
            cmd.append("--cov-report=xml:coverage.xml")
    
    if parallel:
        cmd.extend(["-n", "auto"])
    
    if no_header:
        cmd.append("--no-header")
    
    # Add test paths or default to project directory
    if paths:
        cmd.extend(paths)
    else:
        # Look for common test directories
        test_dirs = ["tests", "test"]
        found_tests = False
        for test_dir in test_dirs:
            if (project_dir / test_dir).exists():
                cmd.append(test_dir)
                found_tests = True
                break
        
        if not found_tests:
            cmd.append(str(project_dir))
    
    # Watch mode with pytest-watch
    if watch:
        try:
            import pytest_watch
            cmd[2] = "ptw"  # Replace pytest with ptw
            cmd = [sys.executable, "-m", "pytest_watch"] + cmd[3:]
        except ImportError:
            print("pytest-watch not installed. Install with: pip install pytest-watch")
            return 1
    
    # Run tests
    try:
        result = subprocess.run(cmd, cwd=project_dir)
        return result.returncode
    except KeyboardInterrupt:
        print("\nTest run interrupted.")
        return 130


def show_test_info(project_dir: Path) -> int:
    """
    Show test environment information.
    
    Returns:
        0 on success
    """
    import importlib.util
    
    print("\nTest Environment Information\n")
    
    # Check Python version
    print(f"Python: {sys.version}")
    print(f"Platform: {sys.platform}")
    print()
    
    # Check for pytest
    packages = {
        "pytest": "pytest",
        "pytest-cov": "pytest_cov",
        "pytest-xdist": "xdist",
        "pytest-asyncio": "pytest_asyncio",
        "pytest-watch": "pytest_watch",
        "httpx": "httpx",
    }
    
    print("Installed test packages:")
    for display_name, import_name in packages.items():
        spec = importlib.util.find_spec(import_name)
        status = "✓" if spec else "✗"
        print(f"  {status} {display_name}")
    print()
    
    # Check for test directories
    print("Test directories:")
    test_dirs = ["tests", "test"]
    found_any = False
    for test_dir in test_dirs:
        path = project_dir / test_dir
        if path.exists():
            files = list(path.rglob("test_*.py"))
            print(f"  ✓ {test_dir}/ ({len(files)} test files)")
            found_any = True
    
    if not found_any:
        print("  ✗ No test directories found")
    print()
    
    # Check for pytest.ini, pyproject.toml, setup.cfg
    print("Configuration files:")
    config_files = ["pytest.ini", "pyproject.toml", "setup.cfg", "tox.ini"]
    for config_file in config_files:
        path = project_dir / config_file
        status = "✓" if path.exists() else "✗"
        print(f"  {status} {config_file}")
    print()
    
    return 0


def collect_tests(project_dir: Path, pattern: str | None = None) -> list[str]:
    """
    Collect all test names without running them.
    
    Returns:
        List of test names
    """
    cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
    
    if pattern:
        cmd.extend(["-k", pattern])
    
    try:
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            capture_output=True,
            text=True,
        )
        
        tests = []
        for line in result.stdout.split("\n"):
            line = line.strip()
            if line and not line.startswith("=") and not line.startswith("no tests"):
                # Extract test path from output like "tests/unit/test_x.py::test_name"
                if "::" in line:
                    tests.append(line)
        
        return tests
    except Exception:
        return []

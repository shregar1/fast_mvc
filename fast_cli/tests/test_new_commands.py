"""
Tests for new CLI commands (logs, config, shell, test, db, middleware, openapi).
"""

import pytest
from click.testing import CliRunner

from fast_cli.cli import cli


class TestLogsCommand:
    """Tests for the logs command group."""

    def test_logs_help(self):
        """Test logs command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["logs", "--help"])
        assert result.exit_code == 0
        assert "View and filter application logs" in result.output
        assert "tail" in result.output
        assert "stats" in result.output

    def test_logs_tail_help(self):
        """Test logs tail command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["logs", "tail", "--help"])
        assert result.exit_code == 0
        assert "Tail and filter application logs" in result.output
        assert "--follow" in result.output
        assert "--level" in result.output

    def test_logs_stats_help(self):
        """Test logs stats command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["logs", "stats", "--help"])
        assert result.exit_code == 0
        assert "Show log file statistics" in result.output


class TestConfigCommand:
    """Tests for the config command group."""

    def test_config_help(self):
        """Test config command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "--help"])
        assert result.exit_code == 0
        assert "View and validate application configuration" in result.output
        assert "show" in result.output
        assert "validate" in result.output
        assert "diff" in result.output

    def test_config_show_help(self):
        """Test config show command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "show", "--help"])
        assert result.exit_code == 0
        assert "Display application configuration" in result.output
        assert "--format" in result.output
        assert "--show-secrets" in result.output

    def test_config_validate_help(self):
        """Test config validate command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "validate", "--help"])
        assert result.exit_code == 0
        assert "Validate configuration" in result.output

    def test_config_diff_help(self):
        """Test config diff command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "diff", "--help"])
        assert result.exit_code == 0
        assert "Compare .env with .env.example" in result.output


class TestShellCommand:
    """Tests for the shell command."""

    def test_shell_help(self):
        """Test shell command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["shell", "--help"])
        assert result.exit_code == 0
        assert "interactive shell" in result.output.lower()
        assert "--shell-type" in result.output
        assert "--no-banner" in result.output


class TestTestCommand:
    """Tests for the test command group."""

    def test_test_help(self):
        """Test test command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["test", "--help"])
        assert result.exit_code == 0
        assert "Run tests with coverage" in result.output
        assert "run" in result.output
        assert "info" in result.output

    def test_test_run_help(self):
        """Test test run command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["test", "run", "--help"])
        assert result.exit_code == 0
        assert "Run tests with pytest" in result.output
        assert "--coverage" in result.output
        assert "--coverage-html" in result.output

    def test_test_info_help(self):
        """Test test info command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["test", "info", "--help"])
        assert result.exit_code == 0
        assert "Show test environment" in result.output


class TestDbCommand:
    """Tests for the db command group."""

    def test_db_help(self):
        """Test db command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["db", "--help"])
        assert result.exit_code == 0
        assert "Database operations" in result.output
        assert "seed" in result.output
        assert "reset" in result.output
        assert "drop" in result.output
        assert "stats" in result.output

    def test_db_seed_help(self):
        """Test db seed command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["db", "seed", "--help"])
        assert result.exit_code == 0
        assert "Seed the database" in result.output
        assert "--dry-run" in result.output

    def test_db_reset_help(self):
        """Test db reset command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["db", "reset", "--help"])
        assert result.exit_code == 0
        assert "Reset database" in result.output
        assert "--force" in result.output

    def test_db_drop_help(self):
        """Test db drop command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["db", "drop", "--help"])
        assert result.exit_code == 0
        assert "Drop all database tables" in result.output

    def test_db_stats_help(self):
        """Test db stats command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["db", "stats", "--help"])
        assert result.exit_code == 0
        assert "Show database statistics" in result.output


class TestMiddlewareCommand:
    """Tests for the middleware command group."""

    def test_middleware_help(self):
        """Test middleware command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["middleware", "--help"])
        assert result.exit_code == 0
        assert "List, enable, and disable middlewares" in result.output
        assert "list" in result.output
        assert "add" in result.output
        assert "remove" in result.output

    def test_middleware_list_help(self):
        """Test middleware list command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["middleware", "list", "--help"])
        assert result.exit_code == 0
        assert "List middlewares" in result.output
        assert "--show-all" in result.output
        assert "--category" in result.output

    def test_middleware_add_help(self):
        """Test middleware add command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["middleware", "add", "--help"])
        assert result.exit_code == 0
        assert "Add a middleware" in result.output

    def test_middleware_remove_help(self):
        """Test middleware remove command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["middleware", "remove", "--help"])
        assert result.exit_code == 0
        assert "Remove/disable a middleware" in result.output


class TestOpenapiCommand:
    """Tests for the openapi command group."""

    def test_openapi_help(self):
        """Test openapi command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["openapi", "--help"])
        assert result.exit_code == 0
        assert "Export and manage OpenAPI specification" in result.output
        assert "export" in result.output

    def test_openapi_export_help(self):
        """Test openapi export command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["openapi", "export", "--help"])
        assert result.exit_code == 0
        assert "Export OpenAPI specification" in result.output
        assert "--output" in result.output


class TestInfoCommand:
    """Tests that info command shows new commands."""

    def test_info_shows_new_commands(self):
        """Test that info command lists all new commands."""
        runner = CliRunner()
        result = runner.invoke(cli, ["info"])
        assert result.exit_code == 0
        # Check that new commands are mentioned
        assert "logs" in result.output
        assert "config" in result.output
        assert "shell" in result.output
        assert "test" in result.output
        assert "db" in result.output
        assert "middleware" in result.output
        assert "openapi" in result.output

"""Tests for system utilities."""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import patch, MagicMock, mock_open

import pytest

from utilities.system import SystemUtility


class TestSystemUtility:
    """Test class for SystemUtility."""

    def test_init_default_values(self):
        """Test initialization with default values."""
        util = SystemUtility()
        assert util.urn is None
        assert util.user_urn is None

    def test_init_with_context(self):
        """Test initialization with context."""
        util = SystemUtility(urn="test", user_urn="user")
        assert util.urn == "test"
        assert util.user_urn == "user"

    def test_get_system_info(self):
        """Test getting system info."""
        info = SystemUtility.get_system_info()
        assert isinstance(info, dict)
        assert "platform" in info
        assert "python_version" in info

    def test_get_system_info_platform_value(self):
        """Test platform value in system info."""
        info = SystemUtility.get_system_info()
        assert info["platform"] == platform.system()

    def test_get_system_info_python_version(self):
        """Test python version in system info."""
        info = SystemUtility.get_system_info()
        assert sys.version.startswith(info["python_version"])

    def test_get_env_variables(self):
        """Test getting environment variables."""
        env_vars = SystemUtility.get_env_variables()
        assert isinstance(env_vars, dict)

    def test_get_env_variables_contains_path(self):
        """Test env vars contains PATH."""
        env_vars = SystemUtility.get_env_variables()
        assert "PATH" in env_vars or "Path" in env_vars

    def test_run_command_success(self):
        """Test running command successfully."""
        result = SystemUtility.run_command(["echo", "hello"])
        assert result.returncode == 0
        assert "hello" in result.stdout

    def test_run_command_failure(self):
        """Test running command that fails."""
        result = SystemUtility.run_command(["false"], check=False)
        assert result.returncode != 0

    def test_run_command_raises_on_failure_with_check(self):
        """Test running command raises on failure with check=True."""
        with pytest.raises(subprocess.CalledProcessError):
            SystemUtility.run_command(["false"], check=True)

    def test_get_current_directory(self):
        """Test getting current directory."""
        result = SystemUtility.get_current_directory()
        assert isinstance(result, str)
        assert os.path.isdir(result)

    def test_get_current_directory_matches_cwd(self):
        """Test current directory matches os.getcwd()."""
        result = SystemUtility.get_current_directory()
        assert result == os.getcwd()

    def test_file_exists_true(self, tmp_path):
        """Test file_exists returns True for existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        assert SystemUtility.file_exists(str(test_file)) is True

    def test_file_exists_false(self, tmp_path):
        """Test file_exists returns False for non-existing file."""
        non_existent = tmp_path / "nonexistent.txt"
        assert SystemUtility.file_exists(str(non_existent)) is False

    def test_directory_exists_true(self, tmp_path):
        """Test directory_exists returns True for existing directory."""
        assert SystemUtility.directory_exists(str(tmp_path)) is True

    def test_directory_exists_false(self, tmp_path):
        """Test directory_exists returns False for non-existing directory."""
        non_existent = tmp_path / "nonexistent"
        assert SystemUtility.directory_exists(str(non_existent)) is False

    def test_create_directory(self, tmp_path):
        """Test creating directory."""
        new_dir = tmp_path / "new_directory"
        SystemUtility.create_directory(str(new_dir))
        assert new_dir.exists()

    def test_create_directory_recursive(self, tmp_path):
        """Test creating directory recursively."""
        nested = tmp_path / "a" / "b" / "c"
        SystemUtility.create_directory(str(nested))
        assert nested.exists()

    def test_delete_file(self, tmp_path):
        """Test deleting file."""
        test_file = tmp_path / "to_delete.txt"
        test_file.write_text("content")
        SystemUtility.delete_file(str(test_file))
        assert not test_file.exists()

    def test_delete_file_nonexistent_raises(self, tmp_path):
        """Test deleting nonexistent file raises."""
        with pytest.raises(FileNotFoundError):
            SystemUtility.delete_file(str(tmp_path / "nonexistent.txt"))

    def test_read_file(self, tmp_path):
        """Test reading file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")
        content = SystemUtility.read_file(str(test_file))
        assert content == "hello world"

    def test_write_file(self, tmp_path):
        """Test writing file."""
        test_file = tmp_path / "test.txt"
        SystemUtility.write_file(str(test_file), "hello")
        assert test_file.read_text() == "hello"

    def test_list_files(self, tmp_path):
        """Test listing files."""
        (tmp_path / "file1.txt").write_text("1")
        (tmp_path / "file2.txt").write_text("2")
        files = SystemUtility.list_files(str(tmp_path))
        assert len(files) == 2

    def test_list_files_with_pattern(self, tmp_path):
        """Test listing files with pattern."""
        (tmp_path / "test.txt").write_text("1")
        (tmp_path / "other.py").write_text("2")
        files = SystemUtility.list_files(str(tmp_path), pattern="*.txt")
        assert len(files) == 1
        assert files[0].endswith("test.txt")

    def test_join_paths(self):
        """Test joining paths."""
        result = SystemUtility.join_paths("a", "b", "c")
        assert result == os.path.join("a", "b", "c")

    def test_get_file_extension(self):
        """Test getting file extension."""
        assert SystemUtility.get_file_extension("file.txt") == ".txt"

    def test_get_file_extension_no_extension(self):
        """Test getting file extension for file without extension."""
        assert SystemUtility.get_file_extension("Makefile") == ""

    def test_get_file_name(self):
        """Test getting file name."""
        assert SystemUtility.get_file_name("/path/to/file.txt") == "file.txt"

    def test_get_file_name_without_extension(self):
        """Test getting file name without extension."""
        assert SystemUtility.get_file_name_without_extension("file.txt") == "file"

    def test_get_directory_name(self):
        """Test getting directory name."""
        assert SystemUtility.get_directory_name("/path/to/file.txt") == "to"

    def test_is_absolute_path_true(self):
        """Test is_absolute_path returns True for absolute path."""
        assert SystemUtility.is_absolute_path("/absolute/path") is True

    def test_is_absolute_path_false(self):
        """Test is_absolute_path returns False for relative path."""
        assert SystemUtility.is_absolute_path("relative/path") is False

    def test_normalize_path(self):
        """Test normalizing path."""
        result = SystemUtility.normalize_path("a/../b/./c")
        assert ".." not in result

    def test_get_absolute_path(self):
        """Test getting absolute path."""
        result = SystemUtility.get_absolute_path(".")
        assert result.startswith("/")

    def test_get_file_size(self, tmp_path):
        """Test getting file size."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")
        size = SystemUtility.get_file_size(str(test_file))
        assert size == 5

    def test_get_file_modification_time(self, tmp_path):
        """Test getting file modification time."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        mtime = SystemUtility.get_file_modification_time(str(test_file))
        assert isinstance(mtime, float)
        assert mtime > 0

    def test_copy_file(self, tmp_path):
        """Test copying file."""
        source = tmp_path / "source.txt"
        dest = tmp_path / "dest.txt"
        source.write_text("content")
        SystemUtility.copy_file(str(source), str(dest))
        assert dest.read_text() == "content"

    def test_move_file(self, tmp_path):
        """Test moving file."""
        source = tmp_path / "source.txt"
        dest = tmp_path / "dest.txt"
        source.write_text("content")
        SystemUtility.move_file(str(source), str(dest))
        assert not source.exists()
        assert dest.read_text() == "content"

    def test_git_repository_folder_name(self):
        """Test getting git repository folder name."""
        name = SystemUtility.git_repository_folder_name()
        assert isinstance(name, str)

    def test_project_root_path(self):
        """Test getting project root path."""
        path = SystemUtility.project_root_path()
        assert isinstance(path, str)
        assert os.path.isdir(path)

    def test_absolute_path(self):
        """Test getting absolute path for relative path."""
        result = SystemUtility.absolute_path(".")
        assert os.path.isabs(result)

    def test_directory_path(self):
        """Test getting directory path."""
        result = SystemUtility.directory_path("/path/to/file.txt")
        assert result == "/path/to"


class TestSystemUtilityProperties:
    """Test properties."""

    def test_urn_property(self):
        """Test urn property."""
        util = SystemUtility()
        util.urn = "test"
        assert util.urn == "test"

    def test_user_urn_property(self):
        """Test user_urn property."""
        util = SystemUtility()
        util.user_urn = "user"
        assert util.user_urn == "user"

    def test_api_name_property(self):
        """Test api_name property."""
        util = SystemUtility()
        util.api_name = "api"
        assert util.api_name == "api"

    def test_user_id_property(self):
        """Test user_id property."""
        util = SystemUtility()
        util.user_id = "id"
        assert util.user_id == "id"


class TestSystemUtilityEdgeCases:
    """Test edge cases."""

    def test_read_file_nonexistent(self):
        """Test reading nonexistent file raises."""
        with pytest.raises(FileNotFoundError):
            SystemUtility.read_file("/nonexistent/file.txt")

    def test_write_file_to_nonexistent_directory(self, tmp_path):
        """Test writing file to nonexistent directory raises."""
        with pytest.raises(FileNotFoundError):
            SystemUtility.write_file(str(tmp_path / "nonexistent" / "file.txt"), "content")

    def test_get_file_size_nonexistent(self):
        """Test getting size of nonexistent file raises."""
        with pytest.raises(FileNotFoundError):
            SystemUtility.get_file_size("/nonexistent/file.txt")

    def test_list_files_nonexistent_directory(self):
        """Test listing nonexistent directory raises."""
        with pytest.raises(FileNotFoundError):
            SystemUtility.list_files("/nonexistent/directory")

    def test_copy_file_nonexistent_source(self, tmp_path):
        """Test copying nonexistent file raises."""
        with pytest.raises(FileNotFoundError):
            SystemUtility.copy_file(str(tmp_path / "nonexistent.txt"), str(tmp_path / "dest.txt"))

    def test_move_file_nonexistent_source(self, tmp_path):
        """Test moving nonexistent file raises."""
        with pytest.raises(FileNotFoundError):
            SystemUtility.move_file(str(tmp_path / "nonexistent.txt"), str(tmp_path / "dest.txt"))

    def test_empty_path_join(self):
        """Test joining empty paths."""
        result = SystemUtility.join_paths()
        assert result == ""

    def test_file_exists_with_directory(self, tmp_path):
        """Test file_exists with directory returns False."""
        assert SystemUtility.file_exists(str(tmp_path)) is False

    def test_directory_exists_with_file(self, tmp_path):
        """Test directory_exists with file returns False."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content")
        assert SystemUtility.directory_exists(str(test_file)) is False

"""Tests for WorkletConfig loading, saving, validation, and permissions.

Implements TEST-02: WorkletConfig unit tests.
"""
import os
import stat
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from worklet.config import WorkletConfig


class TestConfigLoading:
    """Test configuration loading from files."""

    def test_config_load_from_file(self, temp_workspace):
        """Test loading config from file verifies base_url/username/password."""
        # Create proper config file with [zentao] section as expected by code
        config_path = temp_workspace / ".worklet" / "config.toml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("""\
[zentao]
url = "https://test.example.com"
username = "testuser"
password = "testpass"

[output]
dir = "output"

[network]
connect_timeout = 30
read_timeout = 60
""")
        config = WorkletConfig.load(config_path=str(config_path))

        assert config.base_url == "https://test.example.com"
        assert config.username == "testuser"
        assert config.password == "testpass"
        # Note: output_dir is set to workspace/.worklet by load() when workspace_dir not specified

    def test_config_load_workspace_overrides_global(self, temp_workspace, monkeypatch):
        """Test workspace config takes priority over global config."""
        # Create workspace config with [zentao] section
        workspace_config = temp_workspace / ".worklet" / "config.toml"
        workspace_config.parent.mkdir(parents=True, exist_ok=True)
        workspace_config.write_text("""\
[zentao]
url = "https://workspace.example.com"
username = "workspace_user"
password = "workspace_pass"
""")

        # Create global config in a temp location
        global_dir = temp_workspace / "global"
        global_dir.mkdir()
        global_config_path = global_dir / ".worklet" / "config.toml"
        global_config_path.parent.mkdir(parents=True, exist_ok=True)
        global_config_path.write_text("""\
[zentao]
url = "https://global.example.com"
username = "global_user"
password = "global_pass"
""")

        # Mock Path.home() to return global config location
        monkeypatch.setattr(Path, "home", lambda: global_dir)

        # Load with workspace_dir specified - workspace should win
        config = WorkletConfig.load(workspace_dir=str(temp_workspace))

        assert config.base_url == "https://workspace.example.com"
        assert config.username == "workspace_user"
        assert config.password == "workspace_pass"

    def test_config_load_with_explicit_path(self, mock_config):
        """Test loading config with explicit config_path takes highest priority."""
        config = WorkletConfig.load(config_path=str(mock_config))

        assert config.get_config_source() == str(mock_config)


class TestConfigValidation:
    """Test configuration validation via is_initialized()."""

    def test_is_initialized_true(self):
        """When all required fields set, is_initialized() returns True."""
        config = WorkletConfig()
        config.base_url = "https://example.com"
        config.username = "user"
        config.password = "pass"

        assert config.is_initialized() is True

    def test_is_initialized_false(self):
        """When missing any required field, is_initialized() returns False."""
        config = WorkletConfig()

        # No fields set
        assert config.is_initialized() is False

        # Only some fields set
        config.base_url = "https://example.com"
        assert config.is_initialized() is False

        config.username = "user"
        assert config.is_initialized() is False

        # Only missing password
        config.password = None
        assert config.is_initialized() is False


class TestConfigSaving:
    """Test configuration saving to files."""

    def test_save_to_workspace(self, temp_workspace):
        """Test save creates file with correct TOML content."""
        config = WorkletConfig()
        config.base_url = "https://example.com"
        config.username = "user"
        config.password = "pass"
        config.output_dir = str(temp_workspace / "output")
        config.connect_timeout = 15
        config.read_timeout = 45

        config.save_to_workspace(str(temp_workspace))

        saved_file = temp_workspace / ".worklet" / "config.toml"
        assert saved_file.exists()

        content = saved_file.read_text()
        assert 'url = "https://example.com"' in content
        assert "username = \"user\"" in content
        assert "password = \"pass\"" in content
        assert "connect_timeout = 15" in content
        assert "read_timeout = 45" in content

    def test_save_0600_permissions(self, temp_workspace):
        """Test saved config file has 0600 permissions (owner read/write only)."""
        config = WorkletConfig()
        config.base_url = "https://example.com"
        config.username = "user"
        config.password = "pass"

        config.save_to_workspace(str(temp_workspace))

        saved_file = temp_workspace / ".worklet" / "config.toml"
        file_stat = saved_file.stat()
        file_mode = stat.S_IMODE(file_stat.st_mode)

        # 0600 = owner read + write
        assert file_mode == stat.S_IRUSR | stat.S_IWUSR

    def test_save_to_global(self, temp_workspace):
        """Test save_to_global writes to ~/.worklet/config.toml."""
        global_dir = temp_workspace / "home" / ".worklet"
        global_dir.mkdir(parents=True, exist_ok=True)

        # Mock Path.home() for this test
        with patch.object(Path, 'home', return_value=temp_workspace / "home"):
            config = WorkletConfig()
            config.base_url = "https://global.com"
            config.username = "global_user"
            config.password = "global_pass"

            config.save_to_global()

            saved_file = temp_workspace / "home" / ".worklet" / "config.toml"
            assert saved_file.exists()
            assert 'url = "https://global.com"' in saved_file.read_text()


class TestConfigSource:
    """Test config source tracking."""

    def test_get_config_source(self, temp_workspace):
        """After load, get_config_source() returns path to loaded file."""
        config_path = temp_workspace / ".worklet" / "config.toml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("""\
[zentao]
url = "https://test.example.com"
username = "testuser"
password = "testpass"
""")
        config = WorkletConfig.load(config_path=str(config_path))

        assert config.get_config_source() == str(config_path)

    def test_get_config_source_none_when_no_file(self):
        """When no config file loaded, get_config_source() returns None."""
        config = WorkletConfig()

        assert config.get_config_source() is None

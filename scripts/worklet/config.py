#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worklet - configuration management

Config priority:
1. Explicit config path (highest)
2. Workspace config: {workspace}/.worklet/config.toml
3. Global config: ~/.worklet/config.toml (lowest)

Output directory defaults to .worklet/ under current working directory (or provided workspace_dir).
"""

import os
import stat
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import tomli_w


class WorkletConfig:
    """Worklet configuration manager.

    Config priority:
    1. Explicit config path (highest)
    2. Workspace config: {workspace}/.worklet/config.toml
    3. Global config: ~/.worklet/config.toml (lowest)

    Output directory defaults to .worklet/ under current working directory (or provided workspace_dir).
    """

    WORKSPACE_CONFIG = ".worklet/config.toml"
    GLOBAL_CONFIG = "~/.worklet/config.toml"

    def __init__(self):
        self.base_url: str | None = None
        self.username: str | None = None
        self.password: str | None = None
        self.output_dir: str = os.getcwd()
        self.connect_timeout: int = 30
        self.read_timeout: int = 60
        self._config_source: str | None = None

    @classmethod
    def load(cls, workspace_dir: str | None = None, config_path: str | None = None) -> "WorkletConfig":
        """Load configuration

        Args:
            workspace_dir: workspace directory for workspace config lookup
            config_path: specified config file path (highest priority)

        Returns:
            WorkletConfig instance
        """
        config = cls()

        config_files = cls._get_config_files(workspace_dir, config_path)

        for path in config_files:
            if path and path.exists():
                config._load_from_file(path)
                config._config_source = str(path)
                break

        if workspace_dir:
            config.output_dir = str(Path(workspace_dir) / ".worklet")
        else:
            config.output_dir = str(Path.cwd() / ".worklet")

        return config

    @classmethod
    def _get_config_files(cls, workspace_dir: str | None, config_path: str | None) -> list[Path]:
        """Get config file list in priority order"""
        files = []

        if config_path:
            files.append(Path(config_path))

        if workspace_dir:
            workspace_config = Path(workspace_dir) / cls.WORKSPACE_CONFIG
            files.append(workspace_config)

        global_config = Path.home() / ".worklet" / "config.toml"
        files.append(global_config)

        return files

    def _load_from_file(self, path: Path):
        """Load config from TOML file."""
        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)

            zentao = data.get("zentao", {})
            self.base_url = zentao.get("url")
            self.username = zentao.get("username")
            self.password = zentao.get("password")

            network = data.get("network", {})
            if "connect_timeout" in network:
                self.connect_timeout = network["connect_timeout"]
            if "read_timeout" in network:
                self.read_timeout = network["read_timeout"]

            output = data.get("output", {})
            if "dir" in output:
                self.output_dir = output["dir"]

            print(f"Config loaded: {path}")
        except Exception as e:
            print(f"Failed to load config: {e}")

    def save_to_workspace(self, workspace_dir: str):
        """Save config to workspace"""
        path = Path(workspace_dir) / self.WORKSPACE_CONFIG
        self._save_to_file(path)
        print(f"Config saved to workspace: {path}")

    def save_to_global(self):
        """Save config to global location"""
        path = Path.home() / ".worklet" / "config.toml"
        self._save_to_file(path)
        print(f"Config saved to global: {path}")

    def _save_to_file(self, path: Path):
        """Save config to TOML file with 0600 permissions."""
        path.parent.mkdir(parents=True, exist_ok=True)

        data: dict = {"zentao": {}, "output": {}, "network": {}}
        if self.base_url:
            data["zentao"]["url"] = self.base_url
        if self.username:
            data["zentao"]["username"] = self.username
        if self.password:
            data["zentao"]["password"] = self.password

        data["output"]["dir"] = self.output_dir
        data["network"]["connect_timeout"] = self.connect_timeout
        data["network"]["read_timeout"] = self.read_timeout

        with open(path, "wb") as f:
            tomli_w.dump(data, f)

        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)

    def is_initialized(self) -> bool:
        """Check if config is initialized"""
        return all([self.base_url, self.username, self.password])

    def get_config_source(self) -> str | None:
        """Get config source"""
        return self._config_source

    def get_init_prompt(self) -> str:
        """Get initialization prompt"""
        if self.is_initialized():
            return None

        prompt = """Worklet configuration not initialized. Provide config via:

Option 1: Command-line arguments
  python worklet.py --url <server> --username <user> --password <pass>

Option 2: Workspace config (recommended, supports multi-project)
  Create .worklet/config.toml in your workspace root:
  [zentao]
  url = "https://your-zentao-server.com"
  username = "your_username"
  password = "your_password"

Option 3: Global config
  Create ~/.worklet/config.toml

Note: Output directory is determined dynamically each run."""
        return prompt

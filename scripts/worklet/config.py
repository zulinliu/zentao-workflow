#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worklet - configuration management

Config priority:
1. CLI arguments (highest)
2. Workspace config: {workspace}/.chandao/config.properties
3. Global config: ~/.chandao/config.properties (lowest)

Storage directory:
- Default: current workspace root
- Not persisted to config file, determined dynamically at runtime
"""

import os
from pathlib import Path


class WorkletConfig:
    """Worklet configuration manager"""

    # Config file locations
    WORKSPACE_CONFIG = ".chandao/config.properties"
    GLOBAL_CONFIG = "~/.chandao/config.properties"

    def __init__(self):
        self.base_url: str | None = None
        self.username: str | None = None
        self.password: str | None = None
        self.output_dir: str = os.getcwd()
        self.connect_timeout: int = 30000  # milliseconds
        self.read_timeout: int = 60000  # milliseconds
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

        if workspace_dir and not config.output_dir:
            config.output_dir = workspace_dir
        elif not config.output_dir:
            config.output_dir = os.getcwd()

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

        global_config = Path.home() / ".chandao" / "config.properties"
        files.append(global_config)

        return files

    def _load_from_file(self, path: Path):
        """Load config from file"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()

                        if key == "zentao.url":
                            self.base_url = value
                        elif key == "zentao.username":
                            self.username = value
                        elif key == "zentao.password":
                            self.password = value

            print(f"Loaded config: {path}")
        except Exception as e:
            print(f"Failed to load config: {e}")

    def save_to_workspace(self, workspace_dir: str):
        """Save config to workspace"""
        path = Path(workspace_dir) / self.WORKSPACE_CONFIG
        self._save_to_file(path)
        print(f"Config saved to workspace: {path}")

    def save_to_global(self):
        """Save config to global location"""
        path = Path.home() / ".chandao" / "config.properties"
        self._save_to_file(path)
        print(f"Config saved to global: {path}")

    def _save_to_file(self, path: Path):
        """Save config to specified file"""
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write("# Worklet config\n")
            f.write("# Note: output.dir is not persisted, determined at runtime\n")
            if self.base_url:
                f.write(f"zentao.url={self.base_url}\n")
            if self.username:
                f.write(f"zentao.username={self.username}\n")
            if self.password:
                f.write(f"zentao.password={self.password}\n")

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

        prompt = """Worklet config not initialized. Please provide config via one of:

Method 1: CLI arguments
  python worklet.py --url <zentao_url> --username <user> --password <pass>

Method 2: Workspace config file (recommended for multi-project)
  Create .chandao/config.properties in workspace root:
  zentao.url=https://your-zentao-server.com
  zentao.username=your_username
  zentao.password=your_password

Method 3: Global config (shared across all projects)
  Create ~/.chandao/config.properties

Note: output.dir is not persisted to config, determined at runtime."""
        return prompt

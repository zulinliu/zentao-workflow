#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - 配置管理模块
"""

import os
from pathlib import Path
from typing import Optional


class ChandaoConfig:
    """禅道配置管理"""

    DEFAULT_CONFIG_FILE = "~/.chandao/config.properties"

    def __init__(self):
        self.base_url: Optional[str] = None
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.output_dir: str = os.getcwd()
        self.connect_timeout: int = 30000  # 毫秒
        self.read_timeout: int = 60000  # 毫秒

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "ChandaoConfig":
        """加载配置文件"""
        config = cls()

        path = cls._get_config_path(config_path)
        if path and path.exists():
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
                                config.base_url = value
                            elif key == "zentao.username":
                                config.username = value
                            elif key == "zentao.password":
                                config.password = value
                            elif key == "output.dir":
                                config.output_dir = os.path.expanduser(value)

                print(f"已加载配置文件: {path}")
            except Exception as e:
                print(f"加载配置文件失败: {e}")

        # 设置默认输出目录
        if not config.output_dir:
            config.output_dir = os.getcwd()

        return config

    @staticmethod
    def _get_config_path(config_path: Optional[str]) -> Optional[Path]:
        if config_path:
            return Path(config_path)
        return Path.home().expanduser() / ".chandao" / "config.properties"

    def save(self, config_path: Optional[str] = None):
        """保存配置到文件"""
        path = self._get_config_path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write("# 禅道配置文件\n")
            if self.base_url:
                f.write(f"zentao.url={self.base_url}\n")
            if self.username:
                f.write(f"zentao.username={self.username}\n")
            if self.password:
                f.write(f"zentao.password={self.password}\n")
            if self.output_dir:
                f.write(f"output.dir={self.output_dir}\n")

        print(f"配置已保存到: {path}")

    def is_initialized(self) -> bool:
        """检查配置是否已初始化"""
        return all([self.base_url, self.username, self.password])

    def save(self, config_path: Optional[str] = None):
        """保存配置到文件"""
        path = self._get_config_path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write("# 禅道配置文件\n")
            if self.base_url:
                f.write(f"zentao.url={self.base_url}\n")
            if self.username:
                f.write(f"zentao.username={self.username}\n")
            if self.password:
                f.write(f"zentao.password={self.password}\n")
            if self.output_dir:
                f.write(f"output.dir={self.output_dir}\n")

        print(f"配置已保存到: {path}")

    def get_init_prompt(self) -> str:
        """获取初始化提示信息"""
        if self.is_initialized():
            return None

        prompt = """禅道配置未初始化！请通过以下方式之一提供配置：

方式一：命令行参数
  python chandao_fetch.py --url <禅道地址> --username <用户名> --password <密码>

方式二：配置文件
  在用户目录创建 ~/.chandao/config.properties 文件：
  zentao.url=https://your-zentao-server.com
  zentao.username=your_username
  zentao.password=your_password

首次配置后，配置将自动保存到 ~/.chandao/config.properties"""
        return prompt

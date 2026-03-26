#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - 配置管理模块

配置优先级：
1. 命令行参数（最高）
2. 工作区配置：{工作区}/.chandao/config.properties
3. 全局配置：~/.chandao/config.properties（最低）

存储目录：
- 默认使用当前工作区根目录
- 不持久化到配置文件，每次运行时动态确定
"""

import os
from pathlib import Path
from typing import Optional, List


class ChandaoConfig:
    """禅道配置管理"""

    # 配置文件位置
    WORKSPACE_CONFIG = ".chandao/config.properties"
    GLOBAL_CONFIG = "~/.chandao/config.properties"

    def __init__(self):
        self.base_url: Optional[str] = None
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.output_dir: str = os.getcwd()  # 默认当前目录
        self.connect_timeout: int = 30000  # 毫秒
        self.read_timeout: int = 60000  # 毫秒
        self._config_source: Optional[str] = None  # 记录配置来源

    @classmethod
    def load(cls, workspace_dir: Optional[str] = None, config_path: Optional[str] = None) -> "ChandaoConfig":
        """加载配置文件

        Args:
            workspace_dir: 工作区目录，用于查找工作区配置文件
            config_path: 指定的配置文件路径（最高优先级）

        Returns:
            ChandaoConfig 实例
        """
        config = cls()

        # 按优先级加载配置
        config_files = cls._get_config_files(workspace_dir, config_path)

        for path in config_files:
            if path and path.exists():
                config._load_from_file(path)
                config._config_source = str(path)
                break

        # 设置默认输出目录为工作区目录
        if workspace_dir and not config.output_dir:
            config.output_dir = workspace_dir
        elif not config.output_dir:
            config.output_dir = os.getcwd()

        return config

    @classmethod
    def _get_config_files(cls, workspace_dir: Optional[str], config_path: Optional[str]) -> List[Path]:
        """获取配置文件列表，按优先级排序"""
        files = []

        # 1. 指定的配置文件（最高优先级）
        if config_path:
            files.append(Path(config_path))

        # 2. 工作区配置文件
        if workspace_dir:
            workspace_config = Path(workspace_dir) / cls.WORKSPACE_CONFIG
            files.append(workspace_config)

        # 3. 全局配置文件（最低优先级）
        global_config = Path.home() / ".chandao" / "config.properties"
        files.append(global_config)

        return files

    def _load_from_file(self, path: Path):
        """从文件加载配置"""
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
                        # 注意：output.dir 不从配置文件加载，每次运行时动态确定

            print(f"已加载配置文件: {path}")
        except Exception as e:
            print(f"加载配置文件失败: {e}")

    def save_to_workspace(self, workspace_dir: str):
        """保存配置到工作区"""
        path = Path(workspace_dir) / self.WORKSPACE_CONFIG
        self._save_to_file(path)
        print(f"配置已保存到工作区: {path}")

    def save_to_global(self):
        """保存配置到全局位置"""
        path = Path.home() / ".chandao" / "config.properties"
        self._save_to_file(path)
        print(f"配置已保存到全局: {path}")

    def _save_to_file(self, path: Path):
        """保存配置到指定文件"""
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write("# 禅道配置文件\n")
            f.write("# 说明：存储目录(output.dir)不保存到配置文件，每次运行时动态确定\n")
            if self.base_url:
                f.write(f"zentao.url={self.base_url}\n")
            if self.username:
                f.write(f"zentao.username={self.username}\n")
            if self.password:
                f.write(f"zentao.password={self.password}\n")

    def is_initialized(self) -> bool:
        """检查配置是否已初始化"""
        return all([self.base_url, self.username, self.password])

    def get_config_source(self) -> Optional[str]:
        """获取配置来源"""
        return self._config_source

    def get_init_prompt(self) -> str:
        """获取初始化提示信息"""
        if self.is_initialized():
            return None

        prompt = """禅道配置未初始化！请通过以下方式之一提供配置：

方式一：命令行参数
  python chandao_fetch.py --url <禅道地址> --username <用户名> --password <密码>

方式二：工作区配置文件（推荐，支持多项目）
  在工作区根目录创建 .chandao/config.properties 文件：
  zentao.url=https://your-zentao-server.com
  zentao.username=your_username
  zentao.password=your_password

方式三：全局配置文件（所有项目共享）
  在用户目录创建 ~/.chandao/config.properties 文件

注意：存储目录不保存到配置文件，每次运行时动态确定。"""
        return prompt

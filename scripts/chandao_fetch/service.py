#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - 服务层
"""

import os
import re
from pathlib import Path
from typing import List, Optional

from .client import ChandaoClient
from .config import ChandaoConfig
from .exporter import MarkdownExporter
from .models import Attachment, Bug, Story, Task


class ChandaoService:
    """禅道服务主类"""

    def __init__(self, config: ChandaoConfig):
        self.config = config
        self.client = ChandaoClient(config)
        self.exporter = MarkdownExporter(config.output_dir)

    def execute(self, content_type: str, ids: List[int], download_attachments: bool = True):
        """执行下载任务"""
        # 登录
        if not self.client.login():
            raise Exception("登录失败")

        # 下载每个ID的内容
        for item_id in ids:
            self._fetch_by_id(content_type, item_id, download_attachments)

    def _fetch_by_id(self, content_type: str, item_id: int, download_attachments: bool):
        """根据类型和ID获取内容"""
        content_type = content_type.lower()

        if content_type == "story":
            story = self.client.get_story(item_id)
            attach_dir = Path(self.config.output_dir) / "attachments" / "story" / str(item_id)
            if download_attachments:
                if story.attachments:
                    self._download_attachments(story.attachments, attach_dir)
                # 下载内容中的图片
                story.spec = self._download_content_images(story.spec, attach_dir)
                story.verify = self._download_content_images(story.verify, attach_dir)
            self.exporter.export_story(story)

        elif content_type == "task":
            task = self.client.get_task(item_id)
            attach_dir = Path(self.config.output_dir) / "attachments" / "task" / str(item_id)
            if download_attachments:
                if task.attachments:
                    self._download_attachments(task.attachments, attach_dir)
                # 下载内容中的图片
                task.desc = self._download_content_images(task.desc, attach_dir)
            self.exporter.export_task(task)

        elif content_type == "bug":
            bug = self.client.get_bug(item_id)
            attach_dir = Path(self.config.output_dir) / "attachments" / "bug" / str(item_id)
            if download_attachments:
                if bug.attachments:
                    self._download_attachments(bug.attachments, attach_dir)
                # 下载内容中的图片
                bug.steps = self._download_content_images(bug.steps, attach_dir)
            self.exporter.export_bug(bug)

        else:
            raise Exception(f"未知类型: {content_type}")

    def _download_attachments(self, attachments: List[Attachment], attach_dir: Path):
        """下载附件"""
        attach_dir.mkdir(parents=True, exist_ok=True)

        for att in attachments:
            try:
                content = self.client.download_attachment(att.id)
                file_path = attach_dir / att.file_name

                with open(file_path, "wb") as f:
                    f.write(content)

                att.local_path = str(file_path)
                print(f"下载附件: {att.file_name} -> {file_path}")

            except Exception as e:
                print(f"下载附件失败: {att.id} - {att.title}: {e}")

    def _download_content_images(self, content: Optional[str], attach_dir: Path) -> Optional[str]:
        """下载内容中的图片

        只下载图片，不修改内容。图片路径的转换由exporter处理。

        Args:
            content: 原始内容（可能包含<img>标签）
            attach_dir: 附件保存目录

        Returns:
            原始内容（不变）
        """
        if not content:
            return content

        attach_dir.mkdir(parents=True, exist_ok=True)

        # 匹配 <img src="xxx" /> 标签
        pattern = r'<img[^>]+src="([^"]+)"[^>]*>'

        def download_image(match):
            src = match.group(1)
            try:
                # 提取文件名
                filename = src.split("/")[-1]
                if not filename:
                    return

                # 检查文件是否已存在
                file_path = attach_dir / filename
                if file_path.exists():
                    return

                # 下载图片
                image_content = self.client.download_image(src)

                with open(file_path, "wb") as f:
                    f.write(image_content)

                print(f"下载图片: {filename} -> {file_path}")

            except Exception as e:
                print(f"下载图片失败: {src}: {e}")

        # 下载所有图片，但不修改内容
        re.findall(pattern, content)  # 预编译检查
        for match in re.finditer(pattern, content):
            download_image(match)

        return content  # 返回原始内容

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worklet - Markdown export module
"""

import hashlib
import os
import re
from pathlib import Path

import markdownify

from .models import Attachment, Bug, Story, Task, Worklet


class WorkletConverter(markdownify.MarkdownConverter):
    """Custom markdownify converter for Worklet export.

    Handles img tags with attachment path context.
    """

    def __init__(self, attach_path: str = '', **kwargs):
        super().__init__(**kwargs)
        self.attach_path = attach_path

    def convert_img(self, el, text, **kwargs):
        """Convert img tag to Markdown with attachment path."""
        src = el.get('src', '')
        alt = el.get('alt', '')
        # Transform to relative attachment path
        if src and not src.startswith(('http://', 'https://', '/')):
            filename = src.split("/")[-1]
            return f'![{alt}]({self.attach_path}/{filename})'
        elif src.startswith(('http://', 'https://')):
            return f'![{alt}]({src})'
        return f'![{alt}]({src})'


class MarkdownExporter:
    """Markdown export service"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

    def export_story(self, story: Story) -> Path:
        """Export story"""
        safe_title = self._sanitize_filename(story.title)
        filename = f"{story.id}-{safe_title}"
        attach_path = f"../attachments/story/{story.id}"

        md = []
        md.append(f"# [{story.title}]{story.id}")
        md.append("")
        md.append("> 类型: 需求")
        md.append("")

        md.append("## 基本信息")
        md.append("")
        md.append("| 字段 | 值 |")
        md.append("|------|----|")
        md.append(f"| 状态 | {self._safe(story.status)} |")
        md.append(f"| 阶段 | {self._safe(story.stage)} |")
        md.append(f"| 优先级 | {self._safe(story.pri)} |")
        md.append(f"| 来源 | {self._safe(story.source)} |")
        md.append(f"| 分类 | {self._safe(story.category)} |")
        if story.product_name:
            md.append(f"| 产品 | {story.product_name} |")
        if story.project_name:
            md.append(f"| 项目 | {story.project_name} |")
        md.append(f"| 创建人 | {self._safe(story.opened_by)} |")
        md.append(f"| 创建时间 | {self._safe(story.opened_date)} |")
        md.append(f"| 指派给 | {self._safe(story.assigned_to)} |")
        md.append("")

        if story.spec:
            md.append("## 需求描述")
            md.append("")
            md.append(self._process_content(story.spec, attach_path))
            md.append("")

        if story.verify:
            md.append("## 验收标准")
            md.append("")
            md.append(self._process_content(story.verify, attach_path))
            md.append("")

        self._append_attachments(md, story.attachments, attach_path)

        file_path = self.output_dir / "story" / f"{filename}.md"
        self._write_file(file_path, "\n".join(md))

        print(f"Exported story: {file_path}")
        return file_path

    def export_task(self, task: Task) -> Path:
        """Export task"""
        safe_name = self._sanitize_filename(task.name)
        filename = f"{task.id}-{safe_name}"
        attach_path = f"../attachments/task/{task.id}"

        md = []
        md.append(f"# [{task.name}]{task.id}")
        md.append("")
        md.append("> 类型: 任务")
        md.append("")

        md.append("## 基本信息")
        md.append("")
        md.append("| 字段 | 值 |")
        md.append("|------|----|")
        md.append(f"| 状态 | {self._safe(task.status)} |")
        md.append(f"| 类型 | {self._safe(task.type)} |")
        md.append(f"| 优先级 | {self._safe(task.pri)} |")
        if task.project_name:
            md.append(f"| 项目 | {task.project_name} |")
        if task.story_title:
            md.append(f"| 相关需求 | {task.story_title} |")
        md.append(f"| 创建人 | {self._safe(task.opened_by)} |")
        md.append(f"| 创建时间 | {self._safe(task.opened_date)} |")
        md.append(f"| 指派给 | {self._safe(task.assigned_to)} |")
        if task.deadline:
            md.append(f"| 截止日期 | {task.deadline} |")
        if task.estimate:
            md.append(f"| 预计工时 | {task.estimate}h |")
        if task.consumed:
            md.append(f"| 已消耗 | {task.consumed}h |")
        md.append("")

        if task.desc:
            md.append("## 任务描述")
            md.append("")
            md.append(self._process_content(task.desc, attach_path))
            md.append("")

        self._append_attachments(md, task.attachments, attach_path)

        file_path = self.output_dir / "task" / f"{filename}.md"
        self._write_file(file_path, "\n".join(md))

        print(f"Exported task: {file_path}")
        return file_path

    def export_bug(self, bug: Bug) -> Path:
        """Export bug"""
        safe_title = self._sanitize_filename(bug.title)
        filename = f"{bug.id}-{safe_title}"
        attach_path = f"../attachments/bug/{bug.id}"

        md = []
        md.append(f"# [{bug.title}]{bug.id}")
        md.append("")
        md.append("> 类型: Bug")
        md.append("")

        md.append("## 基本信息")
        md.append("")
        md.append("| 字段 | 值 |")
        md.append("|------|----|")
        md.append(f"| 状态 | {self._safe(bug.status)} |")
        md.append(f"| 严重程度 | {self._safe(bug.severity)} |")
        md.append(f"| 优先级 | {self._safe(bug.pri)} |")
        md.append(f"| 类型 | {self._safe(bug.type)} |")
        if bug.product_name:
            md.append(f"| 产品 | {bug.product_name} |")
        if bug.project_name:
            md.append(f"| 项目 | {bug.project_name} |")
        md.append(f"| 创建人 | {self._safe(bug.opened_by)} |")
        md.append(f"| 创建时间 | {self._safe(bug.opened_date)} |")
        md.append(f"| 指派给 | {self._safe(bug.assigned_to)} |")
        if bug.resolved_by:
            md.append(f"| 解决人 | {bug.resolved_by} |")
            md.append(f"| 解决时间 | {self._safe(bug.resolved_date)} |")
            md.append(f"| 解决方案 | {self._safe(bug.resolution)} |")
        md.append("")

        if bug.steps:
            md.append("## 重现步骤")
            md.append("")
            md.append(self._process_content(bug.steps, attach_path))
            md.append("")

        self._append_attachments(md, bug.attachments, attach_path)

        file_path = self.output_dir / "bug" / f"{filename}.md"
        self._write_file(file_path, "\n".join(md))

        print(f"Exported bug: {file_path}")
        return file_path

    def _process_content(self, content: str, attach_path: str) -> str:
        """Process content: convert HTML to Markdown

        Args:
            content: Original content (may contain HTML tags)
            attach_path: Attachment relative path (e.g., ../attachments/bug/66445)
        """
        if not content:
            return ""

        result = content

        result = self._convert_img_tags(result, attach_path)

        result = self._html_to_markdown(result)

        result = re.sub(r'\n{3,}', '\n\n', result).strip()

        return result

    def _convert_img_tags(self, content: str, attach_path: str) -> str:
        """Convert img tags to Markdown format.

        Deprecated: Use _html_to_markdown with WorkletConverter instead.
        This method kept for backward compatibility with existing code paths.
        """
        if not content:
            return ""

        # Delegate to markdownify-based approach
        result = self._html_to_markdown(content, attach_path)
        return result

    def _html_to_markdown(self, html: str, attach_path: str = '') -> str:
        """Convert HTML to Markdown using markdownify.

        Per D-04: Use markdownify>=0.18.0 instead of 40+ regex replacements.

        Args:
            html: HTML content
            attach_path: Attachment relative path for img tag transformation

        Returns:
            Markdown-formatted string
        """
        if not html:
            return ""

        # Use custom converter for img tag handling
        converter = WorkletConverter(attach_path=attach_path)
        result = converter.convert(html)

        # Post-process: normalize excessive newlines
        result = re.sub(r'\n{3,}', '\n\n', result).strip()

        return result

    def _append_attachments(self, md: list[str], attachments: list[Attachment] | None, attach_path: str):
        """Append attachment list

        Args:
            md: Markdown content list
            attachments: Attachment list
            attach_path: Attachment relative path
        """
        if not attachments:
            return

        md.append("## 附件")
        md.append("")

        for att in attachments:
            if att.is_image():
                md.append(f"![{att.file_name}]({attach_path}/{att.file_name})")
                md.append("")
            else:
                md.append(f"- [{att.file_name}]({attach_path}/{att.file_name})")

        md.append("")

    def _sanitize_filename(self, name: str | None, max_length: int = 50) -> str:
        """Sanitize filename and ensure uniqueness via hashing.

        Per EXPORT-02: Use hash instead of simple truncation to avoid collisions.

        Args:
            name: Original name
            max_length: Maximum length before hash suffix

        Returns:
            Sanitized filename with hash suffix if needed
        """
        if not name:
            return "unnamed"

        # Remove illegal characters
        sanitized = re.sub(r'[\\/:*?"<>|]', "_", name)
        sanitized = sanitized.strip()

        # If within limit, return as-is
        if len(sanitized) <= max_length:
            return sanitized

        # Truncate and append short hash of full name for uniqueness
        # Use MD5 hash of original name (first 8 hex chars = 32 bits)
        hash_suffix = hashlib.md5(name.encode('utf-8')).hexdigest()[:8]

        # Truncate to make room for hash: max_length - 1 (underscore) - 8 (hash)
        truncated = sanitized[:max_length - 9]
        return f"{truncated}_{hash_suffix}"

    def _to_worklet(self, item: Story | Task | Bug) -> Worklet:
        """Convert Story/Task/Bug to unified Worklet model.

        Per D-01: Exporter 内部兼容 Story/Task/Bug → Worklet 转换
        This enables Exporter to work with unified Worklet model internally.

        Args:
            item: Story, Task, or Bug instance

        Returns:
            Normalized Worklet instance
        """
        # Determine source type and extract content/title
        if isinstance(item, Story):
            title = item.title or ''
            content = item.spec or ''
            source_type = 'zentao-story'
            item_id = f"story-{item.id}" if item.id else ''
        elif isinstance(item, Task):
            title = item.name or ''
            content = item.desc or ''
            source_type = 'zentao-task'
            item_id = f"task-{item.id}" if item.id else ''
        elif isinstance(item, Bug):
            title = item.title or ''
            content = item.steps or ''
            source_type = 'zentao-bug'
            item_id = f"bug-{item.id}" if item.id else ''
        else:
            raise ValueError(f"Unknown item type: {type(item)}")

        # Build metadata
        metadata = {}
        if item.parent:
            metadata['parent'] = item.parent
        if hasattr(item, 'metadata') and item.metadata:
            metadata.update(item.metadata)

        return Worklet(
            id=item_id,
            title=title,
            content=content,
            source_type=source_type,
            attachments=list(item.attachments) if item.attachments else [],
            metadata=metadata,
        )

    def export_worklet(self, item: Story | Task | Bug) -> Path:
        """Export unified Worklet model.

        Converts Story/Task/Bug to Worklet internally, then exports.

        Args:
            item: Story, Task, or Bug instance

        Returns:
            Path to exported Markdown file
        """
        # Convert to unified Worklet model
        worklet = self._to_worklet(item)

        # Use generic export path based on source_type
        safe_title = self._sanitize_filename(worklet.title)
        filename = f"{worklet.id}-{safe_title}"
        attach_path = f"../attachments/{worklet.source_type}/{worklet.id}"

        md = []
        md.append(f"# [{worklet.title}]")
        md.append("")
        md.append(f"> Source: {worklet.source_type}")
        md.append("")
        md.append("## Content")
        md.append("")
        md.append(self._process_content(worklet.content, attach_path))
        md.append("")

        if worklet.attachments:
            self._append_attachments(md, worklet.attachments, attach_path)

        file_path = self.output_dir / worklet.source_type / f"{filename}.md"
        self._write_file(file_path, "\n".join(md))

        print(f"Exported Worklet: {file_path}")
        return file_path

    def _safe(self, value: str | None) -> str:
        """Safely get string value"""
        return value if value else "-"

    def _write_file(self, path: Path, content: str):
        """Write file"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

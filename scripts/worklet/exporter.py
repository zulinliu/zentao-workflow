#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worklet - Markdown export module
"""

import os
import re
from pathlib import Path

from .models import Attachment, Bug, Story, Task


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
        """Convert img tags to Markdown format"""
        if not content:
            return ""

        pattern = r'<img[^>]+src="([^"]+)"[^>]*>'

        def replace_img(match):
            src = match.group(1)
            filename = src.split("/")[-1]
            return f"\n\n![]({attach_path}/{filename})\n\n"

        return re.sub(pattern, replace_img, content)

    def _html_to_markdown(self, html: str) -> str:
        """Convert HTML to Markdown"""
        if not html:
            return ""

        result = html

        result = re.sub(r'<h1[^>]*>\s*', '\n\n# ', result, flags=re.IGNORECASE)
        result = re.sub(r'<h2[^>]*>\s*', '\n\n## ', result, flags=re.IGNORECASE)
        result = re.sub(r'<h3[^>]*>\s*', '\n\n### ', result, flags=re.IGNORECASE)
        result = re.sub(r'<h4[^>]*>\s*', '\n\n#### ', result, flags=re.IGNORECASE)
        result = re.sub(r'<h5[^>]*>\s*', '\n\n##### ', result, flags=re.IGNORECASE)
        result = re.sub(r'<h6[^>]*>\s*', '\n\n###### ', result, flags=re.IGNORECASE)
        result = re.sub(r'</h[1-6]>', '\n\n', result, flags=re.IGNORECASE)

        result = re.sub(r'<p[^>]*>\s*', '\n\n', result, flags=re.IGNORECASE)
        result = re.sub(r'</p>', '\n\n', result, flags=re.IGNORECASE)

        result = re.sub(r'<br\s*/?>\s*', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'<br[^>]*>', '\n', result, flags=re.IGNORECASE)

        result = re.sub(r'<ul[^>]*>\s*', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'</ul>', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'<ol[^>]*>\s*', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'</ol>', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'<li[^>]*>\s*', '- ', result, flags=re.IGNORECASE)
        result = re.sub(r'</li>', '\n', result, flags=re.IGNORECASE)

        result = re.sub(r'<strong[^>]*>', '**', result, flags=re.IGNORECASE)
        result = re.sub(r'</strong>', '**', result, flags=re.IGNORECASE)
        result = re.sub(r'<b[^>]*>', '**', result, flags=re.IGNORECASE)
        result = re.sub(r'</b>', '**', result, flags=re.IGNORECASE)
        result = re.sub(r'<em[^>]*>', '*', result, flags=re.IGNORECASE)
        result = re.sub(r'</em>', '*', result, flags=re.IGNORECASE)
        result = re.sub(r'<i[^>]*>', '*', result, flags=re.IGNORECASE)
        result = re.sub(r'</i>', '*', result, flags=re.IGNORECASE)

        result = re.sub(r'<code[^>]*>', '`', result, flags=re.IGNORECASE)
        result = re.sub(r'</code>', '`', result, flags=re.IGNORECASE)
        result = re.sub(r'<pre[^>]*>\s*', '\n\n```\n', result, flags=re.IGNORECASE)
        result = re.sub(r'</pre>', '\n```\n', result, flags=re.IGNORECASE)

        result = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', r'[\2](\1)', result, flags=re.IGNORECASE)

        result = re.sub(r'<table[^>]*>\s*', '\n\n', result, flags=re.IGNORECASE)
        result = re.sub(r'</table>', '\n\n', result, flags=re.IGNORECASE)
        result = re.sub(r'<tr[^>]*>\s*', '| ', result, flags=re.IGNORECASE)
        result = re.sub(r'</tr>', ' |\n', result, flags=re.IGNORECASE)
        result = re.sub(r'<td[^>]*>\s*', ' ', result, flags=re.IGNORECASE)
        result = re.sub(r'</td>', ' |', result, flags=re.IGNORECASE)
        result = re.sub(r'<th[^>]*>\s*', ' ', result, flags=re.IGNORECASE)
        result = re.sub(r'</th>', ' |', result, flags=re.IGNORECASE)
        result = re.sub(r'<thead[^>]*>\s*', '', result, flags=re.IGNORECASE)
        result = re.sub(r'</thead>', '', result, flags=re.IGNORECASE)
        result = re.sub(r'<tbody[^>]*>\s*', '', result, flags=re.IGNORECASE)
        result = re.sub(r'</tbody>', '', result, flags=re.IGNORECASE)

        result = re.sub(r'<span[^>]*>', '', result, flags=re.IGNORECASE)
        result = re.sub(r'</span>', '', result, flags=re.IGNORECASE)
        result = re.sub(r'<div[^>]*>\s*', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'</div>', '\n', result, flags=re.IGNORECASE)

        result = re.sub(r'<[^>]+>', '', result)

        result = result.replace('&nbsp;', ' ')
        result = result.replace('&lt;', '<')
        result = result.replace('&gt;', '>')
        result = result.replace('&amp;', '&')
        result = result.replace('&quot;', '"')
        result = result.replace('&#39;', "'")

        result = re.sub(r'\n{3,}', '\n\n', result)
        result = result.strip()

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

    def _sanitize_filename(self, name: str | None) -> str:
        """Sanitize filename, remove illegal characters"""
        if not name:
            return "unnamed"

        sanitized = re.sub(r'[\\/:*?"<>|]', "_", name)

        if len(sanitized) > 50:
            sanitized = sanitized[:50]

        return sanitized.strip()

    def _safe(self, value: str | None) -> str:
        """Safely get string value"""
        return value if value else "-"

    def _write_file(self, path: Path, content: str):
        """Write file"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

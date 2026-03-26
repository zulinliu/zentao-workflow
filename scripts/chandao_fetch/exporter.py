#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - Markdown导出模块
"""

import os
import re
from pathlib import Path
from typing import List, Optional

from .models import Attachment, Bug, Story, Task


class MarkdownExporter:
    """Markdown导出服务"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

    def export_story(self, story: Story) -> Path:
        """导出需求"""
        safe_title = self._sanitize_filename(story.title)
        filename = f"{story.id}-{safe_title}"
        attach_path = f"../attachments/story/{story.id}"

        md = []
        md.append(f"# 【{story.title}】{story.id}")
        md.append("")
        md.append("> 类型: 需求")
        md.append("")

        # 基本信息
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

        # 需求描述
        if story.spec:
            md.append("## 需求描述")
            md.append("")
            md.append(self._process_content(story.spec, attach_path))
            md.append("")

        # 验收标准
        if story.verify:
            md.append("## 验收标准")
            md.append("")
            md.append(self._process_content(story.verify, attach_path))
            md.append("")

        # 附件
        self._append_attachments(md, story.attachments, attach_path)

        # 写入文件
        file_path = self.output_dir / "story" / f"{filename}.md"
        self._write_file(file_path, "\n".join(md))

        print(f"导出需求: {file_path}")
        return file_path

    def export_task(self, task: Task) -> Path:
        """导出任务"""
        safe_name = self._sanitize_filename(task.name)
        filename = f"{task.id}-{safe_name}"
        attach_path = f"../attachments/task/{task.id}"

        md = []
        md.append(f"# 【{task.name}】{task.id}")
        md.append("")
        md.append("> 类型: 任务")
        md.append("")

        # 基本信息
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

        # 任务描述
        if task.desc:
            md.append("## 任务描述")
            md.append("")
            md.append(self._process_content(task.desc, attach_path))
            md.append("")

        # 附件
        self._append_attachments(md, task.attachments, attach_path)

        # 写入文件
        file_path = self.output_dir / "task" / f"{filename}.md"
        self._write_file(file_path, "\n".join(md))

        print(f"导出任务: {file_path}")
        return file_path

    def export_bug(self, bug: Bug) -> Path:
        """导出Bug"""
        safe_title = self._sanitize_filename(bug.title)
        filename = f"{bug.id}-{safe_title}"
        attach_path = f"../attachments/bug/{bug.id}"

        md = []
        md.append(f"# 【{bug.title}】{bug.id}")
        md.append("")
        md.append("> 类型: Bug")
        md.append("")

        # 基本信息
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

        # 重现步骤
        if bug.steps:
            md.append("## 重现步骤")
            md.append("")
            md.append(self._process_content(bug.steps, attach_path))
            md.append("")

        # 附件
        self._append_attachments(md, bug.attachments, attach_path)

        # 写入文件
        file_path = self.output_dir / "bug" / f"{filename}.md"
        self._write_file(file_path, "\n".join(md))

        print(f"导出Bug: {file_path}")
        return file_path

    def _process_content(self, content: str, attach_path: str) -> str:
        """处理内容：将 HTML 转换为 Markdown

        Args:
            content: 原始内容（可能包含 HTML 标签）
            attach_path: 附件相对路径 (如 ../attachments/bug/66445)
        """
        if not content:
            return ""

        result = content

        # 1. 先处理图片标签（在 HTML 转换之前）
        result = self._convert_img_tags(result, attach_path)

        # 2. HTML 转 Markdown
        result = self._html_to_markdown(result)

        # 3. 清理多余的空行
        result = re.sub(r'\n{3,}', '\n\n', result).strip()

        return result

    def _convert_img_tags(self, content: str, attach_path: str) -> str:
        """转换图片标签为 Markdown 格式"""
        if not content:
            return ""

        pattern = r'<img[^>]+src="([^"]+)"[^>]*>'

        def replace_img(match):
            src = match.group(1)
            filename = src.split("/")[-1]
            return f"\n\n![]({attach_path}/{filename})\n\n"

        return re.sub(pattern, replace_img, content)

    def _html_to_markdown(self, html: str) -> str:
        """将 HTML 转换为 Markdown"""
        if not html:
            return ""

        result = html

        # 标题转换 (h1-h6)
        result = re.sub(r'<h1[^>]*>\s*', '\n\n# ', result, flags=re.IGNORECASE)
        result = re.sub(r'<h2[^>]*>\s*', '\n\n## ', result, flags=re.IGNORECASE)
        result = re.sub(r'<h3[^>]*>\s*', '\n\n### ', result, flags=re.IGNORECASE)
        result = re.sub(r'<h4[^>]*>\s*', '\n\n#### ', result, flags=re.IGNORECASE)
        result = re.sub(r'<h5[^>]*>\s*', '\n\n##### ', result, flags=re.IGNORECASE)
        result = re.sub(r'<h6[^>]*>\s*', '\n\n###### ', result, flags=re.IGNORECASE)
        result = re.sub(r'</h[1-6]>', '\n\n', result, flags=re.IGNORECASE)

        # 段落
        result = re.sub(r'<p[^>]*>\s*', '\n\n', result, flags=re.IGNORECASE)
        result = re.sub(r'</p>', '\n\n', result, flags=re.IGNORECASE)

        # 换行
        result = re.sub(r'<br\s*/?>\s*', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'<br[^>]*>', '\n', result, flags=re.IGNORECASE)

        # 列表
        result = re.sub(r'<ul[^>]*>\s*', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'</ul>', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'<ol[^>]*>\s*', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'</ol>', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'<li[^>]*>\s*', '- ', result, flags=re.IGNORECASE)
        result = re.sub(r'</li>', '\n', result, flags=re.IGNORECASE)

        # 强调
        result = re.sub(r'<strong[^>]*>', '**', result, flags=re.IGNORECASE)
        result = re.sub(r'</strong>', '**', result, flags=re.IGNORECASE)
        result = re.sub(r'<b[^>]*>', '**', result, flags=re.IGNORECASE)
        result = re.sub(r'</b>', '**', result, flags=re.IGNORECASE)
        result = re.sub(r'<em[^>]*>', '*', result, flags=re.IGNORECASE)
        result = re.sub(r'</em>', '*', result, flags=re.IGNORECASE)
        result = re.sub(r'<i[^>]*>', '*', result, flags=re.IGNORECASE)
        result = re.sub(r'</i>', '*', result, flags=re.IGNORECASE)

        # 代码
        result = re.sub(r'<code[^>]*>', '`', result, flags=re.IGNORECASE)
        result = re.sub(r'</code>', '`', result, flags=re.IGNORECASE)
        result = re.sub(r'<pre[^>]*>\s*', '\n\n```\n', result, flags=re.IGNORECASE)
        result = re.sub(r'</pre>', '\n```\n', result, flags=re.IGNORECASE)

        # 链接 <a href="url">text</a> -> [text](url)
        result = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', r'[\2](\1)', result, flags=re.IGNORECASE)

        # 表格（简单处理）
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

        # Span 和 div（移除标签，保留内容）
        result = re.sub(r'<span[^>]*>', '', result, flags=re.IGNORECASE)
        result = re.sub(r'</span>', '', result, flags=re.IGNORECASE)
        result = re.sub(r'<div[^>]*>\s*', '\n', result, flags=re.IGNORECASE)
        result = re.sub(r'</div>', '\n', result, flags=re.IGNORECASE)

        # 移除其他未知标签，保留内容
        result = re.sub(r'<[^>]+>', '', result)

        # 处理 HTML 实体
        result = result.replace('&nbsp;', ' ')
        result = result.replace('&lt;', '<')
        result = result.replace('&gt;', '>')
        result = result.replace('&amp;', '&')
        result = result.replace('&quot;', '"')
        result = result.replace('&#39;', "'")

        # 清理多余空行
        result = re.sub(r'\n{3,}', '\n\n', result)
        result = result.strip()

        return result

    def _append_attachments(self, md: List[str], attachments: Optional[List[Attachment]], attach_path: str):
        """添加附件列表

        Args:
            md: Markdown内容列表
            attachments: 附件列表
            attach_path: 附件相对路径 (如 ../attachments/bug/66445)
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

    def _sanitize_filename(self, name: Optional[str]) -> str:
        """清理文件名，移除非法字符"""
        if not name:
            return "unnamed"

        # 移除Windows和Linux不允许的文件名字符
        sanitized = re.sub(r'[\\/:*?"<>|]', "_", name)

        # 限制长度，保留前50个字符
        if len(sanitized) > 50:
            sanitized = sanitized[:50]

        return sanitized.strip()

    def _safe(self, value: Optional[str]) -> str:
        """安全获取字符串值"""
        return value if value else "-"

    def _write_file(self, path: Path, content: str):
        """写入文件"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

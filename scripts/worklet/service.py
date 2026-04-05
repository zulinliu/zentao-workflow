#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worklet - service layer
"""

import os
import re
from pathlib import Path
from urllib.parse import urljoin

from .client import WorkletClient
from .config import WorkletConfig
from .exporter import MarkdownExporter
from .models import Attachment, Bug, Story, Task


class WorkletService:
    """Worklet service"""

    def __init__(self, config: WorkletConfig):
        self.config = config
        self.client = WorkletClient(config)
        self.exporter = MarkdownExporter(config.output_dir)

    def execute(self, content_type: str, ids: list[int], download_attachments: bool = True):
        """Execute download task"""
        if not self.client.login():
            raise Exception("Login failed")

        for item_id in ids:
            self._fetch_by_id(content_type, item_id, download_attachments)

    def _fetch_by_id(self, content_type: str, item_id: int, download_attachments: bool):
        """Fetch content by type and ID"""
        content_type = content_type.lower()

        if content_type == "story":
            story = self.client.get_story(item_id)
            attach_dir = Path(self.config.output_dir) / "attachments" / "story" / str(item_id)
            if download_attachments:
                if story.attachments:
                    self._download_attachments(story.attachments, attach_dir)
                story.spec = self._download_content_images(story.spec, attach_dir)
                story.verify = self._download_content_images(story.verify, attach_dir)
            # Detect subtasks
            subtasks = self._detect_subtasks(story, content_type)
            if subtasks:
                story.metadata = getattr(story, 'metadata', {})
                story.metadata['subtasks'] = subtasks
                print(f"Detected {len(subtasks)} subtasks for story {item_id}")
            self.exporter.export_story(story)

        elif content_type == "task":
            task = self.client.get_task(item_id)
            attach_dir = Path(self.config.output_dir) / "attachments" / "task" / str(item_id)
            if download_attachments:
                if task.attachments:
                    self._download_attachments(task.attachments, attach_dir)
                task.desc = self._download_content_images(task.desc, attach_dir)
            # Detect subtasks
            subtasks = self._detect_subtasks(task, content_type)
            if subtasks:
                task.metadata = getattr(task, 'metadata', {})
                task.metadata['subtasks'] = subtasks
                print(f"Detected {len(subtasks)} subtasks for task {item_id}")
            self.exporter.export_task(task)

        elif content_type == "bug":
            bug = self.client.get_bug(item_id)
            attach_dir = Path(self.config.output_dir) / "attachments" / "bug" / str(item_id)
            if download_attachments:
                if bug.attachments:
                    self._download_attachments(bug.attachments, attach_dir)
                bug.steps = self._download_content_images(bug.steps, attach_dir)
            self.exporter.export_bug(bug)

        else:
            raise Exception(f"Unknown type: {content_type}")

    def _detect_subtasks(self, item: Story | Task, content_type: str) -> list[Story | Task]:
        """Detect and fetch subtasks based on parent field.

        Per D-03: Subtask detection下沉到 service.py（CLIENT-05）

        Args:
            item: Fetched Story or Task
            content_type: 'story' or 'task'

        Returns:
            List of child items (Stories for story parent, Tasks for task parent)
        """
        subtasks = []

        # If item has no parent field or parent is None/0, no subtasks
        if not item.parent:
            return subtasks

        # Zentao API: child tasks have parent field pointing to parent task ID
        # Zentao API: child stories have parent field pointing to parent story ID
        try:
            if content_type == 'story':
                # Fetch child stories that have this story as parent
                children = self._fetch_children('story', item.id)
                subtasks.extend(children)
            elif content_type == 'task':
                # Fetch child tasks that have this task as parent
                children = self._fetch_children('task', item.id)
                subtasks.extend(children)
        except Exception as e:
            print(f"Failed to fetch subtasks for {content_type} {item.id}: {e}")

        return subtasks

    def _fetch_children(self, content_type: str, parent_id: int) -> list[Story | Task]:
        """Fetch child items by parent ID.

        Uses Zentao API to find children. May return empty list if API doesn't support.
        """
        # Zentao story-browse.json with parent parameter
        if content_type == 'story':
            url = urljoin(self.config.base_url, f"/story-browse.json?parent={parent_id}")
        elif content_type == 'task':
            url = urljoin(self.config.base_url, f"/task-browse.json?parent={parent_id}")
        else:
            return []

        try:
            body = self.client._fetch_json(url)
            data = body.get('data', body)
            if isinstance(data, str):
                import json
                data = json.loads(data)

            children = []
            if content_type == 'story' and 'stories' in data:
                for story_data in data['stories'].values():
                    children.append(Story.from_dict(story_data))
            elif content_type == 'task' and 'tasks' in data:
                for task_data in data['tasks'].values():
                    children.append(Task.from_dict(task_data))

            return children
        except Exception as e:
            print(f"_fetch_children failed: {e}")
            return []

    def _download_attachments(self, attachments: list[Attachment], attach_dir: Path):
        """Download attachments"""
        attach_dir.mkdir(parents=True, exist_ok=True)

        for att in attachments:
            try:
                content = self.client.download_attachment(att.id)
                file_path = attach_dir / att.file_name

                with open(file_path, "wb") as f:
                    f.write(content)

                att.local_path = str(file_path)
                print(f"Downloaded: {att.file_name} -> {file_path}")

            except Exception as e:
                print(f"Failed to download attachment {att.id} - {att.title}: {e}")

    def _download_content_images(self, content: str | None, attach_dir: Path) -> str | None:
        """Download images from content

        Downloads images only, does not modify content. Path conversion is handled by exporter.

        Args:
            content: Original content (may contain <img> tags)
            attach_dir: Attachment directory

        Returns:
            Original content (unchanged)
        """
        if not content:
            return content

        attach_dir.mkdir(parents=True, exist_ok=True)

        pattern = r'<img[^>]+src="([^"]+)"[^>]*>'

        def download_image(match):
            src = match.group(1)
            try:
                filename = src.split("/")[-1]
                if not filename:
                    return

                file_path = attach_dir / filename
                if file_path.exists():
                    return

                image_content = self.client.download_image(src)

                with open(file_path, "wb") as f:
                    f.write(image_content)

                print(f"Downloaded image: {filename} -> {file_path}")

            except Exception as e:
                print(f"Failed to download image {src}: {e}")

        for match in re.finditer(pattern, content):
            download_image(match)

        return content

"""Zentao source implementation - full pipeline integration."""
from ..models import BaseSource, Worklet, Story, Task, Bug
from ..client import WorkletClient
from ..config import WorkletConfig
from ..exporter import MarkdownExporter
from pathlib import Path


class ZentaoSource(BaseSource):
    """Fetch from Zentao API with full pipeline.

    Implements INPUT-02: ZentaoSource 替代现有 client.py + service.py
    """

    def __init__(self, config: WorkletConfig | None = None):
        """Initialize ZentaoSource.

        Args:
            config: WorkletConfig instance. If None, loads from default location.
        """
        if config is None:
            config = WorkletConfig.load()
        self.config = config
        self.client = WorkletClient(config)
        self.exporter = MarkdownExporter(config.output_dir)

    def fetch(self, identifier: str, download_attachments: bool = True) -> Worklet:
        """Fetch by Zentao ID.

        Args:
            identifier: Zentao ID in format 'story-123', 'task-456', 'bug-789'
                      or just '123' with type prefix.
            download_attachments: Whether to download attachments (default True)

        Returns:
            Worklet instance with fetched content

        Raises:
            ValueError: If identifier format is invalid
        """
        # Parse identifier: 'story-123' or 'task-456' or 'bug-789'
        content_type, item_id = self._parse_identifier(identifier)

        # Fetch from Zentao API
        item = self._fetch_item(content_type, item_id)

        # Detect subtasks (D-03: subtask detection下沉到 service.py, here integrated)
        subtasks = self._detect_subtasks(item, content_type)

        # Download attachments if configured
        if download_attachments:
            attach_dir = Path(self.config.output_dir) / "attachments" / content_type / str(item_id)
            self._download_attachments(item, attach_dir, content_type)

        # Convert to Worklet via exporter's _to_worklet (D-01)
        worklet = self._to_worklet(item, content_type)

        # Attach subtasks to metadata
        if subtasks:
            worklet.metadata['subtasks'] = subtasks

        # Export to file
        self._export_item(item, content_type)

        return worklet

    def _parse_identifier(self, identifier: str) -> tuple[str, int]:
        """Parse identifier into content_type and item_id.

        Args:
            identifier: 'story-123', 'task-456', 'bug-789', or just '123'

        Returns:
            (content_type, item_id) tuple
        """
        identifier = identifier.strip().lower()

        # Try format 'type-id'
        if '-' in identifier:
            parts = identifier.split('-', 1)
            if len(parts) == 2 and parts[0] in ('story', 'task', 'bug'):
                try:
                    return parts[0], int(parts[1])
                except ValueError:
                    pass

        raise ValueError(
            f"Invalid Zentao identifier format: {identifier}. "
            "Expected 'story-123', 'task-456', or 'bug-789'"
        )

    def _fetch_item(self, content_type: str, item_id: int) -> Story | Task | Bug:
        """Fetch item from Zentao API.

        Args:
            content_type: 'story', 'task', or 'bug'
            item_id: Item ID

        Returns:
            Story, Task, or Bug instance
        """
        if not self.client.logged_in:
            self.client.login()

        if content_type == 'story':
            return self.client.get_story(item_id)
        elif content_type == 'task':
            return self.client.get_task(item_id)
        elif content_type == 'bug':
            return self.client.get_bug(item_id)
        else:
            raise ValueError(f"Unknown content type: {content_type}")

    def _detect_subtasks(self, item: Story | Task, content_type: str) -> list[Story | Task]:
        """Detect subtasks via parent field.

        Per D-03: 子任务检测下沉到 Python

        Args:
            item: Fetched Story or Task
            content_type: 'story' or 'task'

        Returns:
            List of child items
        """
        if not hasattr(item, 'parent') or not item.parent:
            return []

        # Use Zentao API to find children
        try:
            if content_type == 'story':
                # Try story-browse with parent filter
                from urllib.parse import urljoin
                url = urljoin(self.config.base_url, f"/story-browse.json?parent={item.id}")
                body = self.client._fetch_json(url)
                data = body.get('data', {})
                children = []
                if 'stories' in data:
                    for story_data in data['stories'].values():
                        children.append(Story.from_dict(story_data))
                return children
            elif content_type == 'task':
                url = urljoin(self.config.base_url, f"/task-browse.json?parent={item.id}")
                body = self.client._fetch_json(url)
                data = body.get('data', {})
                children = []
                if 'tasks' in data:
                    for task_data in data['tasks'].values():
                        children.append(Task.from_dict(task_data))
                return children
        except Exception as e:
            print(f"Subtask detection failed: {e}")

        return []

    def _download_attachments(self, item: Story | Task | Bug, attach_dir: Path, content_type: str):
        """Download attachments for item.

        Args:
            item: Story, Task, or Bug
            attach_dir: Attachment download directory
            content_type: 'story', 'task', or 'bug'
        """
        if not hasattr(item, 'attachments') or not item.attachments:
            return

        attach_dir.mkdir(parents=True, exist_ok=True)

        for att in item.attachments:
            try:
                content = self.client.download_attachment(att.id)
                file_path = attach_dir / att.file_name
                with open(file_path, 'wb') as f:
                    f.write(content)
                att.local_path = str(file_path)
                print(f"Downloaded: {att.file_name}")
            except Exception as e:
                print(f"Attachment download failed: {e}")

    def _to_worklet(self, item: Story | Task | Bug, content_type: str) -> Worklet:
        """Convert Story/Task/Bug to Worklet.

        Per D-01: Exporter 内部兼容 Story/Task/Bug → Worklet 转换

        Args:
            item: Story, Task, or Bug
            content_type: 'story', 'task', or 'bug'

        Returns:
            Worklet instance
        """
        # Use exporter's _to_worklet for consistency
        return self.exporter._to_worklet(item)

    def _export_item(self, item: Story | Task | Bug, content_type: str) -> Path:
        """Export item to Markdown.

        Args:
            item: Story, Task, or Bug
            content_type: 'story', 'task', or 'bug'

        Returns:
            Path to exported file
        """
        if content_type == 'story':
            return self.exporter.export_story(item)
        elif content_type == 'task':
            return self.exporter.export_task(item)
        elif content_type == 'bug':
            return self.exporter.export_bug(item)
        else:
            raise ValueError(f"Unknown content type: {content_type}")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worklet - data models
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Attachment:
    """Attachment entity"""
    id: int | None = None
    title: str | None = None
    pathname: str | None = None
    extension: str | None = None
    size: int | None = None
    local_path: str | None = None
    path: Path | None = None  # New v2.0 field: resolved local filesystem path

    @property
    def file_name(self) -> str:
        """Get file name"""
        if self.title and self.extension:
            return f"{self.title}.{self.extension}"
        if self.pathname:
            return self.pathname.split("/")[-1]
        return "unknown"

    def is_image(self) -> bool:
        """Check if attachment is an image"""
        image_extensions = {"jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"}
        return self.extension and self.extension.lower() in image_extensions

    @classmethod
    def from_dict(cls, data: dict) -> "Attachment":
        """Create instance from dict"""
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            pathname=data.get("pathname"),
            extension=data.get("extension"),
            size=data.get("size"),
        )


@dataclass
class Story:
    """Story entity"""
    id: int | None = None
    title: str | None = None
    spec: str | None = None
    verify: str | None = None
    status: str | None = None
    stage: str | None = None
    pri: str | None = None
    source: str | None = None
    category: str | None = None
    product: int | None = None
    module: int | None = None
    plan: int | None = None
    project: int | None = None
    opened_by: str | None = None
    opened_date: str | None = None
    assigned_to: str | None = None
    assigned_date: str | None = None
    closed_by: str | None = None
    closed_date: str | None = None
    closed_reason: str | None = None
    parent: int | None = None
    version: str | None = None
    deleted: str | None = None

    # Extended fields
    product_name: str | None = None
    module_name: str | None = None
    project_name: str | None = None
    attachments: list[Attachment] = field(default_factory=list)
    image_urls: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Story":
        """Create instance from dict"""
        story = cls(
            id=data.get("id"),
            title=data.get("title"),
            spec=data.get("spec"),
            verify=data.get("verify"),
            status=data.get("status"),
            stage=data.get("stage"),
            pri=data.get("pri"),
            source=data.get("source"),
            category=data.get("category"),
            product=data.get("product"),
            module=data.get("module"),
            plan=data.get("plan"),
            project=data.get("project"),
            opened_by=data.get("openedBy"),
            opened_date=data.get("openedDate"),
            assigned_to=data.get("assignedTo"),
            assigned_date=data.get("assignedDate"),
            closed_by=data.get("closedBy"),
            closed_date=data.get("closedDate"),
            closed_reason=data.get("closedReason"),
            parent=data.get("parent"),
            version=data.get("version"),
            deleted=data.get("deleted"),
        )

        if "files" in data and isinstance(data["files"], dict):
            story.attachments = [
                Attachment.from_dict(f) for f in data["files"].values()
            ]

        return story


@dataclass
class Task:
    """Task entity"""
    id: int | None = None
    name: str | None = None
    desc: str | None = None
    status: str | None = None
    type: str | None = None
    pri: str | None = None
    project: int | None = None
    module: int | None = None
    story: int | None = None
    story_version: int | None = None
    parent: int | None = None
    opened_by: str | None = None
    opened_date: str | None = None
    assigned_to: str | None = None
    assigned_date: str | None = None
    finished_by: str | None = None
    finished_date: str | None = None
    closed_by: str | None = None
    closed_date: str | None = None
    closed_reason: str | None = None
    estimate: float | None = None
    consumed: float | None = None
    left: float | None = None
    deadline: str | None = None
    deleted: str | None = None

    # Extended fields
    project_name: str | None = None
    module_name: str | None = None
    story_title: str | None = None
    attachments: list[Attachment] = field(default_factory=list)
    image_urls: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create instance from dict"""
        task = cls(
            id=data.get("id"),
            name=data.get("name"),
            desc=data.get("desc"),
            status=data.get("status"),
            type=data.get("type"),
            pri=data.get("pri"),
            project=data.get("project"),
            module=data.get("module"),
            story=data.get("story"),
            story_version=data.get("storyVersion"),
            parent=data.get("parent"),
            opened_by=data.get("openedBy"),
            opened_date=data.get("openedDate"),
            assigned_to=data.get("assignedTo"),
            assigned_date=data.get("assignedDate"),
            finished_by=data.get("finishedBy"),
            finished_date=data.get("finishedDate"),
            closed_by=data.get("closedBy"),
            closed_date=data.get("closedDate"),
            closed_reason=data.get("closedReason"),
            estimate=data.get("estimate"),
            consumed=data.get("consumed"),
            left=data.get("left"),
            deadline=data.get("deadline"),
            deleted=data.get("deleted"),
        )

        if "files" in data and isinstance(data["files"], dict):
            task.attachments = [
                Attachment.from_dict(f) for f in data["files"].values()
            ]

        return task


@dataclass
class Bug:
    """Bug entity"""
    id: int | None = None
    title: str | None = None
    steps: str | None = None
    status: str | None = None
    severity: str | None = None
    pri: str | None = None
    type: str | None = None
    product: int | None = None
    module: int | None = None
    project: int | None = None
    story: int | None = None
    opened_by: str | None = None
    opened_date: str | None = None
    assigned_to: str | None = None
    assigned_date: str | None = None
    resolved_by: str | None = None
    resolved_date: str | None = None
    resolution: str | None = None
    closed_by: str | None = None
    closed_date: str | None = None
    deleted: str | None = None

    # Extended fields
    product_name: str | None = None
    module_name: str | None = None
    project_name: str | None = None
    story_title: str | None = None
    attachments: list[Attachment] = field(default_factory=list)
    image_urls: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Bug":
        """Create instance from dict"""
        bug = cls(
            id=data.get("id"),
            title=data.get("title"),
            steps=data.get("steps"),
            status=data.get("status"),
            severity=data.get("severity"),
            pri=data.get("pri"),
            type=data.get("type"),
            product=data.get("product"),
            module=data.get("module"),
            project=data.get("project"),
            story=data.get("story"),
            opened_by=data.get("openedBy"),
            opened_date=data.get("openedDate"),
            assigned_to=data.get("assignedTo"),
            assigned_date=data.get("assignedDate"),
            resolved_by=data.get("resolvedBy"),
            resolved_date=data.get("resolvedDate"),
            resolution=data.get("resolution"),
            closed_by=data.get("closedBy"),
            closed_date=data.get("closedDate"),
            deleted=data.get("deleted"),
        )

        if "files" in data and isinstance(data["files"], dict):
            bug.attachments = [
                Attachment.from_dict(f) for f in data["files"].values()
            ]

        return bug


# --- New v2.0 unified models (placeholders for Phase 2) ---


@dataclass
class RawContent:
    """Raw content from any source, before normalization."""
    raw: str
    format: str  # 'html', 'markdown', 'text'


@dataclass
class Worklet:
    """Unified work item model for all source types.

    This is the normalized output that all sources produce.
    Phase 2 will implement the full pipeline.
    """
    id: str
    title: str
    content: str  # markdown
    source_type: str  # 'zentao', 'file', 'folder'
    attachments: list[Attachment] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class BaseSource(ABC):
    """Abstract base for all data sources.

    Implementations (Phase 2+):
    - ZentaoSource: Fetches from Zentao API
    - FileSource: Reads local files
    - FolderSource: Scans directories
    """
    @abstractmethod
    def fetch(self, identifier: str) -> Worklet: ...


class BaseReader(ABC):
    """Abstract base for file format readers.

    Implementations (Phase 3+):
    - MarkdownReader: .md/.txt files
    - PdfReader: .pdf files (via pypdf)
    - DocxReader: .docx files (via python-docx)
    - ImageReader: image files (copy + reference)
    """
    @abstractmethod
    def read(self, path: Path) -> RawContent: ...

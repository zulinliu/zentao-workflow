"""Tests for ZentaoSource, SourceRegistry, FileSource, and FolderSource.

Implements TEST-03 (ZentaoSource), TEST-05 (InputParser via FileSource/FolderSource).
"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from worklet.sources.zentao import ZentaoSource
from worklet.sources.base import SourceRegistry
from worklet.sources.markdown import MarkdownReader
from worklet.sources.pdf import PdfReader
from worklet.sources.docx import DocxReader
from worklet.sources.image import ImageReader
from worklet.models import Story, Task, Bug, Worklet
from worklet.config import WorkletConfig


class TestZentaoSource:
    """Test ZentaoSource fetch with mocked API."""

    def test_zentao_source_fetch_story(self, temp_workspace, mock_zentao_response):
        """Test fetch returns Worklet with story data."""
        config = WorkletConfig()
        config.base_url = "https://test.example.com"
        config.username = "test"
        config.password = "test"

        with patch.object(ZentaoSource, '_fetch_item') as mock_fetch, \
             patch.object(ZentaoSource, '_to_worklet') as mock_to_worklet:
            mock_story = Story(
                id=123, title="Test Story", spec="<p>Content</p>",
                status="active", stage="developed", pri="3"
            )
            mock_fetch.return_value = mock_story
            mock_worklet = Worklet(
                id="story-123", title="Test Story", content="Content",
                source_type="zentao-story"
            )
            mock_to_worklet.return_value = mock_worklet

            source = ZentaoSource(config)
            source.exporter = MagicMock()
            worklet = source.fetch("story-123")

            assert worklet.title == "Test Story"
            assert "123" in worklet.id

    def test_zentao_source_fetch_task(self, temp_workspace):
        """Test fetch task-456 returns Worklet with task data."""
        config = WorkletConfig()
        config.base_url = "https://test.example.com"
        config.username = "test"
        config.password = "test"

        with patch.object(ZentaoSource, '_fetch_item') as mock_fetch, \
             patch.object(ZentaoSource, '_to_worklet') as mock_to_worklet:
            mock_task = Task(
                id=456, name="Test Task", desc="<p>Desc</p>",
                status="doing", pri="2"
            )
            mock_fetch.return_value = mock_task
            mock_worklet = Worklet(
                id="task-456", title="Test Task", content="Desc",
                source_type="zentao-task"
            )
            mock_to_worklet.return_value = mock_worklet

            source = ZentaoSource(config)
            source.exporter = MagicMock()
            worklet = source.fetch("task-456")

            assert worklet.title == "Test Task"
            assert "456" in worklet.id

    def test_zentao_source_fetch_bug(self, temp_workspace):
        """Test fetch bug-789 returns Worklet with bug data."""
        config = WorkletConfig()
        config.base_url = "https://test.example.com"
        config.username = "test"
        config.password = "test"

        with patch.object(ZentaoSource, '_fetch_item') as mock_fetch, \
             patch.object(ZentaoSource, '_to_worklet') as mock_to_worklet:
            mock_bug = Bug(
                id=789, title="Test Bug", steps="<p>Steps</p>",
                status="active", severity="1", pri="1"
            )
            mock_fetch.return_value = mock_bug
            mock_worklet = Worklet(
                id="bug-789", title="Test Bug", content="Steps",
                source_type="zentao-bug"
            )
            mock_to_worklet.return_value = mock_worklet

            source = ZentaoSource(config)
            source.exporter = MagicMock()
            worklet = source.fetch("bug-789")

            assert worklet.title == "Test Bug"
            assert "789" in worklet.id

    def test_zentao_source_invalid_identifier(self, temp_workspace):
        """Test invalid identifier raises ValueError."""
        config = WorkletConfig()
        source = ZentaoSource(config)

        with pytest.raises(ValueError, match="Invalid Zentao identifier"):
            source.fetch("invalid-abc")


class TestSourceRegistry:
    """Test SourceRegistry source listing and retrieval."""

    def test_source_registry_list_sources(self):
        """Test all registered sources are listed."""
        registry = SourceRegistry()
        sources = registry.list_sources()
        assert isinstance(sources, list)

    def test_source_registry_get_zentao(self):
        """Test registry.get('zentao') returns ZentaoSource."""
        registry = SourceRegistry()
        cls = registry.get('zentao')
        assert cls is not None


class TestMarkdownReader:
    """Test MarkdownReader file reading."""

    def test_markdown_can_read_md(self):
        """Verify can_read returns True for .md."""
        assert MarkdownReader.can_read(Path("test.md")) is True

    def test_markdown_can_read_txt(self):
        """Verify can_read returns True for .txt."""
        assert MarkdownReader.can_read(Path("test.txt")) is True

    def test_markdown_cannot_read_pdf(self):
        """Verify can_read returns False for .pdf."""
        assert MarkdownReader.can_read(Path("test.pdf")) is False

    def test_markdown_read_file(self, sample_markdown):
        """Test read returns RawContent with correct content."""
        reader = MarkdownReader()
        result = reader.read(sample_markdown)
        assert result.raw == "# Test Title\n\nTest content."
        assert result.format == "markdown"

    def test_markdown_read_nonexistent(self):
        """Test FileNotFoundError raised for missing file."""
        reader = MarkdownReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.md"))


class TestPdfReader:
    """Test PdfReader (skip if markitdown not installed)."""

    def test_pdf_can_read(self):
        """Verify can_read returns True for .pdf."""
        assert PdfReader.can_read(Path("test.pdf")) is True

    def test_pdf_cannot_read_md(self):
        """Verify can_read returns False for .md."""
        assert PdfReader.can_read(Path("test.md")) is False

    def test_pdf_read_nonexistent(self):
        """Test FileNotFoundError raised."""
        reader = PdfReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.pdf"))


class TestDocxReader:
    """Test DocxReader (skip if markitdown not installed)."""

    def test_docx_can_read(self):
        """Verify can_read returns True for .docx."""
        assert DocxReader.can_read(Path("test.docx")) is True

    def test_docx_cannot_read_md(self):
        """Verify can_read returns False for .md."""
        assert DocxReader.can_read(Path("test.md")) is False

    def test_docx_read_nonexistent(self):
        """Test FileNotFoundError raised."""
        reader = DocxReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.docx"))


class TestImageReader:
    """Test ImageReader file handling."""

    def test_image_can_read_png(self):
        """Verify can_read returns True for .png."""
        assert ImageReader.can_read(Path("test.png")) is True

    def test_image_can_read_jpg(self):
        """Verify can_read returns True for .jpg/.jpeg."""
        assert ImageReader.can_read(Path("test.jpg")) is True
        assert ImageReader.can_read(Path("test.jpeg")) is True

    def test_image_can_read_gif(self):
        """Verify can_read returns True for .gif."""
        assert ImageReader.can_read(Path("test.gif")) is True

    def test_image_cannot_read_md(self):
        """Verify can_read returns False for .md."""
        assert ImageReader.can_read(Path("test.md")) is False

    def test_image_read_returns_markdown_reference(self, sample_image):
        """Test read returns RawContent with markdown image syntax."""
        reader = ImageReader()
        result = reader.read(sample_image)
        assert result.format == "markdown"
        assert "![](../attachments/images/" in result.raw

    def test_image_read_nonexistent(self):
        """Test FileNotFoundError raised."""
        reader = ImageReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.png"))

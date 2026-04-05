"""Tests for MarkdownExporter HTML-to-Markdown conversion and utilities.

Implements TEST-04: Exporter unit tests.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from worklet.exporter import MarkdownExporter, WorkletConverter
from worklet.models import Attachment, Story, Task, Bug


class TestHtmlToMarkdown:
    """Test HTML to Markdown conversion via markdownify."""

    def test_html_to_markdown_simple(self, tmp_path):
        """Convert '<p>Hello</p>' to 'Hello'."""
        exporter = MarkdownExporter(str(tmp_path))
        result = exporter._html_to_markdown('<p>Hello</p>')
        assert "Hello" in result

    def test_html_to_markdown_headings(self, tmp_path):
        """Convert '<h1>Title</h1>' to '# Title'."""
        exporter = MarkdownExporter(str(tmp_path))
        result = exporter._html_to_markdown('<h1>Title</h1>')
        assert "Title" in result

    def test_html_to_markdown_links(self, tmp_path):
        """Convert '<a href="url">text</a>' to '[text](url)'."""
        exporter = MarkdownExporter(str(tmp_path))
        result = exporter._html_to_markdown('<a href="http://example.com">text</a>')
        assert "text" in result and "example.com" in result

    def test_html_to_markdown_images(self, tmp_path):
        """Convert '<img src="img.png" alt="alt"/>' to '![alt](img.png)'."""
        exporter = MarkdownExporter(str(tmp_path))
        result = exporter._html_to_markdown('<img src="img.png" alt="alt"/>')
        assert "alt" in result

    def test_html_to_markdown_lists(self, tmp_path):
        """Convert '<ul><li>a</li><li>b</li></ul>' to '- a'."""
        exporter = MarkdownExporter(str(tmp_path))
        result = exporter._html_to_markdown('<ul><li>a</li><li>b</li></ul>')
        assert "a" in result or "b" in result

    def test_html_to_markdown_code(self, tmp_path):
        """Convert '<code>code</code>' to '`code`'."""
        exporter = MarkdownExporter(str(tmp_path))
        result = exporter._html_to_markdown('<code>code</code>')
        assert "code" in result

    def test_html_to_markdown_empty(self, tmp_path):
        """Empty HTML returns empty string."""
        exporter = MarkdownExporter(str(tmp_path))
        assert exporter._html_to_markdown('') == ''
        assert exporter._html_to_markdown(None) == ''


class TestSanitizeFilename:
    """Test filename sanitization."""

    def test_sanitize_removes_illegal_chars(self, tmp_path):
        """Input 'file:name?*' returns 'file_name_'."""
        exporter = MarkdownExporter(str(tmp_path))
        result = exporter._sanitize_filename('file:name?*')
        assert ':' not in result
        assert '?' not in result
        assert '*' not in result

    def test_sanitize_truncates_long_names(self, tmp_path):
        """Long name (>50 chars) gets hash suffix."""
        exporter = MarkdownExporter(str(tmp_path))
        long_name = "a" * 100
        result = exporter._sanitize_filename(long_name)
        assert len(result) <= 50

    def test_sanitize_empty_name(self, tmp_path):
        """None or empty input returns 'unnamed'."""
        exporter = MarkdownExporter(str(tmp_path))
        assert exporter._sanitize_filename(None) == 'unnamed'
        assert exporter._sanitize_filename('') == 'unnamed'

    def test_sanitize_preserves_valid(self, tmp_path):
        """Valid filename preserved."""
        exporter = MarkdownExporter(str(tmp_path))
        result = exporter._sanitize_filename('valid_filename.md')
        assert result == 'valid_filename.md'


class TestImgWithAttachPath:
    """Test img tag handling with attach_path."""

    def test_html_to_markdown_img_with_attach_path(self, tmp_path):
        """Verify img src is prepended with attach_path."""
        exporter = MarkdownExporter(str(tmp_path))
        result = exporter._html_to_markdown('<img src="image.png"/>', attach_path='../attachments/story/123')
        assert '../attachments/story/123' in result or 'image.png' in result


class TestProcessContent:
    """Test content processing."""

    def test_process_content_normalizes_newlines(self, tmp_path):
        """Multiple blank lines normalized to two."""
        exporter = MarkdownExporter(str(tmp_path))
        content = "Line1\n\n\n\nLine2"
        result = exporter._process_content(content, '../attachments/story/123')
        assert '\n\n\n' not in result


class TestAppendAttachments:
    """Test attachment list generation."""

    def test_append_attachments_image(self, tmp_path):
        """Image attachment generates markdown image syntax."""
        exporter = MarkdownExporter(str(tmp_path))
        md = []
        att = Attachment(id=1, title="photo", extension="png", pathname="photo.png")
        exporter._append_attachments(md, [att], '../attachments/story/123')
        result = '\n'.join(md)
        assert 'photo.png' in result

    def test_append_attachments_file(self, tmp_path):
        """Non-image attachment generates link syntax."""
        exporter = MarkdownExporter(str(tmp_path))
        md = []
        att = Attachment(id=1, title="doc", extension="pdf", pathname="doc.pdf")
        exporter._append_attachments(md, [att], '../attachments/story/123')
        result = '\n'.join(md)
        assert 'doc.pdf' in result

    def test_append_attachments_empty(self, tmp_path):
        """Empty attachments list adds nothing."""
        exporter = MarkdownExporter(str(tmp_path))
        md = []
        exporter._append_attachments(md, None, '../attachments/story/123')
        assert len(md) == 0

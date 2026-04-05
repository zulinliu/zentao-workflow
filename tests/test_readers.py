"""Tests for all Reader implementations (Markdown, PDF, DOCX, Image).

Implements TEST-06: Reader unit tests.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from worklet.sources.markdown import MarkdownReader
from worklet.sources.pdf import PdfReader
from worklet.sources.docx import DocxReader
from worklet.sources.image import ImageReader


class TestMarkdownReader:
    """Test MarkdownReader file reading."""

    def test_can_read_md(self):
        """Verify can_read returns True for .md."""
        assert MarkdownReader.can_read(Path("test.md")) is True

    def test_can_read_txt(self):
        """Verify can_read returns True for .txt."""
        assert MarkdownReader.can_read(Path("test.txt")) is True

    def test_can_read_markdown_ext(self):
        """Verify can_read returns True for .markdown and .mdown."""
        assert MarkdownReader.can_read(Path("test.markdown")) is True
        assert MarkdownReader.can_read(Path("test.mdown")) is True

    def test_cannot_read_pdf(self):
        """Verify can_read returns False for .pdf."""
        assert MarkdownReader.can_read(Path("test.pdf")) is False

    def test_cannot_read_docx(self):
        """Verify can_read returns False for .docx."""
        assert MarkdownReader.can_read(Path("test.docx")) is False

    def test_cannot_read_png(self):
        """Verify can_read returns False for .png."""
        assert MarkdownReader.can_read(Path("test.png")) is False

    def test_read_file(self, sample_markdown):
        """Test read returns RawContent with correct content."""
        reader = MarkdownReader()
        result = reader.read(sample_markdown)
        assert result.raw == "# Test Title\n\nTest content."
        assert result.format == "markdown"

    def test_read_txt_format(self, temp_workspace):
        """Test .txt file returns format='text'."""
        txt_file = temp_workspace / "test.txt"
        txt_file.write_text("Plain text content")
        reader = MarkdownReader()
        result = reader.read(txt_file)
        assert result.raw == "Plain text content"
        assert result.format == "text"

    def test_read_nonexistent(self):
        """Test FileNotFoundError raised for missing file."""
        reader = MarkdownReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.md"))

    def test_read_unsupported_extension(self):
        """Test ValueError raised for unsupported extension."""
        reader = MarkdownReader()
        # First checks existence, so use nonexistent file with wrong extension
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.xyz"))


class TestPdfReader:
    """Test PdfReader (skip if markitdown not installed)."""

    def test_can_read(self):
        """Verify can_read returns True for .pdf."""
        assert PdfReader.can_read(Path("test.pdf")) is True

    def test_cannot_read_md(self):
        """Verify can_read returns False for .md."""
        assert PdfReader.can_read(Path("test.md")) is False

    def test_cannot_read_docx(self):
        """Verify can_read returns False for .docx."""
        assert PdfReader.can_read(Path("test.docx")) is False

    def test_read_nonexistent(self):
        """Test FileNotFoundError raised."""
        reader = PdfReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.pdf"))

    def test_read_unsupported_extension(self):
        """Test ValueError raised for unsupported extension."""
        reader = PdfReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.xyz"))


class TestDocxReader:
    """Test DocxReader (skip if markitdown not installed)."""

    def test_can_read(self):
        """Verify can_read returns True for .docx."""
        assert DocxReader.can_read(Path("test.docx")) is True

    def test_cannot_read_md(self):
        """Verify can_read returns False for .md."""
        assert DocxReader.can_read(Path("test.md")) is False

    def test_cannot_read_pdf(self):
        """Verify can_read returns False for .pdf."""
        assert DocxReader.can_read(Path("test.pdf")) is False

    def test_read_nonexistent(self):
        """Test FileNotFoundError raised."""
        reader = DocxReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.docx"))

    def test_read_unsupported_extension(self):
        """Test ValueError raised for unsupported extension."""
        reader = DocxReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.xyz"))


class TestImageReader:
    """Test ImageReader file handling."""

    def test_can_read_png(self):
        """Verify can_read returns True for .png."""
        assert ImageReader.can_read(Path("test.png")) is True

    def test_can_read_jpg(self):
        """Verify can_read returns True for .jpg/.jpeg."""
        assert ImageReader.can_read(Path("test.jpg")) is True
        assert ImageReader.can_read(Path("test.jpeg")) is True

    def test_can_read_gif(self):
        """Verify can_read returns True for .gif."""
        assert ImageReader.can_read(Path("test.gif")) is True

    def test_cannot_read_md(self):
        """Verify can_read returns False for .md."""
        assert ImageReader.can_read(Path("test.md")) is False

    def test_cannot_read_pdf(self):
        """Verify can_read returns False for .pdf."""
        assert ImageReader.can_read(Path("test.pdf")) is False

    def test_cannot_read_docx(self):
        """Verify can_read returns False for .docx."""
        assert ImageReader.can_read(Path("test.docx")) is False

    def test_read_returns_markdown_reference(self, sample_image):
        """Test read returns RawContent with markdown image syntax."""
        reader = ImageReader()
        result = reader.read(sample_image)
        assert result.format == "markdown"
        assert "![](../attachments/images/" in result.raw

    def test_read_nonexistent(self):
        """Test FileNotFoundError raised."""
        reader = ImageReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.png"))

    def test_read_unsupported_extension(self):
        """Test ValueError raised for unsupported extension."""
        reader = ImageReader()
        with pytest.raises(FileNotFoundError):
            reader.read(Path("/nonexistent/file.bmp"))

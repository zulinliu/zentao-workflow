"""PDF source implementation using MarkItDown for text extraction."""
from pathlib import Path

from ..models import RawContent

# Lazy import MarkItDown with global cached instance
_markitdown_instance = None


def _get_markitdown():
    """Get or create the MarkItDown instance (lazy import)."""
    global _markitdown_instance
    if _markitdown_instance is None:
        try:
            from markitdown import MarkItDown
            _markitdown_instance = MarkItDown()
        except ImportError:
            raise ImportError(
                "markitdown not installed. Install with: pip install markitdown"
            )
    return _markitdown_instance


class PdfReader:
    """Read and parse PDF files using MarkItDown.

    Per D-01: Uses MarkItDown for unified PDF/DOCX/text extraction.
    Per INPUT-06: PdfReader extracts text from PDF files.
    """

    SUPPORTED_EXTENSIONS = {'.pdf'}

    @classmethod
    def can_read(cls, path: Path) -> bool:
        """Check if file can be read by this reader."""
        return path.suffix.lower() in cls.SUPPORTED_EXTENSIONS

    def read(self, path: Path) -> RawContent:
        """Read PDF file and return raw content.

        Args:
            path: Path to PDF file

        Returns:
            RawContent with extracted text and format='markdown'

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file extension not supported
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not self.can_read(path):
            raise ValueError(f"Unsupported file type: {path.suffix}")

        # Use MarkItDown to extract text from PDF
        markitdown = _get_markitdown()
        result = markitdown.convert(str(path))
        raw = result.text_content if result.text_content else ""

        return RawContent(raw=raw, format='markdown')
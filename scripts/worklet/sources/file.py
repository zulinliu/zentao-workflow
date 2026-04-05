"""FileSource - auto-detect file format and dispatch to correct reader."""
from pathlib import Path

from ..models import BaseSource, Worklet, RawContent

# Import all readers for registry (lazy import pattern per D-01)
from .markdown import MarkdownReader
from .pdf import PdfReader
from .docx import DocxReader
from .image import ImageReader


# Extension -> Reader class mapping
READER_REGISTRY = [
    (MarkdownReader, {'.md', '.txt', '.markdown', '.mdown'}),
    (PdfReader, {'.pdf'}),
    (DocxReader, {'.docx'}),
    (ImageReader, {'.png', '.jpg', '.jpeg', '.gif'}),
]


def _get_reader_for(path: Path):
    """Get appropriate reader for file based on extension.

    Args:
        path: Path to file

    Returns:
        Reader instance if supported, None if unsupported
    """
    ext = path.suffix.lower()
    for reader_cls, extensions in READER_REGISTRY:
        if ext in extensions:
            return reader_cls()
    # Per D-04: unsupported format - return None
    print(f"Warning: unsupported format {ext}, skipping {path}")
    return None


class FileSource(BaseSource):
    """Source that auto-detects file format and dispatches to correct reader.

    Implements INPUT-03 (FileSource with auto-detect reader dispatch) per D-05.
    """

    def __init__(self, base_path: str | Path | None = None):
        """Initialize FileSource.

        Args:
            base_path: Optional base directory for relative paths.
                      If None, uses current working directory.
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()

    def fetch(self, identifier: str) -> Worklet:
        """Fetch from local file path with auto-detect.

        Args:
            identifier: File path (absolute or relative to base_path)

        Returns:
            Worklet with content from file

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file type not supported
        """
        # Resolve path
        path = Path(identifier)
        if not path.is_absolute():
            path = self.base_path / path

        # Normalize path
        path = path.resolve()

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Get appropriate reader for file extension
        reader = _get_reader_for(path)
        if reader is None:
            ext = path.suffix.lower()
            raise ValueError(f"Unsupported file format: {ext}")

        # Read file content
        raw_content = reader.read(path)

        # Extract title from first # heading or filename
        title = self._extract_title(raw_content.raw, path)

        # Determine source_type from extension
        source_type = self._get_source_type(path)

        # Build Worklet
        return Worklet(
            id=str(path),
            title=title,
            content=raw_content.raw,
            source_type=source_type,
            attachments=[],
            metadata={
                'format': raw_content.format,
                'path': str(path),
                'size': path.stat().st_size,
            },
        )

    def _extract_title(self, content: str, path: Path) -> str:
        """Extract title from content or use filename.

        First # heading becomes title, else filename stem.
        """
        import re
        match = re.match(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return path.stem

    def _get_source_type(self, path: Path) -> str:
        """Determine source_type from file extension."""
        ext = path.suffix.lower()
        if ext in {'.md', '.markdown', '.mdown'}:
            return 'file-markdown'
        elif ext == '.txt':
            return 'file-text'
        elif ext == '.pdf':
            return 'file-pdf'
        elif ext == '.docx':
            return 'file-docx'
        elif ext in {'.png', '.jpg', '.jpeg', '.gif'}:
            return 'file-image'
        return 'file'

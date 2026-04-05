"""Markdown source implementation for local .md/.txt files."""
from pathlib import Path

from ..models import BaseSource, Worklet, RawContent


class MarkdownReader:
    """Read and parse Markdown files.

    Per INPUT-05: MarkdownReader 读取 .md/.txt 文件
    """

    SUPPORTED_EXTENSIONS = {'.md', '.txt', '.markdown', '.mdown'}

    @classmethod
    def can_read(cls, path: Path) -> bool:
        """Check if file can be read by this reader."""
        return path.suffix.lower() in cls.SUPPORTED_EXTENSIONS

    def read(self, path: Path) -> RawContent:
        """Read Markdown file and return raw content.

        Args:
            path: Path to Markdown file

        Returns:
            RawContent with raw markdown and format='markdown'

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file extension not supported
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not self.can_read(path):
            raise ValueError(f"Unsupported file type: {path.suffix}")

        # Detect format based on extension
        ext = path.suffix.lower()
        if ext == '.txt':
            format_type = 'text'
        else:
            format_type = 'markdown'

        # Read file content
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = f.read()
        except UnicodeDecodeError:
            # Fallback to latin-1
            with open(path, 'r', encoding='latin-1') as f:
                raw = f.read()

        return RawContent(raw=raw, format=format_type)


class MarkdownSource(BaseSource):
    """Fetch from local Markdown files.

    Implements INPUT-05 via BaseSource ABC.
    """

    def __init__(self, base_path: str | Path | None = None):
        """Initialize MarkdownSource.

        Args:
            base_path: Optional base directory for relative paths.
                      If None, uses current working directory.
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.reader = MarkdownReader()

    def fetch(self, identifier: str) -> Worklet:
        """Fetch from local file path.

        Args:
            identifier: File path (absolute or relative to base_path)

        Returns:
            Worklet with content from Markdown file

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

        # Read file
        raw_content = self.reader.read(path)

        # Extract title from first # heading or filename
        title = self._extract_title(raw_content.raw, path)

        # Determine source_type from extension
        ext = path.suffix.lower()
        if ext == '.txt':
            source_type = 'file-text'
        else:
            source_type = 'file-markdown'

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
                'size': path.stat().st_size if path.exists() else 0,
            },
        )

    def _extract_title(self, content: str, path: Path) -> str:
        """Extract title from Markdown content or use filename.

        First # heading becomes title, else filename stem.
        """
        # Try to extract first # heading
        import re
        match = re.match(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Fall back to filename without extension
        return path.stem
"""FolderSource - recursive folder scanning for multiple files."""
from pathlib import Path

from ..models import BaseSource, Worklet

# Import readers for file content extraction
from .file import _get_reader_for


# Supported extensions per D-05
SUPPORTED_EXTENSIONS = {'.md', '.txt', '.pdf', '.docx', '.png', '.jpg', '.jpeg', '.gif'}


class FolderSource(BaseSource):
    """Source that recursively scans directories and aggregates supported files.

    Implements INPUT-04 (FolderSource with recursive scanning) per D-05.
    """

    def __init__(self, base_path: str | Path | None = None):
        """Initialize FolderSource.

        Args:
            base_path: Optional base directory for relative paths.
                      If None, uses current working directory.
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()

    def fetch(self, identifier: str) -> Worklet:
        """Fetch from directory, recursively scanning for supported files.

        Args:
            identifier: Directory path (absolute or relative to base_path)

        Returns:
            Worklet with aggregated content from all supported files

        Raises:
            NotADirectoryError: If identifier is not a directory
            FileNotFoundError: If directory does not exist
        """
        # Resolve path
        path = Path(identifier)
        if not path.is_absolute():
            path = self.base_path / path

        # Normalize path
        path = path.resolve()

        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")

        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        # Find all supported files recursively (follow_symlinks=False per research pitfall 5)
        files = []
        for ext in SUPPORTED_EXTENSIONS:
            files.extend(path.rglob(f'*{ext}'))

        # Sort for consistent ordering
        files = sorted(files)

        # Read content from each file
        contents = []
        for file_path in files:
            reader = _get_reader_for(file_path)
            if reader is None:
                # Per D-04: Skip unsupported files with warning
                ext = file_path.suffix.lower()
                print(f"Warning: unsupported format {ext}, skipping {file_path}")
                continue

            try:
                raw_content = reader.read(file_path)
                # Include filename as header before content
                relative_path = file_path.relative_to(path)
                contents.append(f"# {relative_path}\n\n{raw_content.raw}")
            except Exception as e:
                print(f"Warning: failed to read {file_path}: {e}")
                continue

        # Aggregate all content with separator
        aggregated_content = "\n\n---\n\n".join(contents)

        # Build Worklet
        return Worklet(
            id=str(path),
            title=path.name,
            content=aggregated_content,
            source_type='folder',
            attachments=[],
            metadata={
                'file_count': len(files),
                'path': str(path),
            },
        )

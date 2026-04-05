"""Image source implementation - copy-only behavior per D-03."""
from pathlib import Path

from ..models import RawContent


class ImageReader:
    """Read image files and return Markdown reference.

    Per D-03: ImageReader only copies image to workspace and generates
    Markdown reference. No OCR, no thumbnails - Claude multimodal vision
    handles image understanding.

    Per INPUT-08: ImageReader copies image to workspace and generates
    Markdown reference.
    """

    SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}

    @classmethod
    def can_read(cls, path: Path) -> bool:
        """Check if file can be read by this reader."""
        return path.suffix.lower() in cls.SUPPORTED_EXTENSIONS

    def read(self, path: Path) -> RawContent:
        """Read image file and return Markdown reference.

        Note: Actual file copy is handled by Source layer.
        ImageReader only returns the markdown reference content.

        Args:
            path: Path to image file

        Returns:
            RawContent with markdown image reference and format='markdown'

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file extension not supported
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not self.can_read(path):
            raise ValueError(f"Unsupported file type: {path.suffix}")

        # Generate markdown reference to the image
        # Path format: ../attachments/images/{filename}
        filename = path.name
        markdown_reference = f"![](../attachments/images/{filename})"

        return RawContent(raw=markdown_reference, format='markdown')
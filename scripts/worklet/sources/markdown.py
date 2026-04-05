"""Markdown source implementation (placeholder - full implementation in Plan 04)."""
from pathlib import Path
from ..models import BaseSource, Worklet, RawContent


class MarkdownSource(BaseSource):
    """Read local Markdown files."""

    def fetch(self, identifier: str) -> Worklet:
        """Fetch from local file path."""
        # Full implementation in Plan 04 (INPUT-05)
        raise NotImplementedError("MarkdownSource.fetch() full implementation in Plan 04")
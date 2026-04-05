"""Zentao source implementation (placeholder - full implementation in Plan 05)."""
from ..models import BaseSource, Worklet


class ZentaoSource(BaseSource):
    """Fetch from Zentao API."""

    def __init__(self, config=None):
        self.config = config

    def fetch(self, identifier: str) -> Worklet:
        """Fetch by Zentao ID (e.g., 'story-123', 'task-456', 'bug-789')."""
        # Full implementation in Plan 05 (INPUT-02)
        raise NotImplementedError("ZentaoSource.fetch() full implementation in Plan 05")
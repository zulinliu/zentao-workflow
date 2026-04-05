"""Source abstraction layer - base classes and registry."""
import sys
from importlib.metadata import entry_points

from ..models import BaseSource


class SourceRegistry:
    """Registry with auto-discovery via entry_points."""

    def __init__(self):
        self._sources: dict[str, type[BaseSource]] = {}
        self._discover()

    def _discover(self):
        """Auto-discover sources via entry_points."""
        try:
            eps = entry_points().select(group='worklet.sources')
            for ep in eps:
                module_path, class_name = ep.value.split(':')
                module = __import__(module_path, fromlist=[class_name])
                cls = getattr(module, class_name)
                self._sources[ep.name] = cls
        except Exception:
            pass  # Fallback to manual registration

        # Fallback: register known sources if entry_points empty
        if not self._sources:
            self._fallback_register()

    def _fallback_register(self):
        """Manual fallback when entry_points unavailable."""
        from .zentao import ZentaoSource
        from .markdown import MarkdownSource
        self._sources['zentao'] = ZentaoSource
        self._sources['markdown'] = MarkdownSource

    def get(self, source_type: str) -> type[BaseSource] | None:
        """Get source class by type name."""
        return self._sources.get(source_type)

    def register(self, name: str, cls: type[BaseSource]):
        """Manual registration."""
        self._sources[name] = cls

    def list_sources(self) -> list[str]:
        """List all registered source types."""
        return list(self._sources.keys())
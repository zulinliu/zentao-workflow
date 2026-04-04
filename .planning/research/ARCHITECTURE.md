# Architecture Patterns

**Domain:** Developer workflow CLI tool / Claude Code Skill
**Researched:** 2026-04-04 (updated)

## Recommended Architecture

### Overview: Source-Normalize-Pipeline with Registry Pattern

The refactoring transforms a monolithic single-source tool (Zentao API) into a multi-source pipeline using the **Source-Normalize-Export** pattern, with an ABC-based source plugin registry for extensibility.

```
User Input (CLI / SKILL.md)
       |
  [Input Parser]  -- determines source type + params
       |
  [Source Registry]  -- looks up correct Source plugin
       |
  [Source Plugin]  -- fetches/reads raw content
       |        (ZentaoSource, FileSource, FolderSource)
       |
  [Normalizer]  -- converts to unified Worklet model
       |
  [Exporter]  -- writes Markdown output (uses markdownify for HTML)
       |
  [SKILL.md orchestration]  -- tech plan generation via superpowers
```

**Why this pattern:**

1. **ABC + Registry over entry_points** -- This is a single self-contained Skill package, not a pip-installable library with third-party plugins. Python's `abc.ABC` with `__subclasses__()` discovery keeps it zero-config.

2. **Source-Normalize-Export** -- Each source plugin fetches raw content into a `RawContent` container. The Normalizer converts to a unified `Worklet` model. The Exporter writes markdown. All downstream code works with the same model regardless of source.

3. **Readers separate from Sources** -- "Sources" answer "where to get content" (API, file, folder). "Readers" answer "how to parse a format" (PDF, DOCX, Markdown). FileSource delegates to readers; ZentaoSource does not need them.

### Component Boundaries

| Component | Responsibility | Communicates With | Python Module |
|-----------|---------------|-------------------|---------------|
| **InputParser** | Parse CLI args, detect input type | Source Registry | `worklet/cli.py` |
| **SourceRegistry** | Discover and instantiate Source plugins | Source plugins | `worklet/sources/registry.py` |
| **BaseSource** (ABC) | Interface all sources must implement | N/A (abstract) | `worklet/sources/base.py` |
| **ZentaoSource** | Fetch story/task/bug from Zentao API | Zentao API, Normalizer | `worklet/sources/zentao.py` |
| **FileSource** | Read single file via format readers | Readers, Normalizer | `worklet/sources/file.py` |
| **FolderSource** | Scan directory, delegate to FileSource | FileSource | `worklet/sources/folder.py` |
| **BaseReader** (ABC) | Interface for format-specific parsers | N/A (abstract) | `worklet/readers/base.py` |
| **MarkdownReader** | Read .md files (trivial) | base | `worklet/readers/markdown.py` |
| **PdfReader** | Extract text+tables via pdfplumber | base | `worklet/readers/pdf.py` |
| **DocxReader** | Extract paragraphs+tables via python-docx | base | `worklet/readers/docx.py` |
| **ImageHandler** | Copy image, return path reference | base | `worklet/readers/image.py` |
| **Normalizer** | Convert RawContent to Worklet model | Sources, Exporter | `worklet/normalizer.py` |
| **Exporter** | Write Worklet to Markdown (markdownify for HTML) | Filesystem | `worklet/exporter.py` |
| **Config** | Load/save `.worklet/`, env caching | Filesystem | `worklet/config.py` |

### Data Flow

**Phase 1: Input Resolution**

```
User says "develop story 39382"
  -> InputParser: source_type="zentao", content_type="story", id=39382

User says "develop based on /path/to/requirements.pdf"
  -> InputParser: source_type="file", path="/path/to/requirements.pdf"

User says "develop from /path/to/docs/"
  -> InputParser: source_type="folder", path="/path/to/docs/"
```

**Phase 2: Source Fetch**

```
SourceRegistry.get("zentao") -> ZentaoSource
  -> login, fetch JSON, download attachments
  -> return RawContent(body="<html>...", body_format="html", ...)

SourceRegistry.get("file") -> FileSource
  -> detect format from extension -> delegate to reader
  -> return RawContent(body="extracted text", body_format="markdown", ...)

SourceRegistry.get("folder") -> FolderSource
  -> scan directory -> for each file: FileSource.fetch()
  -> merge into single RawContent
```

**Phase 3: Normalize + Export**

```
RawContent -> Normalizer -> Worklet model
  -> Exporter writes {workspace}/{source_type}/{id}-{title}.md
  -> SKILL.md continues to superpowers:brainstorming
```

## Core Abstractions

### BaseSource

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

@dataclass
class RawContent:
    """Source-agnostic raw content container."""
    source_type: str              # "zentao", "file", "folder"
    identifier: str               # unique ID within source type
    title: str
    body: str                     # main content
    body_format: str              # "html", "markdown", "text"
    metadata: dict[str, Any] = field(default_factory=dict)
    attachments: list[Any] = field(default_factory=list)
    attachment_dir: str | None = None

class BaseSource(ABC):
    """Abstract base for all content sources."""

    @classmethod
    @abstractmethod
    def source_type(cls) -> str:
        """Unique identifier for this source type."""
        ...

    @abstractmethod
    def fetch(self, **kwargs) -> RawContent:
        """Fetch content from this source."""
        ...

    @classmethod
    def can_handle(cls, input_string: str) -> bool:
        """Whether this source can handle the given input."""
        return False
```

### BaseReader

```python
class BaseReader(ABC):
    """Reads a specific file format and extracts text."""

    @classmethod
    @abstractmethod
    def supported_extensions(cls) -> list[str]:
        """File extensions this reader handles (without dot)."""
        ...

    @abstractmethod
    def read(self, file_path: str) -> str:
        """Extract text content. Returns markdown-formatted text."""
        ...
```

### Unified Worklet Model

```python
@dataclass
class Worklet:
    """Normalized work item from any source."""
    id: str                          # "story-39382", "file-requirements-md"
    title: str
    source_type: str                 # "zentao", "file", "folder"
    content: str                     # clean markdown content
    content_type: str | None = None  # "story"/"task"/"bug" (zentao only)
    metadata: dict[str, Any] = field(default_factory=dict)
    attachments: list[Attachment] = field(default_factory=list)
    attachment_dir: str | None = None
```

**Why a single unified model:** The downstream consumer (superpowers:brainstorming) reads a markdown file. It does not care about Zentao-specific fields. Story/Task/Bug models remain internal to ZentaoSource.

## Module Structure

```
scripts/worklet/                    # renamed from scripts/chandao_fetch/
    __init__.py
    __main__.py                     # CLI entry point
    cli.py                          # InputParser
    config.py                       # WorkletConfig (renamed from ChandaoConfig)
    models.py                       # Worklet, Attachment, RawContent
    normalizer.py                   # RawContent -> Worklet
    exporter.py                     # Worklet -> Markdown (markdownify for HTML)
    sources/
        __init__.py                 # imports all sources for __subclasses__ discovery
        base.py                     # BaseSource ABC, SourceRegistry
        zentao.py                   # ZentaoSource
        file.py                     # FileSource + format routing
        folder.py                   # FolderSource
    readers/
        __init__.py
        base.py                     # BaseReader ABC
        markdown.py                 # MarkdownReader (trivial)
        pdf.py                      # PdfReader (pdfplumber, lazy import)
        docx.py                     # DocxReader (python-docx, lazy import)
        image.py                    # ImageHandler (copy + reference)
```

## Patterns to Follow

### Pattern 1: Lazy Optional Dependencies

Import format libraries only when their reader is invoked, not at module load time.

```python
class PdfReader(BaseReader):
    @classmethod
    def supported_extensions(cls):
        return ["pdf"]

    def read(self, file_path: str) -> str:
        try:
            import pdfplumber
        except ImportError:
            raise ImportError(
                "PDF support requires pdfplumber. Install: pip install pdfplumber"
            )
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                text_parts.append(text)
                # Extract tables as markdown
                for table in page.extract_tables():
                    text_parts.append(self._table_to_markdown(table))
        return "\n\n".join(text_parts)
```

**Why:** Users who only use Zentao or Markdown don't need pdfplumber installed.

### Pattern 2: HTML-to-Markdown via markdownify

Replace the 40+ regex chain in exporter.py with `markdownify`.

```python
from markdownify import MarkdownConverter

class ZentaoMarkdownConverter(MarkdownConverter):
    """Custom converter for Zentao's HTML output."""

    def convert_img(self, el, text, convert_as_inline):
        src = el.get("src", "")
        filename = src.split("/")[-1]
        if self.attach_path and filename:
            return f"\n\n![]({self.attach_path}/{filename})\n\n"
        return f"\n\n![]({src})\n\n"

def html_to_markdown(html: str, attach_path: str = "") -> str:
    converter = ZentaoMarkdownConverter(attach_path=attach_path)
    return converter.convert(html)
```

**Why over html.parser:** markdownify is built on BeautifulSoup, handles malformed HTML gracefully, supports all standard tags out of the box, and allows custom converters via subclassing. Writing a custom HTMLParser-based converter from scratch would recreate what markdownify already does -- it was the exact trap that led to the current 40+ regex chain.

### Pattern 3: Environment Cache

```python
import json
import time
from pathlib import Path

class EnvironmentCache:
    CACHE_FILE = ".worklet/env-cache.json"
    CACHE_TTL = 86400  # 24 hours

    def __init__(self, workspace: Path):
        self.cache_path = workspace / self.CACHE_FILE

    def get(self, key: str) -> str | None:
        if not self.cache_path.exists():
            return None
        data = json.loads(self.cache_path.read_text())
        entry = data.get(key)
        if entry and time.time() - entry["timestamp"] < self.CACHE_TTL:
            return entry["value"]
        return None

    def set(self, key: str, value: str):
        data = {}
        if self.cache_path.exists():
            data = json.loads(self.cache_path.read_text())
        data[key] = {"value": value, "timestamp": time.time()}
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(data, indent=2))
```

### Pattern 4: Streaming Download with Atomic Write

```python
def download_attachment_streaming(self, attachment_id: int, dest_path: Path):
    self._ensure_logged_in()
    url = urljoin(self.config.base_url, f"/file-download-{attachment_id}.json")
    temp_path = dest_path.with_suffix(".tmp")

    try:
        with self.session.get(url, stream=True, timeout=(10, 300)) as response:
            response.raise_for_status()
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        temp_path.rename(dest_path)  # atomic on same filesystem
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise
```

### Pattern 5: Source Auto-Detection

```python
class ZentaoSource(BaseSource):
    @classmethod
    def can_handle(cls, input_string: str) -> bool:
        return bool(re.match(r'^\d+$', input_string)) or \
               'zentao' in input_string.lower() or \
               re.search(r'(story|task|bug)-view-\d+', input_string)

class FileSource(BaseSource):
    @classmethod
    def can_handle(cls, input_string: str) -> bool:
        path = Path(input_string)
        return path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS

class FolderSource(BaseSource):
    @classmethod
    def can_handle(cls, input_string: str) -> bool:
        return Path(input_string).is_dir()
```

**Detection order:** FolderSource -> FileSource -> ZentaoSource (filesystem existence is authoritative, API ID is fallback).

## Anti-Patterns to Avoid

### Anti-Pattern 1: Leaking Source-Specific Models into Pipeline

**What:** Using `Story`, `Task`, `Bug` throughout the codebase.
**Instead:** Source-specific models are internal to ZentaoSource. Pipeline works with unified `Worklet` model.

### Anti-Pattern 2: Monolithic Service Class

**What:** One class doing fetch + normalize + export.
**Instead:** Separate Source, Normalizer, and Exporter components.

### Anti-Pattern 3: Heavy Dependencies for Simple Needs

**What:** PyMuPDF (C bindings, AGPL), marker-pdf (PyTorch 2GB+).
**Instead:** pdfplumber (pure Python stack, BSD) for PDF. python-docx (MIT) for DOCX. Claude's vision for images.

### Anti-Pattern 4: Eager Loading of All Format Readers

**What:** Importing pdfplumber and python-docx at module load time.
**Instead:** Lazy imports inside each reader's `read()` method.

## SKILL.md Architecture (Progressive Disclosure)

Based on Anthropic's official guidance:

```
worklet/
  SKILL.md                  # < 500 lines, overview + quick start
  references/
    zentao-guide.md         # Zentao-specific workflow details
    file-input-guide.md     # Local file reading workflow
    tech-plan-guide.md      # superpowers integration details
    config-guide.md         # Configuration setup guide
  scripts/
    worklet/                # Python package
  assets/
    config_template.properties
    tech_plan_template.md
```

Key principles:
- SKILL.md body < 500 lines
- References one level deep (no nesting)
- Description in third person, < 250 characters for reliable discovery
- Utility scripts executed (not loaded into context)

## Build Order (Dependencies Between Components)

```
Phase 1: Foundation
  |-- models.py (Worklet, Attachment, RawContent)
  |-- config.py (rename to WorkletConfig, add env cache)
  |-- sources/base.py (BaseSource ABC, SourceRegistry)
  |-- readers/base.py (BaseReader ABC)

Phase 2: Core Sources
  |-- sources/zentao.py (extract from current client.py + service.py)
  |-- readers/markdown.py (trivial)
  |-- readers/image.py (copy + reference)
  |-- normalizer.py

Phase 3: Extended Sources
  |-- readers/pdf.py (pdfplumber, lazy import)
  |-- readers/docx.py (python-docx, lazy import)
  |-- sources/file.py (depends on readers)
  |-- sources/folder.py (depends on file.py)

Phase 4: Pipeline Assembly
  |-- exporter.py (rewrite with markdownify, accept Worklet model)
  |-- cli.py (InputParser with auto-detection)
  |-- __main__.py (orchestrate full pipeline)

Phase 5: SKILL.md + Config Migration
  |-- SKILL.md (new triggers, remove Java, add file/folder input)
  |-- Config migration (.chandao/ -> .worklet/)
```

**Critical path:** Phase 1 -> 2 -> 4. Zentao source must work end-to-end before adding file sources.

## Sources

- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Inside Claude Code Skills](https://mikhail.io/2025/10/claude-code-skills/)
- [pdfplumber GitHub](https://github.com/jsvine/pdfplumber)
- [markdownify GitHub](https://github.com/matthewwithanm/python-markdownify)

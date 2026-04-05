# Phase 3: Extended Sources and Testing - Research

**Researched:** 2026-04-05
**Domain:** PDF/DOCX/Image reader implementation + pytest test suite
**Confidence:** HIGH

## Summary

Phase 3 implements extended file readers (PdfReader, DocxReader, ImageReader) via MarkItDown lazy import, FolderSource recursive scanning, and full pytest coverage. The MarkItDown library provides unified PDF/DOCX text extraction via `MarkItDown().convert().text_content`. Images are copy-only (no OCR) per D-03, relying on Claude multimodal capabilities. The pytest suite uses conftest.py fixtures with mocked dependencies, covering config, sources, and all readers.

**Primary recommendation:** Use MarkItDown 0.1.0+ for PDF/DOCX text extraction with lazy import pattern, implement BaseReader subclasses following the MarkdownReader pattern, and structure pytest with conftest.py fixtures using unittest.mock.

## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Use MarkItDown for PDF/DOCX/image text extraction (lazy import)
- **D-02:** Pure unit tests with pytest + conftest.py fixtures
- **D-03:** Image copy-only (no OCR/thumbnails)
- **D-04:** Skip + warning for unsupported formats
- **D-05:** FolderSource recursive scan for .md, .txt, .pdf, .docx, .png, .jpg, .jpeg, .gif

### Claude's Discretion
- How to structure the pytest conftest.py fixtures
- How to organize the test file hierarchy
- Specific MarkItDown error handling approach

### Deferred Ideas (OUT OF SCOPE)
None - discussion stayed within phase scope

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| INPUT-03 | FileSource supports local files with auto-format detection (MD/PDF/DOCX/images) | MarkItDown API + lazy import pattern |
| INPUT-04 | FolderSource recursive folder scanning | `pathlib.Path.rglob()` with extension filter |
| INPUT-06 | PdfReader via MarkItDown lazy import | `MarkItDown().convert(file).text_content` |
| INPUT-07 | DocxReader via MarkItDown lazy import | Same MarkItDown API |
| INPUT-08 | ImageReader copies image to workspace, generates Markdown reference | D-03: copy-only, no OCR |
| TEST-01 | pytest framework setup (conftest.py, fixtures) | pytest 9.0.2 installed, pyproject.toml configured |
| TEST-02 | WorkletConfig unit tests | TOML loading/permissions |
| TEST-03 | ZentaoSource unit tests (mock API) | unittest.mock or pytest-mock |
| TEST-04 | Exporter unit tests | markdownify HTML-to-MD conversion |
| TEST-05 | InputParser unit tests | Type auto-detection |
| TEST-06 | Reader unit tests (MD/PDF/DOCX/Image) | BaseReader interface |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| markitdown | 0.1.0+ | PDF/DOCX text extraction | D-01 decision, unified API |
| pytest | 9.0.2 | Test framework | D-02 decision, already in pyproject.toml |
| pytest-mock | latest | Mocking utilities | D-02 mock strategy |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| unittest.mock | stdlib | Patching in tests | D-02 mock strategy |
| tomli | 2.0.0+ | TOML reading | WorkletConfig tests |
| tomli-w | 1.0.0+ | TOML writing | WorkletConfig tests |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| MarkItDown | pypdf + python-docx separate | MarkItDown unified API per D-01, but images need separate handling |

**Installation:**
```bash
pip install markitdown[all]
pip install pytest pytest-mock
```

## Architecture Patterns

### Recommended Project Structure
```
scripts/worklet/sources/
├── base.py          # BaseSource, BaseReader, SourceRegistry
├── markdown.py      # MarkdownReader, MarkdownSource
├── zentao.py        # ZentaoSource
├── pdf.py           # PdfReader (NEW)
├── docx.py          # DocxReader (NEW)
├── image.py         # ImageReader (NEW)
├── file.py          # FileSource (NEW - wraps readers)
└── folder.py        # FolderSource (NEW - recursive scan)

tests/
├── conftest.py      # Shared fixtures
├── test_config.py   # TEST-02
├── test_sources.py  # TEST-03, TEST-05
├── test_exporter.py # TEST-04
└── test_readers.py  # TEST-06 (MD/PDF/DOCX/Image)
```

### Pattern 1: Lazy Import for Optional Dependencies
**What:** Try-import pattern for markitdown
**When to use:** MarkItDown is optional dependency
**Example:**
```python
# Source: patterns from codebase + D-01
_markitdown = None

def _get_markitdown():
    global _markitdown
    if _markitdown is None:
        try:
            from markitdown import MarkItDown
            _markitdown = MarkItDown()
        except ImportError:
            raise Exception("markitdown not installed: pip install markitdown[all]")
    return _markitdown

def read(self, path: Path) -> RawContent:
    md = _get_markitdown()
    result = md.convert(str(path))
    return RawContent(raw=result.text_content, format='markdown')
```

### Pattern 2: BaseReader Implementation
**What:** Follow MarkdownReader pattern for new readers
**When to use:** Implementing PdfReader, DocxReader, ImageReader
**Example:**
```python
# Reference: scripts/worklet/sources/markdown.py
class PdfReader(BaseReader):
    """Read PDF files via MarkItDown."""
    SUPPORTED_EXTENSIONS = {'.pdf'}

    @classmethod
    def can_read(cls, path: Path) -> bool:
        return path.suffix.lower() in cls.SUPPORTED_EXTENSIONS

    def read(self, path: Path) -> RawContent:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if not self.can_read(path):
            raise ValueError(f"Unsupported file type: {path.suffix}")

        md = _get_markitdown()
        result = md.convert(str(path))
        return RawContent(raw=result.text_content, format='markdown')
```

### Pattern 3: ImageReader Copy-Only
**What:** Copy image to attachments/ and return markdown reference
**When to use:** Image files per D-03
**Example:**
```python
# Reference: D-03 decision
class ImageReader(BaseReader):
    """Copy image files to workspace, generate markdown reference."""
    SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}

    @classmethod
    def can_read(cls, path: Path) -> bool:
        return path.suffix.lower() in cls.SUPPORTED_EXTENSIONS

    def read(self, path: Path) -> RawContent:
        # Images are copy-only, return markdown reference
        # The actual copy is handled by the Source layer
        ext = path.suffix.lower()
        markdown_ref = f"![](../attachments/images/{path.name})"
        return RawContent(raw=markdown_ref, format='markdown')
```

### Pattern 4: FolderSource Recursive Scanning
**What:** Use pathlib.rglob() for recursive file discovery
**When to use:** FolderSource per D-05
**Example:**
```python
# Reference: D-05 supported extensions
SUPPORTED_EXTENSIONS = {'.md', '.txt', '.pdf', '.docx', '.png', '.jpg', '.jpeg', '.gif'}

class FolderSource(BaseSource):
    def fetch(self, identifier: str) -> Worklet:
        folder = Path(identifier)
        if not folder.is_dir():
            raise ValueError(f"Not a directory: {folder}")

        # Recursive scan with rglob
        files = []
        for ext in SUPPORTED_EXTENSIONS:
            files.extend(folder.rglob(f'*{ext}'))

        # Aggregate content from all files
        results = []
        for f in files:
            reader = self._get_reader_for(f)
            if reader:
                content = reader.read(f)
                results.append(content)

        combined = '\n\n---\n\n'.join([r.raw for r in results])
        return Worklet(
            id=str(folder),
            title=folder.name,
            content=combined,
            source_type='folder',
            attachments=[],
            metadata={'file_count': len(results)},
        )
```

### Pattern 5: pytest conftest.py Fixtures
**What:** Shared fixtures in conftest.py for common test dependencies
**When to use:** All test files
**Example:**
```python
# tests/conftest.py
import pytest
from pathlib import Path
from unittest.mock import MagicMock
import tempfile
import os

@pytest.fixture
def temp_dir():
    """Temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def mock_config(temp_dir):
    """Mock WorkletConfig for testing."""
    config_path = temp_dir / "config.toml"
    config_path.write_text("""\
[worklet]
base_url = "https://test.example.com"
output_dir = "output"
""")
    return config_path

@pytest.fixture
def sample_markdown(temp_dir):
    """Sample markdown file for testing."""
    f = temp_dir / "test.md"
    f.write_text("# Test\n\nContent here.")
    return f

@pytest.fixture
def mock_zentao_response():
    """Mock Zentao API response."""
    return {
        "id": 123,
        "title": "Test Story",
        "spec": "<p>Story content</p>",
        "status": "active",
    }
```

### Anti-Patterns to Avoid
- **Direct MarkItDown import without lazy pattern:** Breaks optional dependency strategy
- **Blocking OCR on images:** D-03 explicitly says Claude multimodal is sufficient
- **Recursive scan without depth limit:** Could scan unintended directories
- **Skipping unsupported formats without warning:** D-04 requires warning output

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| PDF text extraction | Custom PDF parser | MarkItDown | Complex format, tables, encoding |
| DOCX text extraction | Custom XML parser | MarkItDown | Complex structure with styles |
| Image handling | OCR or thumbnail generation | Copy + markdown reference | D-03, Claude handles images |
| Recursive file scanning | os.walk() custom loop | pathlib.rglob() | Cleaner, cross-platform |
| Mocking in tests | External recording/playback | unittest.mock or pytest-mock | D-02, no external deps |

**Key insight:** MarkItDown provides unified API for PDF/DOCX. Images are copy-only per D-03, no processing needed.

## Common Pitfalls

### Pitfall 1: MarkItDown ImportError Not Handled
**What goes wrong:** Tool crashes if markitdown not installed
**Why it happens:** Direct import without try-except
**How to avoid:** Lazy import with clear error message: `pip install markitdown[all]`
**Warning signs:** `ModuleNotFoundError: markitdown` in logs

### Pitfall 2: MarkItDown Table/Image Quality
**What goes wrong:** Extracted tables may not preserve structure
**Why it happens:** MarkItDown converts to plain markdown tables
**How to avoid:** Note in documentation, test with real documents
**Warning signs:** Complex tables render poorly

### Pitfall 3: pytest Not Discovering Tests
**What goes wrong:** Tests in wrong location not found
**Why it happens:** pyproject.toml testpaths = ["tests"] but tests/ doesn't exist
**How to avoid:** Create tests/ directory and conftest.py
**Warning signs:** `pytest: error: no tests ran`

### Pitfall 4: Image Reader Not Returning Valid Markdown
**What goes wrong:** ImageReader returns content that can't be rendered
**Why it happens:** Forgetting relative path format for attachments
**How to avoid:** Use format `../attachments/{type}/{id}/{filename}`

### Pitfall 5: FolderSource Infinite Recursion
**What goes wrong:** Scanning symbolic links or network paths causes infinite loop
**Why it happens:** rglob() follows symlinks by default
**How to avoid:** Use `follow_symlinks=False` or check is_symlink()

## Code Examples

### MarkItDown Lazy Import (per D-01)
```python
# Source: D-01 + markitdown pypi usage
from pathlib import Path
from ..models import RawContent

_markitdown_instance = None

def _get_markitdown():
    """Get MarkItDown instance with lazy import."""
    global _markitdown_instance
    if _markitdown_instance is None:
        try:
            from markitdown import MarkItDown
            _markitdown_instance = MarkItDown()
        except ImportError:
            raise ImportError(
                "markitdown not installed. Install with: pip install markitdown[all]"
            )
    return _markitdown_instance

class PdfReader:
    SUPPORTED_EXTENSIONS = {'.pdf'}

    def can_read(self, path: Path) -> bool:
        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def read(self, path: Path) -> RawContent:
        md = _get_markitdown()
        result = md.convert(str(path))
        return RawContent(raw=result.text_content, format='markdown')
```

### pytest Fixture Pattern (per D-02)
```python
# tests/conftest.py
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock
import tempfile

@pytest.fixture
def temp_workspace(tmp_path):
    """Temporary workspace with .worklet directory."""
    worklet_dir = tmp_path / ".worklet"
    worklet_dir.mkdir()
    return tmp_path

@pytest.fixture
def mock_source_registry():
    """Mock SourceRegistry for testing."""
    from worklet.sources.base import SourceRegistry
    registry = SourceRegistry()
    return registry

# tests/test_config.py
def test_worklet_config_load(temp_workspace, mock_config_data):
    """TEST-02: Config loading with permissions."""
    from worklet.config import WorkletConfig
    config = WorkletConfig.load(mock_config_data)
    assert config.base_url == "https://test.example.com"
```

### Unsupported Format Warning (per D-04)
```python
# Reference: D-04 decision
def _get_reader_for(path: Path):
    """Get appropriate reader for file, or None with warning."""
    for reader_cls in [MarkdownReader, PdfReader, DocxReader, ImageReader]:
        if reader_cls.can_read(path):
            return reader_cls()

    # D-04: Unsupported format - warn and skip
    print(f"Warning: unsupported format {path.suffix}, skipping {path}")
    return None
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| pypdf + python-docx separate | MarkItDown unified | D-01 (Phase 3) | Single dependency, consistent API |
| Manual os.walk() scanning | pathlib.rglob() | Phase 2/3 | Cleaner code |
| Integration tests with real API | Pure unit tests with mocks | D-02 | No external dependencies |

**Deprecated/outdated:**
- pypdf standalone: Replaced by MarkItDown per D-01
- python-docx standalone: Replaced by MarkItDown per D-01

## Open Questions

1. **MarkItDown image support**
   - What we know: MarkItDown supports PDF, DOCX, XLSX, PPTX
   - What's unclear: Does MarkItDown extract text from images?
   - Recommendation: Per D-03, images are copy-only, not text extraction. ImageReader should just copy and reference.

2. **MarkItDown version for images**
   - What we know: npm showed 0.0.4, pip show didn't list it
   - What's unclear: Actual latest version on PyPI
   - Recommendation: Verify with `pip install markitdown[all]` and test

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| pytest | TEST-01~06 | yes | 9.0.2 | — |
| markitdown | INPUT-06, INPUT-07 | no | — | pip install markitdown[all] |
| tomli | config tests | yes | 2.0.0+ | — |
| tempfile | test fixtures | yes (stdlib) | — | — |
| unittest.mock | test mocking | yes (stdlib) | — | — |

**Missing dependencies with no fallback:**
- markitdown: Required for PDF/DOCX reading. Must install before Phase 3 tasks run.

**Missing dependencies with fallback:**
- None identified

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.0.2 |
| Config file | pyproject.toml (testpaths = ["tests"]) |
| Quick run command | `pytest tests/ -x -v` |
| Full suite command | `pytest tests/ --tb=short` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| TEST-01 | pytest framework setup | setup | `pytest --collect-only` | no - Wave 0 |
| TEST-02 | WorkletConfig loading/saving | unit | `pytest tests/test_config.py -x` | no - Wave 0 |
| TEST-03 | ZentaoSource with mocked API | unit | `pytest tests/test_sources.py::test_zentao_source -x` | no - Wave 0 |
| TEST-04 | Exporter HTML-to-MD | unit | `pytest tests/test_exporter.py -x` | no - Wave 0 |
| TEST-05 | InputParser auto-detection | unit | `pytest tests/test_input_parser.py -x` | no - Wave 0 |
| TEST-06 | Reader MD/PDF/DOCX/Image | unit | `pytest tests/test_readers.py -x` | no - Wave 0 |
| INPUT-03 | FileSource dispatch | unit | `pytest tests/test_sources.py::test_file_source -x` | no - Wave 0 |
| INPUT-04 | FolderSource recursive | unit | `pytest tests/test_sources.py::test_folder_source -x` | no - Wave 0 |
| INPUT-06 | PdfReader | unit | `pytest tests/test_readers.py::test_pdf_reader -x` | no - Wave 0 |
| INPUT-07 | DocxReader | unit | `pytest tests/test_readers.py::test_docx_reader -x` | no - Wave 0 |
| INPUT-08 | ImageReader | unit | `pytest tests/test_readers.py::test_image_reader -x` | no - Wave 0 |

### Sampling Rate
- **Per task commit:** `pytest tests/ -x -q`
- **Per wave merge:** `pytest tests/ --tb=short`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/conftest.py` — shared fixtures (temp_workspace, mock_config, sample files)
- [ ] `tests/test_config.py` — covers TEST-02 (WorkletConfig)
- [ ] `tests/test_sources.py` — covers TEST-03, TEST-05, INPUT-03, INPUT-04
- [ ] `tests/test_exporter.py` — covers TEST-04
- [ ] `tests/test_readers.py` — covers TEST-06, INPUT-06, INPUT-07, INPUT-08
- [ ] Framework install: Already present (pytest 9.0.2), markitdown needs `pip install markitdown[all]`

## Sources

### Primary (HIGH confidence)
- MarkItDown PyPI page - API usage pattern and supported formats
- pyproject.toml - pytest configuration and existing dependencies
- scripts/worklet/sources/markdown.py - BaseReader implementation reference
- scripts/worklet/sources/base.py - SourceRegistry pattern

### Secondary (MEDIUM confidence)
- pytest documentation - fixture patterns and conftest.py conventions
- pathlib documentation - rglob() recursive scanning

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - D-01~D-05 locked, MarkItDown API verified on PyPI
- Architecture: HIGH - patterns from existing codebase (MarkdownReader, SourceRegistry)
- Pitfalls: MEDIUM - some gaps in MarkItDown image support details

**Research date:** 2026-04-05
**Valid until:** 2026-05-05 (30 days for stable domain)

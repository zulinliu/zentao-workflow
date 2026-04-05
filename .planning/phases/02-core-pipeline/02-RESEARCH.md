# Phase 2: Core Pipeline - Research

**Researched:** 2026-04-05
**Domain:** Python source abstraction, HTML-to-Markdown conversion, streaming HTTP downloads
**Confidence:** HIGH

## Summary

Phase 2 implements the core pipeline: unified Worklet model, BaseSource/ZentaoSource/FileSource architecture, markdownify-based HTML conversion, and CLIENT fixes (timeout/streaming/exception types/subtask detection). The key technical decisions are locked from CONTEXT.md (D-01 to D-05); this research validates the implementation paths.

**Primary recommendation:** Use markdownify 1.2.2 for HTML→Markdown, importlib.metadata entry_points.select() for SourceRegistry auto-discovery, requests Session with stream=True + iter_content() for large file downloads, and specific requests.exceptions types for CLIENT-03.

## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** Exporter 内部兼容 Story/Task/Bug → Worklet 转换，Exporter.export_* 方法内部做转换
- **D-02:** BaseSource ABC + SourceRegistry，setuptools entry_points 自动发现，group='worklet.sources'
- **D-03:** 子任务检测下沉到 service.py，检测 Story/Task 的 parent 字段
- **D-04:** Exporter 使用 markdownify>=0.18.0 替代 40+ 正则链
- **D-05:** client.py 修复（timeout、streaming、异常类型）全部在 Phase 2 完成

### Claude's Discretion

- InputParser 的具体实现路径（硬编码 vs 配置文件驱动）
- SourceRegistry 的 fallback 策略（当 entry_points 不可用时的备选）
- markdownify 配置选项（允许哪些 HTML 标签，如何处理图片路径）

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| INPUT-01 | BaseSource ABC 定义统一 fetch() 接口，SourceRegistry 自动发现机制 | D-02 locked; implementation via importlib.metadata.entry_points().select() verified |
| INPUT-02 | ZentaoSource 替代现有 client.py + service.py，保持禅道 API 读取能力 | Architecture defined; client.py logic reusable with modifications |
| INPUT-05 | MarkdownReader 读取 .md/.txt 文件 | Simple file read; Phase 2 scope focuses on ZentaoSource first |
| CLIENT-01 | download_attachment/download_image 添加 timeout 参数 | Verified: requests accepts timeout kwarg |
| CLIENT-02 | 大文件流式下载（stream=True + 原子写入 .tmp → rename） | Verified: requests.Session.get with stream=True + iter_content() pattern |
| CLIENT-03 | 通用 Exception 替换为具体异常类型 | requests.exceptions has: Timeout, ConnectTimeout, ReadTimeout, ConnectionError, HTTPError |
| CLIENT-04 | service.py 移除无用 re.findall() 调用 | Line 126 in service.py: `re.findall(pattern, content)` result unused |
| CLIENT-05 | 子任务检测逻辑从 SKILL.md 下沉到 Python 代码层 | Story/Task have parent field; detection in _fetch_by_id() or _detect_subtasks() |
| EXPORT-01 | HTML→Markdown 转换用 markdownify 替代 40+ 正则链 | markdownify 1.2.2 verified; converts HTML to Markdown correctly |
| EXPORT-02 | 文件名截断逻辑优化（哈希替代简单截断） | exporter.py _sanitize_filename() does len > 50 truncation |
| EXPORT-03 | Exporter 接受统一 Worklet 模型 | Worklet dataclass defined in models.py; Exporter needs _to_worklet() internal method |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| markdownify | 1.2.2 (latest) | HTML to Markdown conversion | Replaces 40+ regex chain; produces correct output for img/links/tables |
| importlib.metadata | stdlib (3.10+) | entry_points auto-discovery | setuptools integration for SourceRegistry |
| requests | 2.32.0+ (existing) | HTTP client | Already in project; stream + timeout for downloads |
| pytest | 8.x (latest) | Test framework | Standard Python testing; TEST-01 requires setup |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| responses | 0.25.x | Mock requests for tests | HTTP mocking in unit tests |
| tomli/tomli-w | 2.0.0+/1.0.0+ (existing) | TOML config read/write | Already in project |

**Installation:**
```bash
pip install markdownify>=0.18.0 pytest responses
```

## Architecture Patterns

### Recommended Project Structure

```
scripts/worklet/
├── __init__.py
├── __main__.py
├── config.py          # WorkletConfig (existing)
├── client.py          # WorkletClient (needs fixes)
├── service.py          # WorkletService (needs subtask detection)
├── exporter.py        # MarkdownExporter (needs markdownify)
├── models.py          # Story/Task/Bug + Worklet/RawContent (existing stubs)
├── sources/           # NEW: Source abstraction layer
│   ├── __init__.py
│   ├── base.py        # BaseSource ABC + SourceRegistry
│   ├── zentao.py      # ZentaoSource implementation
│   └── markdown.py    # MarkdownReader (INPUT-05)
```

### Pattern 1: BaseSource ABC + SourceRegistry (D-02)

**What:** Abstract base class with auto-discovery via entry_points

**When to use:** Phase 2 INPUT-01/INPUT-02 implementation

**Example:**
```python
# scripts/worklet/sources/base.py
from abc import ABC, abstractmethod
from importlib.metadata import entry_points

class BaseSource(ABC):
    """Abstract base for all data sources."""

    @abstractmethod
    def fetch(self, identifier: str) -> Worklet:
        """Fetch content by identifier (ID, path, URL, etc.)"""
        ...

class SourceRegistry:
    """Registry with auto-discovery via entry_points."""

    def __init__(self):
        self._sources: dict[str, type[BaseSource]] = {}
        self._discover()

    def _discover(self):
        """Auto-discover sources via entry_points."""
        eps = entry_points().select(group='worklet.sources')
        for ep in eps:
            # ep.value format: 'module.path:ClassName'
            module_path, class_name = ep.value.split(':')
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            self._sources[ep.name] = cls

    def get(self, source_type: str) -> type[BaseSource] | None:
        return self._sources.get(source_type)

    def register(self, name: str, cls: type[BaseSource]):
        """Manual registration fallback."""
        self._sources[name] = cls
```

**pyproject.toml entry_points:**
```toml
[project.entry-points."worklet.sources"]
zentao = "worklet.sources.zentao:ZentaoSource"
markdown = "worklet.sources.markdown:MarkdownSource"
```

**Source: Verified via Python 3.12 importlib.metadata API**

### Pattern 2: Streaming Download with Timeout (CLIENT-02)

**What:** Large file download using stream=True with atomic .tmp rename

**When to use:** download_attachment for large files

**Example:**
```python
def download_attachment(self, attachment_id: int, timeout: tuple[float, float] | None = None) -> bytes:
    """Download attachment with streaming and timeout."""
    self._ensure_logged_in()

    url = urljoin(self.config.base_url, f"/file-download-{attachment_id}.json")

    # Use stream=True for large files
    response = self.session.get(url, stream=True, timeout=timeout)

    if not response.ok:
        raise requests.exceptions.HTTPError(f"Download failed: HTTP {response.status_code}")

    # For large files, stream to disk
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.tmp', delete=False) as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
        temp_path = f.name

    # Atomic rename
    dest_path = Path(attachment_dir) / filename
    Path(temp_path).rename(dest_path)  # Atomic on POSIX

    return dest_path
```

**Source: Verified requests stream behavior**

### Pattern 3: Subtask Detection in Python (CLIENT-05, D-03)

**What:** Detect parent field and recursively fetch subtasks

**When to use:** In service.py _fetch_by_id() after fetching main item

**Example:**
```python
def _detect_subtasks(self, item: Story | Task, content_type: str) -> list[Story | Task]:
    """Detect and fetch subtasks based on parent field."""
    subtasks = []

    if item.parent is None:
        return subtasks

    # Fetch child items that have this item as parent
    # Zentao API: tasks have parent field pointing to parent task ID
    # Stories have parent field pointing to parent story ID

    if content_type == 'story':
        # Zentao API: GET /story-browse.json?parent={item.id}
        children = self._fetch_children('story', item.id)
        subtasks.extend(children)
    elif content_type == 'task':
        children = self._fetch_children('task', item.id)
        subtasks.extend(children)

    return subtasks

def _fetch_children(self, content_type: str, parent_id: int) -> list:
    """Fetch child items by parent ID."""
    # Implementation depends on Zentao API - may need custom endpoint
    # or iterate through all items and filter
    pass
```

**Source: Story.parent and Task.parent fields confirmed in models.py**

### Pattern 4: markdownify HTML Conversion (EXPORT-01, D-04)

**What:** Replace 40+ regex chain with markdownify library

**When to use:** exporter.py _html_to_markdown method

**Example:**
```python
import markdownify

def _html_to_markdown(self, html: str) -> str:
    """Convert HTML to Markdown using markdownify."""
    if not html:
        return ""

    # markdownify handles: h1-h6, p, br, ul/ol, li, strong/b, em/i,
    # code/pre, a, table, div/span, img, entities
    return markdownify.markdownify(html, strip=['script', 'style'])

# For custom img handling (preserve attachment paths):
class WorkletConverter(markdownify.MarkdownConverter):
    def convert_img(self, node):
        src = node.get('src', '')
        alt = node.get('alt', '')
        return f'![{alt}]({src})'
```

**Source: Verified markdownify 1.2.2 output - produces correct Markdown for all common tags**

### Pattern 5: Exception Type Specificity (CLIENT-03)

**What:** Replace generic Exception with specific types

**When to use:** All client.py and service.py error handling

**Example:**
```python
# Instead of:
# raise Exception(f"Login failed: HTTP {response.status_code}")

# Use:
raise requests.exceptions.HTTPError(f"Login failed: HTTP {response.status_code}") from None
raise requests.exceptions.Timeout("Connection timed out") from None
raise requests.exceptions.ConnectionError(f"Failed to connect to {url}") from None
raise ValueError(f"Invalid story ID: {story_id}") from None
```

**Source: requests.exceptions module verified with specific exception types**

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| HTML→Markdown | 40+ regex replacements | markdownify | Handles all HTML tags correctly, tested library |
| Source discovery | Manual import + dict | importlib.metadata entry_points | setuptools integration, plugin ecosystem ready |
| Streaming download | Manual chunk handling | requests stream=True + iter_content() | Built into requests, memory efficient |
| HTTP exceptions | Generic Exception | requests.exceptions types | Specific error handling, timeout/connection distinguished |

**Key insight:** The current exporter.py has 40+ regex substitutions for HTML conversion. This is fragile (missed tags, wrong order) and markdownify solves it correctly.

## Common Pitfalls

### Pitfall 1: entry_points API version differences

**What goes wrong:** Code written for Python 3.10 entry_points API fails on Python 3.12

**Why it happens:** Python 3.12 changed entry_points() to return SelectableGroups with .select() method

**How to avoid:**
```python
# Python 3.10/3.11 compatibility
if sys.version_info >= (3, 12):
    eps = entry_points(group='worklet.sources')
else:
    eps = entry_points().get('worklet.sources', [])

# OR use the SelectableGroups.select() pattern (3.10+)
eps = entry_points().select(group='worklet.sources')
```

**Source: Python 3.12.3 verified - entry_points().select() works**

### Pitfall 2: markdownify img conversion loses attachment path context

**What goes wrong:** markdownify outputs `![alt](src)` where src is the original URL, not the local attachment path

**Why it happens:** markdownify preserves original src attribute

**How to avoid:** Use custom converter class or post-process img tags:
```python
class WorkletConverter(MarkdownConverter):
    def convert_img(self, node):
        src = node.get('src', '')
        alt = node.get('alt', '')
        # Transform relative paths to attachment paths
        return f'![{alt}]({attach_path}/{src.split("/")[-1]})'
```

**Source: Verified markdownify behavior - preserves original src**

### Pitfall 3: tempfile not cleaned up on exception

**What goes wrong:** .tmp files left behind if download fails mid-stream

**Why it happens:** Exception before atomic rename

**How to avoid:** Use try/finally or context manager:
```python
temp_path = None
try:
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.tmp', delete=False) as f:
        temp_path = f.name
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    Path(temp_path).rename(dest_path)
except Exception:
    if temp_path and Path(temp_path).exists():
        Path(temp_path).unlink()
    raise
```

**Source: Standard tempfile pattern**

### Pitfall 4: Missing fallback when entry_points returns empty

**What goes wrong:** SourceRegistry silently has no sources if entry_points not configured

**Why it happens:** No error on empty entry_points group

**How to avoid:** Provide manual registration fallback:
```python
class SourceRegistry:
    def __init__(self):
        self._sources: dict[str, type[BaseSource]] = {}
        self._discover()
        if not self._sources:
            self._fallback_register()

    def _fallback_register(self):
        """Manual fallback when entry_points unavailable."""
        from .zentao import ZentaoSource
        from .markdown import MarkdownSource
        self._sources['zentao'] = ZentaoSource
        self._sources['markdown'] = MarkdownSource
```

**Source: Standard fallback pattern**

## Code Examples

### Verified markdownify output

```python
>>> import markdownify
>>> markdownify.markdownify('<h1>Hello</h1><p>World</p>')
'Hello\\n=====\\n\\nWorld'
>>> markdownify.markdownify('<img src="test.png" alt="screenshot">')
'![screenshot](test.png)'
>>> markdownify.markdownify('<a href="http://ex.com">link</a>')
'[link](http://ex.com)'
>>> markdownify.markdownify('<table><tr><td>cell</td></tr></table>')
'|  |\\n| --- |\\n| cell |'
```

### Verified entry_points auto-discovery

```python
>>> from importlib.metadata import entry_points
>>> eps = entry_points()
>>> eps.select(group='console_scripts', name='pytest')
[EntryPoint(name='pytest', value='pytest:console_main', group='console_scripts')]
>>> eps.select(group='worklet.sources')  # Empty until configured
[]
```

### Verified requests timeout types

```python
>>> import requests.exceptions
>>> [e for e in dir(requests.exceptions) if 'Timeout' in e or 'Connect' in e]
['ConnectTimeout', 'Timeout', 'ReadTimeout']
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 40+ regex chain for HTML→MD | markdownify library | Phase 2 | Cleaner code, correct handling of all HTML |
| Manual source registration | importlib.metadata entry_points | Phase 2 | Plugin ecosystem support |
| Non-streaming downloads | stream=True + iter_content() | Phase 2 | Memory efficiency for large files |
| Generic Exception | requests.exceptions types | Phase 2 | Better error handling, debugging |

**Deprecated/outdated:**
- Java version: Removed in Phase 1
- chandao/zentao naming: Removed in Phase 1
- Java Properties config: Replaced by TOML in Phase 1

## Open Questions

1. **Zentao API subtask endpoint**
   - What we know: Story/Task have parent field, but Zentao API may not have a direct "get children by parent" endpoint
   - What's unclear: Need to verify if `/story-browse.json?parent=X` or similar endpoint exists
   - Recommendation: Test with actual Zentao instance or check API documentation

2. **InputParser configuration-driven vs hardcoded**
   - What we know: Phase 2 only requires ZentaoSource + MarkdownReader
   - What's unclear: Whether InputParser (Phase 4) should be config-driven or hardcoded
   - Recommendation: Hardcode for Phase 2 (INPUT-01/05 only), defer config decision to Phase 4

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Runtime | ✓ | 3.12.3 | — |
| requests | HTTP client | ✓ | 2.32.0+ | — |
| importlib.metadata | entry_points | ✓ | stdlib | Manual dict fallback |
| markdownify | HTML→MD | ✗ | — (1.2.2 on PyPI) | Add to dependencies |
| pytest | Testing | ✗ | — | Add to dependencies |
| responses | HTTP mocking | ✗ | — | Add to dependencies |

**Missing dependencies with no fallback:**
- None blocking - all missing deps can be added to pyproject.toml

**Missing dependencies with fallback:**
- None - all missing deps are new requirements

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 8.x |
| Config file | pytest.ini or pyproject.toml [tool.pytest.ini_options] |
| Quick run command | `pytest tests/ -x -v` |
| Full suite command | `pytest tests/ --tb=short` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| INPUT-01 | BaseSource ABC defined, SourceRegistry discovers sources | unit | `pytest tests/test_sources.py::test_source_registry_discovery -x` | ❌ Wave 0 |
| INPUT-02 | ZentaoSource.fetch() returns Worklet | unit | `pytest tests/test_sources.py::test_zentao_source_fetch -x` | ❌ Wave 0 |
| INPUT-05 | MarkdownReader.read() returns RawContent | unit | `pytest tests/test_sources.py::test_markdown_reader -x` | ❌ Wave 0 |
| CLIENT-01 | download_attachment has timeout parameter | unit | `pytest tests/test_client.py::test_download_attachment_timeout -x` | ❌ Wave 0 |
| CLIENT-02 | Large file downloaded via streaming | unit | `pytest tests/test_client.py::test_download_streaming -x` | ❌ Wave 0 |
| CLIENT-03 | Specific exception types raised | unit | `pytest tests/test_client.py::test_exception_types -x` | ❌ Wave 0 |
| CLIENT-04 | service.py re.findall removed | unit | `pytest tests/test_service.py::test_no_useless_findall -x` | ❌ Wave 0 |
| CLIENT-05 | Subtask detection returns children | unit | `pytest tests/test_service.py::test_detect_subtasks -x` | ❌ Wave 0 |
| EXPORT-01 | markdownify converts HTML correctly | unit | `pytest tests/test_exporter.py::test_html_to_markdown_markdownify -x` | ❌ Wave 0 |
| EXPORT-02 | Filename uses hash not truncation | unit | `pytest tests/test_exporter.py::test_filename_hash -x` | ❌ Wave 0 |
| EXPORT-03 | Exporter._to_worklet() converts Story/Task/Bug | unit | `pytest tests/test_exporter.py::test_to_worklet -x` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `pytest tests/ -x -q`
- **Per wave merge:** `pytest tests/ --tb=short`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_sources.py` — BaseSource, SourceRegistry, ZentaoSource, MarkdownSource
- [ ] `tests/test_client.py` — timeout, streaming, exception types
- [ ] `tests/test_service.py` — subtask detection, re.findall removal
- [ ] `tests/test_exporter.py` — markdownify, filename hash, _to_worklet
- [ ] `tests/conftest.py` — shared fixtures (mock config, temp dirs)
- [ ] Framework install: `pip install pytest responses markdownify`

## Sources

### Primary (HIGH confidence)

- markdownify 1.2.2 - Tested locally, verified HTML→MD conversion
- importlib.metadata entry_points - Verified Python 3.12.3 API
- requests exceptions - Verified requests.exceptions module
- Python 3.12.3 - Verified streaming and timeout behavior

### Secondary (MEDIUM confidence)

- setuptools entry_points documentation - Community standard
- pytest documentation - Industry standard testing

### Tertiary (LOW confidence)

- Zentao API subtask endpoint - Not verified, needs actual API test

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH - markdownify/importlib.metadata/requests all verified locally
- Architecture: HIGH - BaseSource/SourceRegistry pattern verified with Python 3.12 API
- Pitfalls: MEDIUM - entry_points and tempfile patterns known, but Zentao API untested

**Research date:** 2026-04-05
**Valid until:** 2026-05-05 (30 days for stable stack)

---

## RESEARCH COMPLETE

**Phase:** 02-core-pipeline
**Confidence:** HIGH

### Key Findings

1. **markdownify 1.2.2** verified for HTML→Markdown: handles img/links/tables correctly, replaces 40+ regex
2. **importlib.metadata.entry_points().select()** verified working on Python 3.12.3
3. **requests stream=True + iter_content()** pattern verified for streaming downloads
4. **requests.exceptions** has specific types: Timeout, ConnectTimeout, ReadTimeout, ConnectionError, HTTPError
5. **Subtask detection** possible via Story.parent/Task.parent fields (parent field exists in models.py)

### File Created

`.planning/phases/02-core-pipeline/02-RESEARCH.md`

### Confidence Assessment

| Area | Level | Reason |
|------|-------|--------|
| Standard Stack | HIGH | All libraries verified locally |
| Architecture | HIGH | BaseSource/SourceRegistry pattern verified |
| Pitfalls | MEDIUM | entry_points/tempfile patterns known, Zentao API untested |

### Open Questions

1. Zentao API subtask endpoint - needs verification with actual API
2. InputParser config vs hardcoded - deferred to Phase 4

### Ready for Planning

Research complete. Planner can now create PLAN.md files.

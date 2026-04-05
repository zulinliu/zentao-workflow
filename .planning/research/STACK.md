# Technology Stack

**Project:** Worklet (v2.0.0)
**Researched:** 2026-04-04 (updated)

## Critical Decision: Python Version Floor

**Recommendation: Python >= 3.10**

The PROJECT.md states "Python 3.6+" as a constraint citing "enterprise environments." This constraint is outdated and harmful:

- Python 3.6 reached EOL in December 2021, 3.7 in June 2023, 3.8 in October 2024, 3.9 in October 2025
- `requests` 2.33.x (March 2026) dropped Python 3.9, now requires 3.10+
- `python-docx` 1.2.0 requires Python >= 3.9
- `markitdown` requires Python >= 3.10
- RHEL 9 standardizes on Python 3.9 as its default; RHEL 8 Python 3.9 support ended November 2025
- Every major tool (pip, setuptools, black, mypy) already requires 3.9+

Since v2.0 is a major version with no backward compatibility promised, this is the right time to raise the floor. **Python 3.10** is the pragmatic choice: it is the oldest version still receiving security patches, and it unlocks modern syntax (match/case, union types via `|`, ParamSpec).

**Confidence: HIGH** -- Based on official Python lifecycle data and verified PyPI version requirements.

## Recommended Stack

### Core Runtime

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Python | >= 3.10 | Runtime | Oldest supported version; matches `requests` 2.33.x and `markitdown` requirements |

### HTTP Client

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| requests | >= 2.32.0 | HTTP client for Zentao API | Already in use, battle-tested, sufficient for sync API calls. The project does not need async HTTP -- it makes sequential API calls to a single Zentao server. |

**Confidence: HIGH** -- `requests` is already the project dependency; no reason to change.

**Why NOT httpx:** httpx's async capability is unnecessary since Zentao API calls are sequential per-item. The PROJECT.md fix items (download timeout, streaming large files) are achievable with `requests` via `stream=True` and explicit `timeout=` parameters. Adding httpx means a new dependency and session management patterns for zero practical gain.

### Document Format Parsers -- Two Viable Approaches

**Decision required: Unified (MarkItDown) vs Modular (pdfplumber + python-docx)?**

Both approaches are technically sound. Here is the comparison:

#### Option A: Microsoft MarkItDown (Recommended)

| Library | Version | Purpose | Why | Confidence |
|---------|---------|---------|-----|------------|
| markitdown[docx,pdf] | >= 0.1.5 | Read PDF, DOCX, PPTX, HTML, images | Single library handles ALL document formats. MIT licensed, 91K GitHub stars, maintained by Microsoft Research. Requires Python 3.10+. Uses pdfminer.six and mammoth internally. | MEDIUM-HIGH |

**Strengths:**
- One dependency replaces 2-3 separate libraries (python-docx, pdfplumber, html-to-markdown)
- Unified API: `markitdown.convert("file.pdf")` works for any supported format
- Output is optimized for LLM consumption (designed for RAG/LLM pipelines)
- Plugin architecture for OCR if needed later
- MCP server integration available
- MIT licensed, no AGPL concerns

**Weaknesses:**
- Still v0.1.5 (pre-1.0, API may change)
- Table extraction quality may be weaker than pdfplumber (uses pdfminer.six, not pdfplumber)
- Newer library, less battle-tested for edge cases
- Optional extras require specifying `markitdown[docx,pdf]` for needed format support

#### Option B: Modular Stack (pdfplumber + python-docx)

| Library | Version | Purpose | Why | Confidence |
|---------|---------|---------|-----|------------|
| python-docx | >= 1.2.0 | Read .docx files | MIT, production-stable (v1.2.0), 1.85K GitHub stars. De facto standard. | HIGH |
| pdfplumber | >= 0.11.9 | Read PDF files | BSD, best table extraction. Depends on pdfminer.six + Pillow + pypdfium2. | HIGH |
| markdownify | >= 0.14.1 | Convert HTML to Markdown | MIT, replaces 40+ regex chain. Built on BeautifulSoup4. | HIGH |

**Strengths:**
- All libraries are production-stable (>= v1.0)
- pdfplumber has the best table extraction of any Python PDF library
- More granular control over each format
- Battle-tested for years

**Weaknesses:**
- Three dependencies instead of one
- ~45MB total footprint (Pillow is the heaviest)
- More code to write (separate reader per format)

#### Recommendation

**Use MarkItDown as the primary approach, with fallback clarity.**

Rationale:
1. It aligns with the "lightweight, minimal dependencies" constraint in PROJECT.md
2. One `pip install markitdown[docx,pdf]` replaces 3 separate installs
3. Its LLM-optimized output is exactly what this Skill needs (content goes to Claude for plan generation)
4. Microsoft maintains it actively (91K stars, 304 commits)
5. If table extraction proves insufficient for specific use cases, individual readers (pdfplumber) can be added later as optional enhancements

**Risk:** MarkItDown is pre-1.0 (v0.1.5). If its API breaks in a future release, the reader abstraction layer (see ARCHITECTURE.md) isolates the impact to a single module.

**Confidence: MEDIUM-HIGH** -- Strong library with active maintenance, but pre-1.0 version warrants monitoring.

### HTML-to-Markdown Conversion (for Zentao API responses)

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| markdownify | >= 0.14.1 | Replace 40+ regex chain in exporter.py | Even if MarkItDown is used for document parsing, Zentao API returns raw HTML that needs conversion. markdownify handles this cleanly with custom converter subclassing. |

Note: MarkItDown can also convert HTML, but markdownify's custom converter API (subclass `MarkdownConverter`, override `convert_img()`) is better suited for Zentao-specific HTML patterns (inline images with custom src paths).

**Confidence: HIGH** -- markdownify is production-stable, MIT licensed.

**Why NOT html.parser (stdlib):** PROJECT.md suggests this, but html.parser only parses HTML -- it does not convert to Markdown. You would still need to write conversion logic, recreating what markdownify already does. Using html.parser directly means building your own converter, which is exactly the fragile pattern the project wants to eliminate (see the 40+ regex chain in current exporter.py).

### Why NOT These Libraries

| Category | Rejected | Why Not |
|----------|----------|---------|
| PDF | PyMuPDF / pymupdf4llm | **AGPL-3.0 license** -- viral copyleft requires open-sourcing any application that uses it, or purchasing a commercial license from Artifex. Users embed this Skill in proprietary workflows. AGPL is a dealbreaker. |
| PDF | pypdf | Pure Python, fast (0.024s), BSD licensed, but weaker text extraction quality than pdfplumber/markitdown for complex layouts and tables. |
| PDF | PyPDF2 | Deprecated. Merged into `pypdf`. Do not use. |
| Document | Docling (IBM) | Heavy ML models (~1GB+). Overkill for a CLI Skill. |
| Document | Marker | Requires GPU for speed. GPL licensed. |
| DOCX | docx-parser | Wrapper around python-docx with less community. |
| HTML | html-to-markdown | Modern markdownify fork, but smaller community. markdownify is sufficient. |
| HTML | html.parser (stdlib) | Only parses HTML, does not convert. Would recreate the regex chain problem. |
| OCR | pytesseract | Requires Tesseract system binary. Not pip-only. |
| OCR | EasyOCR | Pulls PyTorch (~2GB). |
| OCR | PaddleOCR | Pulls PaddlePaddle framework. |

### OCR / Image Text Extraction

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| (None -- defer to Claude vision) | N/A | Image reading | See rationale below | MEDIUM |

**Rationale:** For a Claude Code Skill, images should be passed to Claude's multimodal vision rather than processed by a Python OCR library. The Skill copies image files to the workspace and references them; Claude reads them natively. If OCR is later required, MarkItDown's `markitdown-ocr` plugin (uses LLM Vision, no ML library dependencies) is the lightest option.

### File Reading Pipeline (New in v2.0)

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pathlib (stdlib) | built-in | File path handling | Already used. Cross-platform. |
| mimetypes (stdlib) | built-in | File type detection | No external dependency needed. |

### Configuration & Environment

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pathlib (stdlib) | built-in | Config directory management | Already used in config.py. |
| json (stdlib) | built-in | Cache file format | For `.worklet/env-cache.json`. Simpler than properties for structured data. |

**Why NOT xdg-base-dirs:** The project uses `.worklet/` in project root or `~/.worklet/`. This is project-specific, not XDG-compliant, and deliberately so -- per-workspace config discovery is required.

### Testing

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pytest | >= 8.0 | Test runner | Industry standard. Fixture system for test setup. |
| pytest-cov | >= 5.0 | Coverage reporting | Integrates with pytest. |

**Confidence: HIGH** -- Standard choices.

### Development Tools

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| ruff | >= 0.9.0 | Linting + formatting | Replaces flake8 + black + isort in a single Rust-based tool. 10-100x faster. The standard for new Python projects in 2025+. |

**Confidence: HIGH** -- ruff has become the dominant Python linter/formatter.

## SKILL.md Structure Recommendations

Based on Anthropic's official Skill authoring best practices (verified from platform.claude.com):

| Guideline | Current State | Recommendation |
|-----------|---------------|----------------|
| SKILL.md body < 500 lines | Current: 625 lines | Split into SKILL.md (overview) + reference files |
| Name: lowercase-hyphens | `zentao-workflow` | `worklet` |
| Description: third person, < 1024 chars | 40+ lines (~1,200 chars) | Under 250 chars, imperative language, English-first |
| Progressive disclosure | Everything in one file | Move guides to `references/` directory |
| One-level-deep references | N/A (single file) | SKILL.md -> reference files (no nesting) |
| Variable syntax | `{SKILL_DIR}` (wrong) | `${CLAUDE_SKILL_DIR}` (official) |

**Confidence: HIGH** -- Directly from Anthropic's official documentation.

### Recommended SKILL.md Frontmatter

```yaml
---
name: worklet
description: |
  Development workflow assistant. ALWAYS invoke when user wants to develop a
  requirement, fix a bug, or implement a feature from any source (zentao, file,
  folder). Generates technical implementation plans with superpowers.
  Triggers: develop, implement, fix, build, requirement, task, bug, story,
  zentao, chandao, tech plan. Do not start coding directly -- use this first.
---
```

## Full Dependency List

### Runtime Dependencies (MarkItDown approach)

```
# requirements.txt
requests>=2.32.0
markitdown[docx,pdf]>=0.1.5
markdownify>=0.14.1
```

### Runtime Dependencies (Modular approach -- alternative)

```
# requirements.txt
requests>=2.32.0
python-docx>=1.2.0
pdfplumber>=0.11.9
markdownify>=0.14.1
```

### Dev Dependencies

```
# requirements-dev.txt
pytest>=8.0
pytest-cov>=5.0
ruff>=0.9.0
```

### Installation

```bash
# MarkItDown approach (recommended)
pip install requests 'markitdown[docx,pdf]' markdownify

# Modular approach (alternative)
pip install requests python-docx pdfplumber markdownify

# Dev
pip install pytest pytest-cov ruff
```

### Dependency Weight Analysis

| Approach | Packages | Approximate Size | License |
|----------|----------|------------------|---------|
| MarkItDown | requests, markitdown, markdownify | ~15MB | Apache-2.0, MIT, MIT |
| Modular | requests, python-docx, pdfplumber, markdownify | ~45MB | Apache-2.0, MIT, BSD, MIT |

MarkItDown is lighter because it does not pull Pillow or pypdfium2.

## Migration Path from v1.x

| Current (v1.x) | v2.0 | Migration Notes |
|-----------------|------|-----------------|
| Python 3.6+ | Python 3.10+ | Breaking change. Document in CHANGELOG. |
| requests only | requests + markitdown + markdownify | New deps for multi-format support |
| 40+ regex HTML->MD | markdownify library | Drop exporter.py regex chain entirely |
| Java + Python dual runtime | Python only | Delete all Java artifacts |
| `.chandao/` config dir | `.worklet/` config dir | New directory, one-time migration prompt |
| `chandao_fetch` package | `worklet` package | Full rename |

## Sources

- [Microsoft MarkItDown (GitHub)](https://github.com/microsoft/markitdown) -- v0.1.5, 91K stars, MIT
- [MarkItDown PyPI](https://pypi.org/project/markitdown/) -- Python >= 3.10, optional extras
- [MarkItDown Guide (Real Python)](https://realpython.com/python-markitdown/)
- [python-docx PyPI](https://pypi.org/project/python-docx/) -- v1.2.0, Python >= 3.9, MIT
- [pdfplumber PyPI](https://pypi.org/project/pdfplumber/) -- v0.11.9, Python >= 3.8, BSD
- [markdownify PyPI](https://pypi.org/project/markdownify/) -- v1.2.2, MIT
- [pypdf PyPI](https://pypi.org/project/pypdf/) -- v6.9.2, BSD (considered, not primary recommendation)
- [PyMuPDF AGPL Discussion](https://github.com/pymupdf/PyMuPDF/discussions/971) -- License concern
- [requests PyPI](https://pypi.org/project/requests/) -- v2.33.1, Apache-2.0
- [HTTPX Documentation](https://www.python-httpx.org/) -- Evaluated, not needed
- [Python Version Status](https://devguide.python.org/versions/)
- [Python 3.9 EOL (Red Hat)](https://developers.redhat.com/articles/2025/12/04/python-39-reaches-end-life-what-it-means-rhel-users)
- [Claude Code Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Code Skills Overview](https://code.claude.com/docs/en/skills)
- [PDF Extractors Comparison 2025](https://dev.to/onlyoneaman/i-tested-7-python-pdf-extractors-so-you-dont-have-to-2025-edition-akm)
- [html-to-markdown PyPI](https://pypi.org/project/html-to-markdown/)
- [HTTPX vs Requests Comparison](https://www.morethanmonkeys.co.uk/article/comparing-requests-and-httpx-in-python-which-http-client-should-you-use-in-2025/)

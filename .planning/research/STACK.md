# Technology Stack

**Project:** Worklet (v2.0.0)
**Researched:** 2026-04-04

## Critical Decision: Python Version Floor

**Recommendation: Python >= 3.10**

The PROJECT.md states "Python 3.6+" as a constraint citing "enterprise environments." This constraint is outdated and harmful:

- Python 3.6 reached EOL in December 2021, 3.7 in June 2023, 3.8 in October 2024, 3.9 in October 2025
- `requests` 2.33.x (March 2026) dropped Python 3.9, now requires 3.10+
- `python-docx` 1.2.0 requires Python >= 3.9
- `pdfplumber` requires Python >= 3.8
- RHEL 9 standardizes on Python 3.9 as its default; RHEL 8 Python 3.9 support ended November 2025
- Every major tool (pip, setuptools, black, mypy) already requires 3.9+

Since v2.0 is a major version with no backward compatibility promised, this is the right time to raise the floor. **Python 3.10** is the pragmatic choice: it is the oldest version still receiving security patches, and it unlocks modern syntax (match/case, union types via `|`, ParamSpec).

**Confidence: HIGH** -- Based on official Python lifecycle data and verified PyPI version requirements.

## Recommended Stack

### Core Runtime

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Python | >= 3.10 | Runtime | Oldest supported version; matches `requests` 2.33.x requirement |

### HTTP Client

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| requests | >= 2.32.0 | HTTP client for Zentao API | Already in use, battle-tested, sufficient for sync API calls. The project does not need async HTTP -- it makes sequential API calls to a single Zentao server. Switching to httpx adds complexity without benefit here. |

**Confidence: HIGH** -- `requests` is already the project dependency; no reason to change for this use case.

**Why NOT httpx:** The PROJECT.md lists a fix for "download timeout" and "streaming large file download" in client.py. Both are achievable with `requests` via `stream=True` and explicit `timeout=` parameters. httpx's async capability is unnecessary since Zentao API calls are sequential per-item. Adding httpx means a new dependency, new session management patterns, and a learning curve -- all for zero practical gain.

### Document Format Parsers

| Library | Version | Purpose | Why | Confidence |
|---------|---------|---------|-----|------------|
| python-docx | >= 1.2.0 | Read .docx files | MIT licensed, production-stable, pure Python + lxml. The de facto standard with 1.85K GitHub stars, 644 dependent packages. Reads paragraphs, tables, and images. No alternatives come close in maturity. | HIGH |
| pdfplumber | >= 0.11.9 | Read PDF files, extract text and tables | BSD licensed, pure Python, lightweight (depends on pdfminer.six + Pillow + pypdfium2). Best table extraction of any Python PDF library. Text extraction is reliable for structured documents (which requirement docs typically are). | HIGH |
| markdownify | >= 0.14.1 | Convert HTML to Markdown | MIT licensed, replaces the fragile 40+ regex chain in current exporter.py. Handles headings, lists, tables, links, images, code blocks. Supports custom converters via subclassing for project-specific needs. | HIGH |

**Confidence: HIGH for all three** -- Versions verified on PyPI, all actively maintained, all permissively licensed.

### Why NOT These Alternatives

| Category | Rejected | Why Not |
|----------|----------|---------|
| PDF | PyMuPDF / pymupdf4llm | **AGPL-3.0 license** -- viral copyleft requires open-sourcing any application that uses it, or purchasing a commercial license from Artifex. This is a Skill distributed via GitHub; users embed it in proprietary workflows. AGPL is a dealbreaker. |
| PDF | pypdf | Pure Python, fast (0.024s), BSD licensed, but text extraction quality is weaker than pdfplumber for complex layouts and tables. Requirement docs often contain tables. |
| PDF | PyPDF2 | Deprecated. Merged into `pypdf`. Do not use. |
| DOCX | docx-parser | Wrapper around python-docx with less community adoption. No added value for read-only use cases. |
| DOCX | python-docx-ml6 | Fork with unmerged features. Unstable API surface. |
| HTML->MD | html-to-markdown | Modern fork of markdownify, but requires Python 3.9+ and has smaller community. markdownify is sufficient and more battle-tested. |
| HTML->MD | html.parser (stdlib) | PROJECT.md suggests this. The stdlib html.parser only parses HTML -- it does not convert to Markdown. You would still need to write conversion logic, recreating what markdownify already does. Using html.parser directly means building and maintaining your own converter, which is exactly the fragile pattern the project wants to eliminate. |

### OCR / Image Text Extraction

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| (None -- defer) | N/A | Image OCR | See rationale below | MEDIUM |

**Rationale for deferring OCR:** The PROJECT.md lists "images" as an input format. However, for a Claude Code Skill, the most practical approach is:

1. Claude itself has vision capabilities -- it can read images directly when they are referenced in the Skill workflow
2. The Skill can copy image files to the workspace and reference them in the tech plan, letting Claude's multimodal model interpret them
3. Adding OCR dependencies (pytesseract requires Tesseract binary install; EasyOCR pulls PyTorch ~2GB; PaddleOCR pulls PaddlePaddle) massively inflates the Skill footprint

**If OCR is later required**, the lightest option is:
- `pytesseract` >= 0.3.13 + system Tesseract binary -- but this is a system-level install, not pip-only
- Consider this a separate future milestone, not v2.0 scope

**Confidence: MEDIUM** -- This is an architectural recommendation, not a verified library choice. Depends on whether Claude's vision is sufficient for the project's image use cases.

### HTML Parsing (for Zentao API responses)

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| markdownify | >= 0.14.1 | Replace 40+ regex chain in exporter.py | Single dependency handles all HTML-to-Markdown needs. Built on BeautifulSoup4, which handles malformed HTML gracefully. Custom converter subclass can handle Zentao-specific patterns (e.g., inline images). |

Note: `markdownify` depends on `beautifulsoup4`, which will be installed automatically. This is an acceptable transitive dependency -- it is widely used, pure Python, and MIT licensed.

### File Reading Pipeline (New in v2.0)

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pathlib (stdlib) | built-in | File path handling | Already used in the project. Cross-platform, clean API. |
| mimetypes (stdlib) | built-in | File type detection by extension | No external dependency needed for basic MIME type detection. |

### Configuration & Environment

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pathlib (stdlib) | built-in | Config directory management | Current config.py already uses pathlib. Sufficient for `.worklet/` directory management. |
| json (stdlib) | built-in | Cache file format | For environment detection cache (`.worklet/env-cache.json`). Simpler than properties format for structured data. |

**Why NOT xdg-base-dirs:** The project uses a custom config directory pattern (`.worklet/` in project root or `~/.worklet/`). This is project-specific, not XDG-compliant, and deliberately so -- the Skill needs per-workspace config discovery. Adding xdg-base-dirs would conflict with this design.

### Testing

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pytest | >= 8.0 | Test runner | Industry standard, better output than unittest, fixture system for test setup. |
| pytest-cov | >= 5.0 | Coverage reporting | Integrates with pytest. |

**Confidence: HIGH** -- Standard choices, no controversy.

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
| Name: lowercase-hyphens, gerund | `zentao-workflow` | `processing-worklets` or `worklet` |
| Description: third person, < 1024 chars | First person mixed | Rewrite in third person with trigger keywords |
| Progressive disclosure | Everything in one file | Move guides to `references/` directory |
| One-level-deep references | N/A (single file) | SKILL.md -> reference files (no nesting) |

**Confidence: HIGH** -- Directly from Anthropic's official documentation.

### Recommended SKILL.md Frontmatter

```yaml
---
name: worklet
description: |
  Reads development requirements from multiple sources (Zentao API, local
  Markdown/PDF/Word/image files) and generates technical implementation plans.
  Integrates with superpowers skills for brainstorming and code execution.

  Use when: user mentions requirements, stories, tasks, bugs, development
  plans, technical design, or provides requirement documents. Also triggers
  on Zentao-related keywords (zentao, chandao) or file paths pointing to
  requirement documents (.md, .pdf, .docx).
---
```

## Full Dependency List

### Runtime Dependencies

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
# Core
pip install requests python-docx pdfplumber markdownify

# Dev
pip install -D pytest pytest-cov ruff
```

### Dependency Weight Analysis

| Package | Transitive Deps | Approximate Size | License |
|---------|-----------------|------------------|---------|
| requests | urllib3, certifi, charset-normalizer, idna | ~2MB | Apache-2.0 |
| python-docx | lxml | ~15MB (lxml is C-compiled) | MIT |
| pdfplumber | pdfminer.six, Pillow, pypdfium2 | ~25MB (Pillow + pypdfium2) | MIT/BSD |
| markdownify | beautifulsoup4, six | ~3MB | MIT |
| **Total** | | **~45MB** | All permissive |

This is reasonable for a CLI tool with document parsing capabilities. The heaviest component is Pillow (image handling for PDF), which is also widely pre-installed.

## Migration Path from v1.x

| Current (v1.x) | v2.0 | Migration Notes |
|-----------------|------|-----------------|
| Python 3.6+ | Python 3.10+ | Breaking change. Document in CHANGELOG. |
| requests only | requests + python-docx + pdfplumber + markdownify | New dependencies for multi-format support |
| 40+ regex HTML->MD | markdownify library | Drop exporter.py regex chain entirely |
| Java + Python dual runtime | Python only | Delete all Java artifacts |
| `.chandao/` config dir | `.worklet/` config dir | New directory, no migration |
| `chandao_fetch` package | `worklet` package | Full rename |

## Sources

- [python-docx PyPI](https://pypi.org/project/python-docx/) -- Version 1.2.0, Python >= 3.9, MIT
- [pdfplumber PyPI](https://pypi.org/project/pdfplumber/) -- Version 0.11.9, Python >= 3.8, MIT
- [markdownify PyPI](https://pypi.org/project/markdownify/) -- Version 1.2.2, MIT
- [pypdf PyPI](https://pypi.org/project/pypdf/) -- Version 6.9.2, BSD (considered but not recommended)
- [PyMuPDF AGPL Discussion](https://github.com/pymupdf/PyMuPDF/discussions/971) -- License concern documentation
- [pymupdf4llm Docs](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/) -- AGPL, not suitable
- [requests PyPI](https://pypi.org/project/requests/) -- Version 2.33.1, Apache-2.0
- [HTTPX Documentation](https://www.python-httpx.org/) -- Evaluated, not needed
- [Python Version Status](https://devguide.python.org/versions/) -- EOL timeline
- [Python 3.9 EOL (Red Hat)](https://developers.redhat.com/articles/2025/12/04/python-39-reaches-end-life-what-it-means-rhel-users)
- [Claude Code Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Code Skills Overview](https://code.claude.com/docs/en/skills)
- [PDF Extractors Comparison 2025](https://dev.to/onlyoneaman/i-tested-7-python-pdf-extractors-so-you-dont-have-to-2025-edition-akm)
- [html-to-markdown PyPI](https://pypi.org/project/html-to-markdown/)
- [xdg-base-dirs](https://github.com/srstevenson/xdg-base-dirs) -- Evaluated, not needed

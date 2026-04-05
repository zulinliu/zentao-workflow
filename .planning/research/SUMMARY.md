# Project Research Summary

**Project:** Worklet (v2.0.0) -- refactored from zentao-workflow
**Domain:** CLI developer workflow tool / Claude Code Skill
**Researched:** 2026-04-04 (updated with stack research)
**Confidence:** HIGH

## Executive Summary

Worklet v2.0 is a major refactoring of a Claude Code Skill that currently fetches requirements exclusively from the Zentao project management API. The v2.0 goal is to transform it into a multi-source tool that also reads local Markdown, PDF, and Word documents, while simultaneously shedding the Java dual-runtime, raising the Python version floor, and rewriting the Skill's surface area to meet current Claude Code platform standards.

The stack research identified four critical decisions:

**Python >= 3.10 is the correct minimum version.** The current 3.6+ claim is already violated by the codebase (uses dataclasses, requires 3.7+) and is incompatible with every recommended library: `requests` 2.33.x requires 3.10+, `python-docx` 1.2.0 requires 3.9+, and `markitdown` requires 3.10+. Since v2.0 is a major version with no backward compatibility, raising the floor is both safe and necessary.

**Microsoft MarkItDown is the recommended unified document parser.** It handles PDF, DOCX, PPTX, HTML, and images in a single MIT-licensed package (91K GitHub stars, maintained by Microsoft Research). It is lighter (~15MB) than a modular stack of pdfplumber + python-docx (~45MB). Its pre-1.0 status (v0.1.5) is the main risk, mitigated by the reader abstraction layer in the architecture. An alternative modular stack (pdfplumber for tables, python-docx for Word) remains viable if MarkItDown proves insufficient.

**markdownify replaces the 40+ regex HTML-to-Markdown chain** in exporter.py. Zentao API responses return raw HTML. markdownify (MIT, built on BeautifulSoup) handles this cleanly with custom converter subclassing. The PROJECT.md suggestion of stdlib html.parser would recreate the fragile hand-written converter problem.

**OCR is deferred to Claude's multimodal vision.** Images are passed to Claude rather than processed by Python OCR libraries. This avoids pytesseract (system binary) and EasyOCR (2GB PyTorch). MarkItDown's OCR plugin is available as an optional later enhancement.

## Key Findings

### Recommended Stack

**Core technologies:**
- Python >= 3.10: runtime -- oldest version still receiving security patches
- requests >= 2.32.0: Zentao API HTTP client -- already in use, sufficient
- markitdown[docx,pdf] >= 0.1.5: unified document parser -- PDF, DOCX, PPTX, HTML, images (MIT)
- markdownify >= 0.14.1: HTML-to-Markdown for Zentao API responses -- replaces 40+ regex chain (MIT)
- pytest >= 8.0 + ruff >= 0.9.0: testing and linting

**Alternative modular stack (if MarkItDown insufficient):**
- python-docx >= 1.2.0 (MIT) + pdfplumber >= 0.11.9 (BSD) -- heavier but more mature

**Note on PDF library decision:** STACK.md recommends MarkItDown as primary with pdfplumber as fallback. The FEATURES.md researcher also independently recommended MarkItDown. If MarkItDown's table extraction proves insufficient for requirement documents with complex tables, pdfplumber can be swapped in at the reader layer without affecting the rest of the pipeline.

### Architecture Approach

Source-Normalize-Export pipeline with ABC-based plugin registry. `BaseSource` defines a `fetch()` interface; concrete subclasses (`ZentaoSource`, `FileSource`, `FolderSource`) return a `RawContent` dataclass. A `Normalizer` converts to a unified `Worklet` model. The `Exporter` writes Markdown. Format-specific readers use lazy imports so users who only use Zentao are not required to install document parsing libraries.

### Critical Pitfalls (Top 5)

1. **PyMuPDF AGPL license** -- Appears in every "best PDF library" article but is a license trap. Use MarkItDown or pdfplumber (both MIT/BSD) instead.
2. **SKILL.md description over 250 chars** -- Descriptions are truncated in skill listings; multiline YAML triggers a known discovery bug. Keep under 250 chars, single line, imperative language.
3. **Wrong variable syntax** -- Current `{SKILL_DIR}` must become `${CLAUDE_SKILL_DIR}`.
4. **Incomplete rename** -- chandao/zentao references scattered across 10+ files. Grep-based verification after each phase is mandatory.
5. **Python 3.6 false claim** -- Already broken by dataclass usage. Set >= 3.10 before writing any new code.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Foundation and Rename
**Rationale:** Every subsequent change depends on correct naming and stable data model shapes.
**Delivers:** Renamed `worklet` package; data models; `WorkletConfig`; ABCs; Java removal; Python 3.10+ floor.
**Avoids:** Pitfall 3 (orphan references), Pitfall 4 (Java refs), Pitfall 7 (Python version), Pitfall 13 (credential leak)

### Phase 2: Core Pipeline -- Zentao + Markdown
**Rationale:** Validate the BaseSource ABC against the already-working Zentao use case.
**Delivers:** End-to-end pipeline for Zentao IDs and local .md files. markdownify-based exporter. Streaming download fix.
**Avoids:** Pitfall 9 (HTML converter rewrite -- test corpus first), Pitfall 11 (streaming partial files)

### Phase 3: Extended File Sources
**Rationale:** PDF, DOCX, and image support are net-new. Separate phase = clean rollback point.
**Delivers:** PdfReader, DocxReader, ImageReader via MarkItDown (lazy import). FolderSource.
**Avoids:** Pitfall 6 (AGPL contamination), Pitfall 14 (dependency bloat)

### Phase 4: Pipeline Assembly and CLI
**Rationale:** CLI auto-detection depends on knowing each source's can_handle() implementation.
**Delivers:** InputParser, environment detection with caching, superpowers detection.
**Avoids:** Pitfall 12 (stale env cache), Pitfall 16 (superpowers detection path)

### Phase 5: SKILL.md Rewrite and Release
**Rationale:** SKILL.md reflects final code behavior. Write it last.
**Delivers:** Rewritten SKILL.md with ${CLAUDE_SKILL_DIR}, sub-250-char description, progressive disclosure. Updated release.yml. GitHub repo rename.
**Avoids:** Pitfall 1 (variable syntax), Pitfall 2 (description length), Pitfall 8 (CI breakage), Pitfall 10 (over-triggering)

### Phase Ordering Rationale
- Rename first: all paths, keys, imports depend on it
- Models before sources: data shapes determine every interface
- Zentao before file sources: validates ABC against working code
- Code before SKILL.md: SKILL.md reflects behavior, does not drive it
- GitHub rename absolute last: redirects mask CI/CD breakage

### Research Flags for Phases
- **Phase 3:** Needs validation that MarkItDown table extraction is sufficient for requirement documents
- **Phase 4:** superpowers npx detection needs live environment testing
- **Phase 5:** Verify SKILL.md syntax against live platform docs immediately before writing

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack (Python, requests, markdownify) | HIGH | All versions verified on PyPI; Python EOL from official lifecycle |
| MarkItDown recommendation | MEDIUM-HIGH | 91K stars, MIT, active maintenance, but pre-1.0 (v0.1.5) |
| Architecture (ABC + registry) | HIGH | Python stdlib, validated pattern |
| SKILL.md best practices | HIGH | Directly from Anthropic official documentation |
| Pitfalls (AGPL, rename, description) | HIGH | 11 of 16 directly verified in source files; rest from official docs |
| OCR deferral | MEDIUM | Depends on Claude vision sufficiency for image use cases |

**Overall confidence:** HIGH

## Gaps to Address

- MarkItDown table extraction quality needs hands-on testing with actual Zentao requirement documents
- SKILL.md activation rate needs empirical testing (target >85% across 20 prompts)
- superpowers detection method needs live testing with both installation methods
- Concurrent attachment downloads (ThreadPoolExecutor) identified but deferred to post-v2.0

## Stack Decision Quick Reference

| Need | Use This | NOT This | Why |
|------|----------|----------|-----|
| Python | >= 3.10 | 3.6/3.7/3.8/3.9 | All EOL; library requirements |
| HTTP | requests | httpx | No async need; already in use |
| PDF/DOCX | markitdown[docx,pdf] | PyMuPDF, Marker, Docling | MIT, lightweight, unified API |
| HTML->MD | markdownify | regex chain, html.parser | Proven library vs hand-written converter |
| Images | Claude vision | pytesseract, EasyOCR | Zero dependency; Claude is multimodal |
| Testing | pytest + ruff | unittest, flake8+black | Modern standards |
| Config dir | .worklet/ (custom) | XDG dirs | Project-specific workspace discovery |

## Sources

### Primary (HIGH confidence)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Claude Code Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Microsoft MarkItDown (GitHub)](https://github.com/microsoft/markitdown) -- v0.1.5, 91K stars, MIT
- [MarkItDown PyPI](https://pypi.org/project/markitdown/)
- [requests PyPI](https://pypi.org/project/requests/) -- v2.33.1, Python 3.10+
- [python-docx PyPI](https://pypi.org/project/python-docx/) -- v1.2.0, MIT
- [pdfplumber PyPI](https://pypi.org/project/pdfplumber/) -- v0.11.9, BSD
- [markdownify PyPI](https://pypi.org/project/markdownify/) -- v1.2.2, MIT
- [PyMuPDF AGPL Discussion](https://github.com/pymupdf/PyMuPDF/discussions/971)
- [Python Version Status](https://devguide.python.org/versions/)

### Secondary (MEDIUM confidence)
- [PDF Extractors Comparison 2025](https://dev.to/onlyoneaman/i-tested-7-python-pdf-extractors-so-you-dont-have-to-2025-edition-akm)
- [MarkItDown Guide (Real Python)](https://realpython.com/python-markitdown/)
- [HTTPX vs Requests](https://www.morethanmonkeys.co.uk/article/comparing-requests-and-httpx-in-python-which-http-client-should-you-use-in-2025/)
- [Python 3.9 EOL (Red Hat)](https://developers.redhat.com/articles/2025/12/04/python-39-reaches-end-life-what-it-means-rhel-users)
- Codebase analysis: `scripts/chandao_fetch/*.py`, `SKILL.md`, `.github/workflows/release.yml`

---
*Research completed: 2026-04-04*
*Ready for roadmap: yes*

# Project Research Summary

**Project:** Worklet (v2.0.0) — refactored from zentao-workflow
**Domain:** CLI developer workflow tool / Claude Code Skill
**Researched:** 2026-04-04
**Confidence:** HIGH

## Executive Summary

Worklet v2.0 is a major refactoring of a Claude Code Skill that currently fetches requirements exclusively from the Zentao project management API. The v2.0 goal is to transform it into a multi-source tool that also reads local Markdown, PDF, and Word documents, while simultaneously shedding the Java dual-runtime, raising the Python version floor, and rewriting the Skill's surface area to meet current Claude Code platform standards. Experts build this class of tool using a pipeline architecture with a source plugin registry — each source fetches raw content, a normalizer converts it to a unified model, and a shared exporter writes Markdown output. This pattern keeps all downstream code (tech plan generation, superpowers integration) source-agnostic and allows new source types to be added without modifying existing pipeline code.

The recommended approach is a bottom-up build order across five logical phases: Foundation (rename, models, ABCs), Core Pipeline (Zentao + Markdown working end-to-end), Extended Sources (PDF + DOCX + images), Pipeline Assembly (CLI auto-detection, exporter rewrite), and finally the SKILL.md rewrite. This ordering is non-negotiable: the SKILL.md must always be the last artifact updated because it reflects actual code behavior, not the other way around. The rename from `chandao`/`zentao` to `worklet` and the Java removal must be the first tasks completed atomically, since every other change builds on correct naming.

The two highest-risk operations are (1) breaking Claude Code Skill discovery by writing a description field that exceeds 250 characters or uses multiline YAML format, and (2) leaving orphan `chandao`/`java` references scattered across 10+ files during the rename and Java removal phases. Both risks are preventable through disciplined grep-based verification built into each phase as a mandatory completion check. Dependency bloat is the third significant risk: multi-format support must use only pure-Python libraries and delegate image/scanned-PDF understanding to Claude's native multimodal vision, keeping the total install footprint under 50 MB.

## Key Findings

### Recommended Stack

Python 3.10 is the correct version floor for v2.0. The current codebase already uses `@dataclass` (requiring Python 3.7+), so the stated 3.6 constraint was never valid. More critically, `requests` 2.33.x now requires Python 3.10+, and every major tooling library (pip, setuptools, ruff, mypy) has already dropped support for anything below 3.9. Raising the floor to 3.10 is a prerequisite for using the current `requests` release and unlocks modern syntax (match/case, union types via `|`).

The runtime dependency list is intentionally minimal. `requests` stays for Zentao API calls — async is unnecessary for sequential API calls to a single server. `markdownify` replaces the 40+ regex chain in `exporter.py`; it is built on `beautifulsoup4` and handles the HTML edge cases the current regex chain silently corrupts. `pypdf` (not PyMuPDF) handles PDF text extraction: pure Python, BSD licensed, zero hard dependencies, and free of the AGPL licensing problem that makes PyMuPDF a dealbreaker for a publicly distributed Skill. `python-docx` handles Word documents with only `lxml` as a transitive dependency. Total install footprint is approximately 45 MB.

**Core technologies:**
- Python >= 3.10: runtime — oldest version still receiving security patches; required by `requests` 2.33.x
- requests >= 2.32.0: Zentao API HTTP client — already in use, sufficient for sequential sync calls
- python-docx >= 1.2.0: Word document reading — de facto standard, MIT licensed
- pypdf >= 6.9: PDF text extraction — pure Python, BSD licensed, zero required dependencies
- markdownify >= 0.14.1: HTML-to-Markdown conversion — replaces fragile 40+ regex chain, MIT licensed
- pytest >= 8.0 + ruff >= 0.9.0: testing and linting — industry standard

**Note on PDF library:** STACK.md recommends `pdfplumber` (better table extraction) while ARCHITECTURE.md recommends `pypdf` (zero hard dependencies). Given the dependency-weight constraint, `pypdf` is the safer default; `pdfplumber` can be offered as an optional extra if table fidelity becomes a user complaint after v2.0 ships.

### Expected Features

**Must have (table stakes):**
- Zentao API read (story/task/bug) — existing core, needs rename and client bug fixes (timeout, streaming download, exception types)
- Markdown file reading — simplest new input format, validates the multi-source architecture
- PDF text extraction — highest-value enterprise document format
- Word (.docx) reading — second-most-common enterprise format
- Attachment and inline image download — existing feature extended to local file sources
- Tech plan generation via superpowers:brainstorming — existing v1.5 core, unchanged
- Config file management — rename `.chandao/` to `.worklet/`, add credential protection and automatic `.gitignore` setup

**Should have (differentiators):**
- Auto-detect input type from path — user provides path, tool infers Zentao ID vs file vs folder (FolderSource > FileSource > ZentaoSource detection order)
- Streaming file download with atomic write — prevents partial-file corruption on large attachments
- Config file permission protection (0600) — credentials are plaintext, must be protected
- Image passthrough to Claude — copy image to workspace, let Claude's multimodal vision interpret; no OCR needed
- Environment detection with caching (24h TTL) — skip slow checks on repeat runs
- Folder scanning (recursive) — aggregate all docs from a project docs directory

**Explicitly deferred (v2.1+):**
- OCR / image text extraction — Claude's vision is sufficient; pytesseract/EasyOCR adds 2 GB+ to install
- Zentao write operations — read-only safety constraint is non-negotiable
- Real-time sync, GUI, batch project download — outside Skill scope

### Architecture Approach

The recommended pattern is Source-Normalize-Pipeline with an ABC-based plugin registry. A `BaseSource` abstract class defines a `fetch()` interface; concrete subclasses (`ZentaoSource`, `FileSource`, `FolderSource`) return a `RawContent` dataclass. A `Normalizer` converts `RawContent` to a unified `Worklet` model. The `Exporter` writes the `Worklet` to Markdown. An `InputParser` handles CLI args and auto-detection via each source's `can_handle()` classmethod. Source-specific model knowledge (Story, Task, Bug fields) is fully encapsulated inside `ZentaoSource` and never leaks into the shared pipeline. Format-specific readers (`PdfReader`, `DocxReader`, `MarkdownReader`, `ImageReader`) use lazy imports so users who only use Zentao source are not required to install `pypdf` or `python-docx`.

**Major components:**
1. **InputParser** (`worklet/cli.py`) — CLI argument parsing and auto-detection of source type
2. **SourceRegistry + BaseSource** (`worklet/sources/base.py`) — `__subclasses__()` auto-discovery, zero manual registration
3. **ZentaoSource** (`worklet/sources/zentao.py`) — replaces `client.py` + `service.py`; fixes streaming download and timeout
4. **FileSource / FolderSource** (`worklet/sources/file.py`, `folder.py`) — delegates format dispatch to readers
5. **Readers** (`worklet/readers/`) — `MarkdownReader`, `PdfReader`, `DocxReader`, `ImageReader`; all use lazy optional imports
6. **Normalizer** (`worklet/normalizer.py`) — `RawContent` -> `Worklet`; single conversion point for the whole pipeline
7. **Exporter** (`worklet/exporter.py`) — rewritten using `markdownify`; accepts `Worklet` model only
8. **WorkletConfig** (`worklet/config.py`) — renamed from `ChandaoConfig`; adds env cache, credential protection, `.chandao/` migration prompt

### Critical Pitfalls

1. **Wrong SKILL.md variable syntax** — current `{SKILL_DIR}` is not a recognized substitution; replace all instances with `${CLAUDE_SKILL_DIR}`. Failure silently breaks path resolution on any non-standard install. Verify with `grep -c 'SKILL_DIR' SKILL.md` returning zero after rewrite.

2. **SKILL.md description too long** — descriptions over 250 characters are truncated in skill listings; multiline YAML `|` blocks trigger a known skill discovery bug (GitHub Issue #9817). Keep to a single-line value under 250 characters, front-loading the primary use case.

3. **Incomplete rename leaves orphan references** — the rename touches 6 Python modules, SKILL.md (625 lines), release.yml, README, and templates. Run `grep -ri "chandao|zentao|java|jar" scripts/ SKILL.md .github/` after each phase; treat unexpected matches as blocking failures. Do NOT rename entries in CHANGELOG.md historical sections.

4. **Config migration without user prompt** — silently changing `.chandao/config.properties` to `.worklet/config.properties` means all existing users lose credentials on upgrade. On first run, detect the old path and offer a one-time migration prompt. Auto-migrating silently is not acceptable.

5. **Streaming download partial file corruption** — replacing `response.content` (in-memory) with `stream=True` introduces a third state: file exists on disk but is truncated. Use atomic write pattern: write to `.tmp`, rename on completion, clean up `.tmp` on exception.

6. **Trigger keyword over-triggering** — generic keywords like "开发" and "优化" will fire the skill during unrelated coding conversations. Require compound keywords ("开发需求", "worklet") or use user-invoked-only mode (`/worklet`). Test with a normal coding session to count false positive activations.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Foundation and Rename
**Rationale:** Every subsequent change depends on correct naming and stable data model shapes. The rename and Java removal must be one atomic commit to avoid a mixed state where some files say `chandao` and others say `worklet`. Setting Python 3.10 as the floor before writing new code prevents wasted effort on compatibility shims.
**Delivers:** Renamed `worklet` package; `Worklet`, `RawContent`, `Attachment` dataclasses; `WorkletConfig` with 0600 permissions, `.gitignore` setup, and `.chandao/` migration prompt; `BaseSource` and `BaseReader` ABCs; Java artifacts and all Java references deleted.
**Addresses:** Config management (table stakes), credential protection (differentiator)
**Avoids:** Pitfall 3 (orphan rename references), Pitfall 4 (Java refs in SKILL.md/CI), Pitfall 12 (false Python 3.6 constraint), Pitfall 13 (credential leak via git)

### Phase 2: Core Pipeline — Zentao + Markdown
**Rationale:** Validate the `BaseSource` ABC against the already-working Zentao use case before adding net-new sources. If the interface design has a flaw, discovering it here while the surface area is minimal is cheap. `MarkdownReader` (stdlib `open()`) is trivially simple and validates the file source path at almost zero cost.
**Delivers:** End-to-end pipeline working for Zentao IDs and local `.md` files. `ZentaoSource` with streaming download fix and atomic write. Rewritten `Exporter` using `markdownify` (with test corpus verified before replacing the regex chain). `Normalizer`. Integration test.
**Uses:** `requests >= 2.32.0`, `markdownify >= 0.14.1`
**Avoids:** Pitfall 9 (HTML converter rewrite — build test corpus first), Pitfall 11 (streaming partial files)

### Phase 3: Extended File Sources
**Rationale:** PDF, DOCX, and image support are net-new functionality. Keeping them in a separate phase from the Zentao migration means a clean rollback point. Lazy imports for `pypdf` and `python-docx` are mandatory — users who only use Zentao must not be required to install document parsing libraries.
**Delivers:** `PdfReader` (pypdf, lazy import), `DocxReader` (python-docx, lazy import), `ImageReader` (copy + markdown reference), `FolderSource`. All format libraries are optional with a clear error message pointing to the install command.
**Uses:** `pypdf >= 6.9` (lazy), `python-docx >= 1.2.0` (lazy)
**Avoids:** Pitfall 6 (dependency bloat — pure Python only, leverage Claude multimodal for images)

### Phase 4: Pipeline Assembly and CLI
**Rationale:** `InputParser` auto-detection logic and `__main__.py` orchestration depend on knowing each source's `can_handle()` implementation. Finalizing the CLI after sources are stable prevents interface churn. Environment detection caching and superpowers detection belong here because they are operational concerns tied to the CLI entry point.
**Delivers:** `InputParser` with auto-detection (FolderSource > FileSource > ZentaoSource priority order), environment detection with 24h TTL cache and content-based invalidation, superpowers detection by capability (not file path), `--no-cache` flag.
**Avoids:** Pitfall 8 (stale env cache), Pitfall 15 (superpowers detection path coupling to installation method)

### Phase 5: SKILL.md Rewrite and Release
**Rationale:** SKILL.md is the integration layer that reflects final code behavior. Writing it before code is stable means updating it repeatedly. GitHub repo rename must be absolute last: redirects mask CI/CD breakage in release artifact naming.
**Delivers:** SKILL.md with `${CLAUDE_SKILL_DIR}` throughout, single-line description under 250 characters, references/ directory structure for progressive disclosure, compound trigger keywords only. Updated release.yml with `worklet` naming and directory structure. GitHub repo rename.
**Avoids:** Pitfall 1 (wrong variable syntax), Pitfall 2 (description too long), Pitfall 7 (CI/CD breakage from premature rename), Pitfall 10 (over-triggering from generic keywords)

### Phase Ordering Rationale

- Rename first because all file paths, config keys, import names, and CI/CD artifacts depend on it; mid-refactor renaming means double-touching every file
- Models before sources because `Worklet` and `RawContent` shape determines every component's interface; wrong shapes here are the most expensive mistakes
- Zentao before file sources because it validates the `BaseSource` ABC against a real working case before adding net-new complexity
- File sources before pipeline assembly because `InputParser` auto-detection depends on knowing each source's `can_handle()` behavior
- SKILL.md absolute last because it must reflect final code behavior, not drive it
- GitHub rename after all content updates because GitHub redirects give a false sense of safety while CI/CD artifact names remain broken

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 5 (SKILL.md rewrite):** Claude Code Skill authoring evolves rapidly; verify current frontmatter fields, substitution variable names, and description character limits against the live platform docs immediately before writing — not at research time
- **Phase 4 (superpowers detection):** The shift from `claude plugins add` to `npx` installation is in-progress; capability-based detection approach needs verification against both installation methods in a live environment

Phases with well-documented patterns (skip deeper research):
- **Phase 1 (Foundation/Rename):** Pure mechanical refactoring with grep-based verification; Python dataclass and ABC patterns are stdlib
- **Phase 2 (Zentao + Markdown):** Zentao client is well-understood from v1.x; markdownify is stable and well-documented
- **Phase 3 (File Sources):** pypdf and python-docx both have complete, current documentation

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All library versions verified on PyPI; Python EOL dates from official python.org lifecycle; AGPL concern confirmed via PyMuPDF GitHub discussion |
| Features | HIGH | Based on existing v1.x feature set plus direct PROJECT.md requirements; no speculative features included |
| Architecture | HIGH | Pattern sourced from multiple production case studies; ABC + `__subclasses__()` verified against Python stdlib docs; build order derived from direct codebase dependency analysis |
| Pitfalls | HIGH | 11 of 15 pitfalls directly verified in source files (`exporter.py`, `client.py`, `SKILL.md`, `release.yml`); 4 are preventive based on Claude Code official docs and confirmed GitHub issue reports |

**Overall confidence:** HIGH

### Gaps to Address

- **pypdf vs pdfplumber final decision:** Must be resolved before Phase 3 begins. Recommendation is pypdf as default (lighter), pdfplumber as optional extra if users report table quality issues.
- **superpowers detection verification:** Capability-based detection (check exit code of a superpowers command) is the proposed approach for Phase 4, but requires hands-on testing against both `claude plugins add` and `npx` installation methods.
- **Folder scanning scope:** FEATURES.md marks folder scanning as "defer," but ARCHITECTURE.md includes `FolderSource` in the Phase 3 build order. Align on v2.0 scope before Phase 3 planning to avoid designing components that get cut.
- **Concurrent attachment downloads:** Not addressed in the architecture. `concurrent.futures.ThreadPoolExecutor` is stdlib and could parallelize attachment downloads. Defer to a post-v2.0 optimization unless performance is flagged during testing.

## Sources

### Primary (HIGH confidence)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills) — SKILL.md format, variable substitution syntax, frontmatter fields
- [Claude Code Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — description length limits, triggering behavior
- [GitHub Issue #9817](https://github.com/anthropics/claude-code/issues/9817) — multiline description breaks skill discovery
- [Python Version Status](https://devguide.python.org/versions/) — EOL timeline confirming 3.6-3.9 end-of-life
- [requests PyPI](https://pypi.org/project/requests/) — v2.33.1, Python 3.10+ requirement confirmed
- [python-docx PyPI](https://pypi.org/project/python-docx/) — v1.2.0, MIT, Python >= 3.9
- [pypdf PyPI](https://pypi.org/project/pypdf/) — v6.9.2, BSD, zero required dependencies confirmed
- [markdownify PyPI](https://pypi.org/project/markdownify/) — v1.2.2, MIT
- [PyMuPDF AGPL Discussion](https://github.com/pymupdf/PyMuPDF/discussions/971) — AGPL license dealbreaker confirmed
- [GitHub Docs: Renaming a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository) — redirect behavior and CI/CD limitations
- Codebase direct analysis: `scripts/chandao_fetch/*.py`, `SKILL.md`, `.github/workflows/release.yml`

### Secondary (MEDIUM confidence)
- [pdfplumber PyPI](https://pypi.org/project/pdfplumber/) — v0.11.9, MIT, better table extraction than pypdf
- [Merkle Science: Multi-chain data platform](https://www.merklescience.com/blog/using-python-to-build-a-unified-multi-chain-blockchain-data-harvesting-platform) — Extractor/Normalizer/Exporter production precedent
- [Unstract: Python PDF Libraries 2026](https://unstract.com/blog/evaluating-python-pdf-to-text-libraries/) — library comparison benchmarks
- [OneUptime: Python plugin systems 2026](https://oneuptime.com/blog/post/2026-01-30-python-plugin-systems/view) — `__subclasses__()` discovery pattern
- [Claude Vision API](https://platform.claude.com/docs/en/build-with-claude/vision) — multimodal image input, confirms no OCR dependency needed

---
*Research completed: 2026-04-04*
*Ready for roadmap: yes*

# Roadmap: Worklet v2.0.0

## Overview

Worklet v2.0.0 transforms zentao-workflow from a Zentao-only fetch tool into a multi-source developer workflow assistant. The roadmap moves through five phases: rename and restructure the foundation, rebuild the core pipeline (Zentao + Markdown) on new abstractions, extend to PDF/DOCX/image sources with test coverage, assemble the CLI auto-detection layer, and finally rewrite SKILL.md with full documentation and release. Each phase delivers a verifiable capability; nothing ships until GitHub rename closes Phase 5.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Foundation and Rename** - Rename everything from chandao/zentao to worklet, delete Java, establish new data models and config
- [ ] **Phase 2: Core Pipeline** - End-to-end Zentao + Markdown pipeline with fixed client, new exporter, and source abstractions
- [ ] **Phase 3: Extended Sources and Testing** - PDF, DOCX, image readers via MarkItDown plus full pytest suite
- [ ] **Phase 4: Pipeline Assembly and CLI** - InputParser auto-detection, environment caching, superpowers npx upgrade
- [ ] **Phase 5: SKILL.md Rewrite and Release** - Rewritten skill file, updated docs, CI/CD, changelog, GitHub repo rename

## Phase Details

### Phase 1: Foundation and Rename
**Goal**: The project is fully renamed to Worklet with a clean codebase -- no Java artifacts, no chandao/zentao naming remnants, new data model shapes ready for source plugins
**Depends on**: Nothing (first phase)
**Requirements**: FOUND-01, FOUND-02, FOUND-03, FOUND-04, FOUND-05, FOUND-06, FOUND-07, FOUND-08, FOUND-09, FOUND-10, FOUND-11, FOUND-12, FOUND-13, FOUND-14, FOUND-15, FOUND-16, DOC-03
**Success Criteria** (what must be TRUE):
  1. Running `grep -r "chandao\|zentao" scripts/` returns zero hits (all naming references eliminated)
  2. The Java JAR, java-src/ directory, and all Java references are gone from the repository
  3. `python -c "from worklet import __version__; print(__version__)"` prints "2.0.0" from the renamed package
  4. WorkletConfig loads from .worklet/config.toml with 0600 file permissions enforced
  5. `pyproject.toml` exists and declares Python >= 3.10 with correct project metadata
**Plans:** 1/4 plans executed

Plans:
- [ ] 01-01-PLAN.md -- Delete Java artifacts, clean __pycache__, remove Java permissions from settings
- [x] 01-02-PLAN.md -- Rename package chandao_fetch to worklet, update all imports/classes, version to 2.0.0
- [ ] 01-03-PLAN.md -- Migrate config to TOML format, add new data model stubs, convert config template
- [ ] 01-04-PLAN.md -- Create pyproject.toml, update requirements.txt, update .gitignore/.release-ignore/SKILL.md/release.yml

### Phase 2: Core Pipeline
**Goal**: A developer can fetch a Zentao story/task/bug by ID or read a local Markdown file, and get clean Markdown output through the unified Source-Normalize-Export pipeline
**Depends on**: Phase 1
**Requirements**: INPUT-01, INPUT-02, INPUT-05, CLIENT-01, CLIENT-02, CLIENT-03, CLIENT-04, CLIENT-05, EXPORT-01, EXPORT-02, EXPORT-03
**Success Criteria** (what must be TRUE):
  1. Running the tool with a Zentao story ID produces a Markdown file in .worklet/ with all attachments downloaded (streaming, with timeout)
  2. Running the tool with a local .md file path produces equivalent normalized output through the same pipeline
  3. The Exporter converts Zentao HTML content to Markdown using markdownify (no regex chain) with correct image path references
  4. Subtask detection runs in Python code, not in SKILL.md logic
**Plans**: TBD

### Phase 3: Extended Sources and Testing
**Goal**: The tool handles PDF, DOCX, and image files as input sources, and the entire codebase has pytest coverage validating each component
**Depends on**: Phase 2
**Requirements**: INPUT-03, INPUT-04, INPUT-06, INPUT-07, INPUT-08, TEST-01, TEST-02, TEST-03, TEST-04, TEST-05, TEST-06
**Success Criteria** (what must be TRUE):
  1. Running the tool with a PDF file extracts text content and produces Markdown output (via MarkItDown lazy import)
  2. Running the tool with a DOCX file extracts text content and produces Markdown output (via MarkItDown lazy import)
  3. Running the tool with an image file copies it to the workspace and generates a Markdown reference for Claude multimodal processing
  4. Running the tool with a folder path recursively scans and aggregates all supported file types
  5. `pytest` passes with tests covering config, ZentaoSource (mocked), Exporter, InputParser, and all readers
**Plans**: TBD

### Phase 4: Pipeline Assembly and CLI
**Goal**: The tool auto-detects input type (folder vs file vs Zentao ID) and manages its runtime environment with smart caching
**Depends on**: Phase 3
**Requirements**: INPUT-09, ENV-01, ENV-02, ENV-03, ENV-04
**Success Criteria** (what must be TRUE):
  1. Passing a folder path, a file path, or a Zentao ID to the tool triggers the correct source handler without user intervention
  2. Environment detection uses try-first-check-later strategy and caches successful results in .worklet/config.properties with 24h TTL
  3. superpowers is detected and installed via npx (not `claude plugins add`)
  4. No Java environment detection code remains
**Plans**: TBD

### Phase 5: SKILL.md Rewrite and Release
**Goal**: Worklet is installable as a Claude Code Skill with correct trigger keywords, updated documentation, and a published GitHub release
**Depends on**: Phase 4
**Requirements**: SKILL-01, SKILL-02, SKILL-03, SKILL-04, SKILL-05, DOC-01, DOC-02, DOC-04, DOC-05, REL-01, REL-02, REL-03, REL-04, REL-05
**Success Criteria** (what must be TRUE):
  1. SKILL.md has a single-line description under 250 characters and triggers on generic dev keywords (not just zentao/chandao)
  2. SKILL.md uses ${CLAUDE_SKILL_DIR} for all path references and asks users to choose input source (Zentao API or local file)
  3. CLAUDE.md, CONTRIBUTING.md, README.md, and reference docs all reflect the Worklet name and v2.0.0 architecture
  4. release.yml produces a clean release artifact with no Java files and correct directory structure
  5. GitHub repository is renamed to "worklet"
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation and Rename | 1/4 | In Progress|  |
| 2. Core Pipeline | 0/? | Not started | - |
| 3. Extended Sources and Testing | 0/? | Not started | - |
| 4. Pipeline Assembly and CLI | 0/? | Not started | - |
| 5. SKILL.md Rewrite and Release | 0/? | Not started | - |

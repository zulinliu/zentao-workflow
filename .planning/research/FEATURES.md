# Feature Landscape

**Domain:** Development workflow automation (Claude Code Skill: requirement-to-code pipeline)
**Researched:** 2026-04-04
**Overall Confidence:** MEDIUM-HIGH (based on official Claude Code docs, ecosystem research, and competitive analysis)

---

## Table Stakes

Features users expect from a development workflow assistant Skill. Missing any of these means the product feels broken or incomplete compared to alternatives.

| # | Feature | Why Expected | Complexity | Notes |
|---|---------|--------------|------------|-------|
| T1 | **Multi-source requirement input** | Users have requirements in various places (API systems, local files, URLs). A "universal workflow assistant" that only reads from one API is not universal. | Medium | v1.x only supports Zentao API. v2.0 must add local file/folder input at minimum. URL and clipboard can follow. |
| T2 | **Markdown file reading** | Markdown is the lingua franca of developer documentation. Every dev has .md files with specs/requirements. | Low | Python `open()` + parse. Already partially supported via Markdown export. |
| T3 | **Reliable skill activation** | Research shows baseline activation is ~50% without optimization, dropping to 20% with poor descriptions. If the skill does not trigger when users say "develop this requirement," it is effectively invisible. | Medium | Current v1.6 description is 1000+ chars, Chinese-heavy. Must be restructured with imperative triggers, negative constraints, and bilingual keywords. 250-char truncation limit is critical. |
| T4 | **Configuration management** | Users expect one-time setup, not re-entering credentials every session. Config must survive across sessions and support project-scoped overrides. | Low | Already exists (`.chandao/config.properties`). Needs rename to `.worklet/` and permission hardening (0600). |
| T5 | **Environment detection** | Auto-detect available runtimes (Python) and dependencies (superpowers plugin) without manual user intervention. | Low | Already exists. Simplify to Python-only (remove Java detection). Add "try-first, check-later" pattern with cached results. |
| T6 | **Technical plan generation** | The core value proposition is "requirement to code." Without plan generation, this is just a download tool. Spec-driven development (GitHub Spec Kit, Kiro, superpowers:brainstorming) has become the industry norm in 2026. | Medium | Already exists via superpowers:brainstorming delegation. Keep this pattern but make the input source-agnostic. |
| T7 | **Attachment/image download** | Requirements frequently include screenshots, mockups, and supplementary files. Losing attachments means losing critical context. | Low | Already implemented. Maintain current behavior. |
| T8 | **Cross-platform support** | Developers use Linux, macOS, and Windows. A CLI tool that only works on one platform is rejected immediately. | Low | Already supported. Maintain path handling with `pathlib`. |
| T9 | **Workspace-scoped storage** | Downloaded content and generated plans must live in the project workspace, not scattered globally. Different projects must not interfere with each other. | Low | Already implemented (workspace-first, global fallback). Rename directories. |
| T10 | **Progress feedback** | Users need to know the tool is working, especially during multi-step operations (download -> parse -> plan). Silent operations feel broken. | Low | Partially implemented (Step progress markers). Ensure all async operations provide feedback. |

---

## Differentiators

Features that set Worklet apart from manually invoking superpowers or using generic spec-driven tools. These are not expected but provide significant value.

| # | Feature | Value Proposition | Complexity | Notes |
|---|---------|-------------------|------------|-------|
| D1 | **PDF/Word document parsing** | Competitors (GitHub Spec Kit, Kiro) assume requirements are already in text. Enterprise teams frequently receive requirements as PDF/Word. Being able to ingest these directly is a genuine time-saver. | Medium | Use Microsoft MarkItDown (lightweight, MIT, supports PDF/DOCX/PPTX/images, no ML dependencies). Avoid Marker/Docling (too heavy for a Skill). |
| D2 | **Image-based requirement reading (multimodal)** | Requirements sometimes arrive as screenshots or photographed whiteboards. Claude's multimodal capabilities can read these natively. No OCR library needed for basic image understanding. | Low | Simply pass image path to Claude and let it describe the requirement. For actual OCR text extraction, use MarkItDown's OCR plugin as optional enhancement. |
| D3 | **Sub-task/parent-task auto-resolution** | Zentao (and other PM tools) have hierarchical task structures where child tasks have empty descriptions. Automatically fetching parent context saves significant manual work. | Low | Already implemented in v1.6. Generalize the pattern for future PM tool integrations. |
| D4 | **Project tech stack auto-detection** | Automatically detecting whether a project uses Java/Spring, React, Python/Django etc. allows the plan generator to produce contextually relevant implementation steps. | Low | Check for `pom.xml`, `package.json`, `requirements.txt`, `go.mod` etc. Already partially implemented. |
| D5 | **Bilingual trigger activation** | Most Claude Code Skills are English-only. Supporting both Chinese and English trigger keywords captures the Chinese developer market while remaining accessible globally. | Low | Must be done carefully due to 250-char description truncation. Front-load English triggers, add Chinese in examples. |
| D6 | **Spec-driven plan structure** | Align plan output with the emerging spec-driven development standard (requirements.md -> design.md -> tasks.md), making plans directly consumable by other tools like GitHub Spec Kit or cc-sdd. | Medium | Restructure tech_plan_template.md to follow the three-artifact pattern (requirements, design, tasks) instead of the current monolithic format. |
| D7 | **Configurable execution mode** | After plan generation, let users choose their preferred execution path: superpowers:subagent-driven-development for large features, executing-plans for batch work, or manual implementation. | Low | Already implemented in v1.5 Step 6. Maintain and polish. |
| D8 | **Smart content caching** | Cache previously downloaded requirements locally so repeated invocations for the same ID do not hit the API again. Saves time and reduces API load. | Low | Check if `{type}/{id}-*.md` already exists. Ask user whether to re-download or use cached. |
| D9 | **Zentao URL parsing** | Accept full Zentao URLs (e.g., `https://zentao.example.com/story-view-38817.html`) and automatically extract type + ID. Users often paste URLs from browser. | Low | Already partially implemented. Ensure robust regex for various Zentao URL formats. |
| D10 | **Folder scanning with aggregation** | Read all supported documents from a folder, aggregate context, and generate a unified plan. Useful when requirements are split across multiple files. | Medium | Walk directory tree, filter by supported extensions, concatenate content with source attribution. |
| D11 | **Streaming file download** | Large attachments do not exhaust memory. Download with chunked transfer. | Low | `requests` with `stream=True`, write chunks. Fixes existing client.py OOM issue. |

---

## Anti-Features

Features to explicitly NOT build. Building these would increase complexity without proportional value, or would violate the tool's design principles.

| # | Anti-Feature | Why Avoid | What to Do Instead |
|---|--------------|-----------|-------------------|
| A1 | **Write-back to PM systems** | Creating/updating/deleting items in Zentao (or any PM tool) from a CLI tool is a security and trust nightmare. One wrong API call can corrupt data. The tool's safety model is "read-only." | Maintain strict read-only constraint. If users need write-back, they use the PM tool's own UI. |
| A2 | **GUI/web interface** | Worklet is a Claude Code Skill, meaning it runs inside Claude Code's terminal. Building a GUI contradicts the CLI-native positioning and adds enormous maintenance cost. | Keep everything terminal-based. Use Claude Code's native AskUserQuestion for interactive input. |
| A3 | **Real-time sync/webhooks** | Polling PM systems for changes or receiving webhooks adds infrastructure requirements (servers, ports, persistent processes) that are incompatible with a Skill's lifecycle (invoked, runs, exits). | On-demand fetch only. Users invoke when they need content. |
| A4 | **Multi-PM-tool adapter layer** | Building generic adapters for Jira, GitHub Issues, Linear, etc. in v2.0 is scope creep. The PM API integration is one input source among many; local files are more universally useful. | Keep Zentao as the only API source in v2.0. Design the internal interface so other PM tools could be added later, but do not build them now. |
| A5 | **Heavyweight document parsing dependencies** | Libraries like Docling (IBM, heavy ML models), Marker (requires GPU for speed), or MinerU add hundreds of MB of dependencies. This violates the "lightweight, minimal dependencies" constraint. | Use MarkItDown (Microsoft, lightweight, no ML deps for core features) for PDF/Word. For images, rely on Claude's multimodal capability first. |
| A6 | **Batch/project-level download** | Downloading all stories/tasks in a Zentao project (e.g., "fetch everything in sprint 42") is complex (pagination, rate limiting, storage) and encourages working on too many things at once. | Keep single-item and explicit multi-ID download only. The existing v1.x warning about multi-download is good UX. |
| A7 | **Built-in test generation** | The tech plan template previously included test plans. superpowers:brainstorming and TDD skills handle this better. Duplicating test generation in the Skill adds no value. | Delegate to superpowers TDD skill during execution phase. Already removed in v1.5. |
| A8 | **Configuration migration from v1.x** | Building auto-migration from `.chandao/` to `.worklet/` adds complexity for a one-time operation affecting few users. | Document the manual migration (rename directory) in CHANGELOG. Do not auto-migrate. |
| A9 | **Plugin marketplace distribution** | Publishing to Claude's plugin marketplace requires ongoing maintenance, review processes, and compatibility testing. For a niche tool, personal/project skill installation is sufficient. | Distribute as a GitHub repo with installation instructions. Users clone or add as git submodule. |
| A10 | **Java runtime support** | v2.0 removes Java to simplify. Maintaining two runtimes doubles testing surface for negligible benefit (Python is now stable). | Python-only. Remove JAR, java-src, and all Java-related code paths. |
| A11 | **Legacy .doc (pre-2007) format** | `python-docx` only supports .docx (Word 2007+). Legacy .doc requires heavy dependencies (antiword or LibreOffice subprocess). The format is increasingly rare. | Document the limitation. Suggest users convert .doc to .docx before using the tool. |
| A12 | **Built-in OCR engine** | Adding pytesseract (requires Tesseract binary) or EasyOCR (2GB+ PyTorch) as hard dependencies is disproportionate for a lightweight Skill. | Rely on Claude's native multimodal vision for image reading. Offer MarkItDown OCR plugin as optional enhancement for power users. |

---

## Feature Dependencies

```
T1 (Multi-source input) --+-- T2 (Markdown reading) [prerequisite: file I/O foundation]
                           |-- D1 (PDF/Word parsing) [requires: MarkItDown integration]
                           +-- D2 (Image reading) [requires: Claude multimodal, no code dep]

T3 (Reliable activation) --- independent, but enables all other features to be discovered

T4 (Config management) ---- T5 (Environment detection) [config stores cached env state]

T6 (Tech plan generation) -+-- T1 (Multi-source input) [plans need requirement content]
                            |-- D4 (Tech stack detection) [plans need project context]
                            +-- D6 (Spec-driven structure) [plan format improvement]

D3 (Sub-task resolution) --- T1 (Multi-source input) [only relevant for API sources]

D7 (Execution modes) ------ T6 (Tech plan generation) [executes the generated plan]

D8 (Smart caching) -------- T9 (Workspace storage) [cache lives in workspace]

D10 (Folder scanning) ----- T2 (Markdown reading) [scanning iterates over file reading]
                            D1 (PDF/Word parsing) [folder may contain mixed formats]
```

### Critical Path

The most important dependency chain for v2.0 is:

```
T3 (Activation) -> T1 (Multi-source) -> T6 (Plan generation) -> D7 (Execution)
```

If the skill does not activate (T3), nothing else matters. If it activates but cannot read requirements from multiple sources (T1), the "universal" promise is broken. If requirements are read but no plan is generated (T6), the tool is just a downloader. If plans are generated but cannot be executed (D7), the workflow is incomplete.

---

## MVP Recommendation

### Phase 1: Foundation (Must ship together)

Prioritize in this order:

1. **T3 - Reliable skill activation** -- Single most impactful change. Rewrite SKILL.md frontmatter description to use imperative language, explicit bilingual triggers, negative constraints. Target >85% activation rate. Without this, the tool is invisible.

2. **T1 + T2 - Multi-source input (file/folder + Markdown)** -- The defining feature of v2.0 ("no longer Zentao-only"). Support reading local `.md` and `.txt` files as requirement input. This is the minimum viable "universal."

3. **T4 + T5 - Config/env rename and cleanup** -- `.chandao/` -> `.worklet/`, remove Java detection, add 0600 permissions. Necessary for brand consistency.

4. **T6 - Plan generation (source-agnostic)** -- Ensure brainstorming integration works regardless of whether input came from Zentao API or local file. The plan template should not assume Zentao-specific fields.

5. **T9 - Workspace storage rename** -- Align storage directories with new naming.

### Phase 2: Format Expansion

6. **D1 - PDF/Word parsing via MarkItDown** -- Add `markitdown` as optional dependency. If installed, enable PDF/DOCX input. If not installed, gracefully degrade with "install markitdown for PDF support" message.

7. **D2 - Image requirement reading** -- Leverage Claude's native multimodal. No library needed. Just pass image path to Claude with "describe the requirements shown in this image."

8. **D5 - Bilingual triggers** -- Optimize SKILL.md description for both Chinese and English activation patterns.

### Phase 3: Polish

9. **D6 - Spec-driven plan structure** -- Align plan output with requirements.md / design.md / tasks.md convention.

10. **D8 - Smart content caching** -- Check for existing downloads before re-fetching.

11. **D4 - Tech stack auto-detection** -- Improve project context detection.

12. **D10 - Folder scanning** -- Walk directories, aggregate multi-file requirements.

### Defer to v2.1+

- **D3 (Sub-task resolution)** -- Already works. No changes needed for v2.0.
- **D7 (Execution modes)** -- Already works. Polish only.
- **D9 (URL parsing)** -- Already partially works. Low-priority refinement.
- **D11 (Streaming download)** -- Bug fix, handle during code audit.

---

## Activation Strategy Deep-Dive

The SKILL.md description field is the single most impactful factor for the skill's usefulness. Research across 650 trials shows description wording alone can swing activation from 20% to 100%.

### Current Problems (v1.6)

1. **Too long** -- Over 1000 characters. Will be truncated at 250 chars in skill listings.
2. **Chinese-first** -- Claude's skill routing uses pure LLM reasoning, not keyword matching. Chinese-heavy descriptions may reduce activation reliability for bilingual prompts.
3. **Too specific to Zentao** -- Mentions "zentao", "chandao", "story-view" URLs. v2.0 needs broader triggers.
4. **No negative constraint** -- Does not tell Claude what NOT to do, reducing directive force.
5. **Passive voice** -- Uses descriptive language ("禅道开发工作流助手") instead of imperative commands ("ALWAYS invoke this skill").

### Recommended v2.0 Description

```yaml
description: |
  Development workflow assistant. ALWAYS invoke this skill when user wants to
  develop a requirement, fix a bug, implement a feature, or work on a task from
  any source (zentao, file, folder). Triggers: develop, implement, fix, build,
  requirement, task, bug, story, zentao, chandao, tech plan, specification.
  Do not start coding directly -- use this skill first to generate a plan.
```

Key changes:
- **Imperative language** ("ALWAYS invoke")
- **Negative constraint** ("Do not start coding directly")
- **Broad triggers** (not just Zentao keywords)
- **Under 250 chars for critical info** (front-loaded)
- **English-first** (better LLM routing; Chinese triggers in skill body)

### Description Structure Formula

Based on the research, the optimal formula is:

```
[Domain] expert. ALWAYS invoke this skill when [trigger conditions].
Triggers: [keyword1], [keyword2], [keyword3]...
Do not [alternative action] directly -- use this skill first.
```

### Activation Testing Plan

Based on the 650-trial study findings:

1. Create 20 test prompts (10 Chinese, 10 English) covering trigger scenarios:
   - Direct: "develop requirement 39382"
   - Indirect: "I need to work on this feature"
   - File-based: "implement what's described in spec.md"
   - Chinese: "开发需求39382" / "修复这个bug"
2. Run each prompt 5 times, measure activation rate
3. Target: >85% activation across all prompt types
4. Iterate on description wording until target is met

---

## Document Format Support Matrix

| Format | v1.6 (Current) | v2.0 (Target) | Library | Complexity |
|--------|----------------|----------------|---------|------------|
| Zentao API | Yes | Yes | requests (built-in) | Done |
| Markdown (.md) | Export only | Read input | stdlib (built-in) | Low |
| Plain text (.txt) | No | Yes | stdlib (built-in) | Low |
| PDF (.pdf) | No | Yes (optional) | markitdown | Medium |
| Word (.docx) | No | Yes (optional) | markitdown | Medium |
| Images (.png/.jpg) | Download only | Read via Claude multimodal | None (Claude native) | Low |
| Folder (recursive) | No | Yes (Phase 3) | stdlib os.walk | Medium |
| URL (web page) | No | No (v2.1+) | -- | Deferred |

### Why MarkItDown over alternatives

| Criterion | MarkItDown | Marker | Docling | PyMuPDF4LLM |
|-----------|-----------|--------|---------|-------------|
| Lightweight | Yes (no ML deps) | No (GPU preferred) | No (heavy models) | Yes |
| PDF support | Yes | Yes | Yes | Yes |
| Word/DOCX support | Yes | Yes | Yes | No |
| Image OCR | Via plugin | Built-in | Built-in | Hybrid |
| Install size | Small (~5MB) | Large (~500MB+) | Large (~1GB+) | Medium (~50MB) |
| License | MIT | GPL | MIT | AGPL |

**Decision:** Use MarkItDown because it is the only option that is (a) lightweight, (b) covers both PDF and Word, (c) MIT licensed, and (d) maintained by Microsoft with active development. MarkItDown requires Python 3.10+, which means v2.0 should raise its minimum Python version from 3.6 to 3.10 (acceptable given the constraint note says 3.6 is for "enterprise environments," but MarkItDown is optional -- the core tool can still work on 3.6 with Markdown/text input only).

---

## Spec-Driven Plan Format (D6)

The industry is converging on a three-artifact pattern for spec-driven development. Aligning Worklet's output with this standard makes plans interoperable with GitHub Spec Kit, Kiro, cc-sdd, and other tools.

### Current Format (v1.5 monolithic)

```
{type}_{id}_技术实现方案.md
  - 需求分析 (Requirement Analysis)
  - 架构设计 (Architecture Design)
  - 实现步骤 (Implementation Steps)
```

### Proposed Format (v2.0 three-artifact)

```
.worklet/plans/{source_identifier}/
  - requirements.md   (Requirement analysis, acceptance criteria)
  - design.md          (Architecture, tech choices, module design)
  - tasks.md           (Implementation steps, file paths, verification)
```

**Benefits:**
- Each artifact can be reviewed/approved independently
- Compatible with spec-driven development tools
- superpowers:brainstorming can focus on design.md
- superpowers:subagent-driven-development can consume tasks.md directly
- Easier to update one aspect without regenerating the entire plan

**Risk:** This is a MEDIUM confidence recommendation. The three-artifact pattern is well-documented but Worklet's integration with superpowers may not cleanly separate into three phases. Needs validation during implementation.

---

## Confidence Assessment

| Area | Confidence | Reasoning |
|------|-----------|-----------|
| Table stakes list | HIGH | Based on official Claude Code docs, existing v1.x features, and clear user expectations for the "universal" positioning |
| Activation strategy | HIGH | Backed by 650-trial empirical study and official Claude docs on description truncation. Description wording is proven to be the primary lever. |
| MarkItDown recommendation | MEDIUM | MarkItDown is well-documented and actively maintained, but its Python 3.10 requirement creates a compatibility trade-off. Needs testing with Worklet's architecture. |
| Spec-driven plan format | MEDIUM | Industry trend is clear (GitHub, AWS, community tools all converging). But integration with superpowers:brainstorming workflow needs validation. |
| Anti-features list | HIGH | Directly validated against PROJECT.md out-of-scope items and the tool's stated design constraints. |
| Feature dependencies | HIGH | Logical ordering validated against existing code structure and the critical path analysis. |

---

## Sources

### Official Documentation (HIGH confidence)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills) -- Authoritative reference for skill structure, activation, frontmatter, 250-char truncation, budget scaling.
- [GitHub Spec Kit](https://github.com/github/spec-kit) -- Specification -> Plan -> Tasks -> Implementation workflow standard.
- [Kiro by AWS](https://kiro.dev/) -- Requirements -> Design -> Tasks three-phase spec workflow.
- [Superpowers Plugin (GitHub)](https://github.com/obra/superpowers) -- Brainstorming, subagent-driven-development, TDD skills framework.

### Activation Research (MEDIUM confidence)
- [Claude Code Skills Activation Guide (Gist)](https://gist.github.com/mellanon/50816550ecb5f3b239aa77eef7b8ed8d) -- 200+ prompt testing results, activation patterns.
- [How to Make Claude Code Skills Actually Activate - 650 Trials (Medium)](https://medium.com/@ivan.seleznov1/why-claude-code-skills-dont-activate-and-how-to-fix-it-86f679409af1) -- Description wording as primary activation lever.
- [2 Fixes for 95% Activation (DEV Community)](https://dev.to/oluwawunmiadesewa/claude-code-skills-not-triggering-2-fixes-for-100-activation-3b57) -- Hook-based detection, forced evaluation patterns.

### Ecosystem & Workflow Research (MEDIUM confidence)
- [Spec-Driven Development Analysis (Martin Fowler)](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) -- Comparison of SDD tools and approaches.
- [Addy Osmani - How to Write a Good Spec](https://addyosmani.com/blog/good-spec/) -- Spec quality patterns for AI agents.
- [Addy Osmani - AI Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/) -- Layered tooling patterns.
- [AWS AI-Driven Development Life Cycle](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/) -- Enterprise spec-to-code patterns.

### Document Parsing Libraries (MEDIUM-HIGH confidence)
- [Microsoft MarkItDown (GitHub)](https://github.com/microsoft/markitdown) -- Lightweight PDF/Word/Image to Markdown. MIT license.
- [Python MarkItDown Guide (Real Python)](https://realpython.com/python-markitdown/) -- Usage patterns and limitations.
- [XDG Base Directory Specification](https://xdgbasedirectoryspecification.com/) -- Standard for CLI config directory placement.

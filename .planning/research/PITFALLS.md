# Domain Pitfalls

**Domain:** CLI tool refactoring (zentao-workflow v1.6 to Worklet v2.0) + Claude Code Skill development
**Researched:** 2026-04-04 (updated)
**Overall confidence:** HIGH

## Critical Pitfalls

Mistakes that cause rewrites, broken releases, or silent user-facing failures.

---

### Pitfall 1: SKILL.md Uses Wrong Variable Syntax -- `{SKILL_DIR}` vs `${CLAUDE_SKILL_DIR}`

**What goes wrong:** The current SKILL.md references `{SKILL_DIR}` throughout. The official Claude Code substitution syntax is `${CLAUDE_SKILL_DIR}`. The braces-without-dollar-sign form is NOT a recognized substitution.
**Why it happens:** SKILL.md was authored before Claude Code standardized the syntax.
**Consequences:** Scripts fail on non-standard install paths. Skill becomes non-portable.
**Prevention:** Replace ALL `{SKILL_DIR}` with `${CLAUDE_SKILL_DIR}`. Validate against official docs.
**Detection:** `grep -c 'SKILL_DIR' SKILL.md` -- must return zero matches for old pattern.
**Confidence:** HIGH -- verified against official Claude Code docs.

---

### Pitfall 2: SKILL.md Description Too Long -- Kills Skill Discovery

**What goes wrong:** The current description is 40+ lines (~1,200 characters). Official docs state max 1024 characters, and descriptions over 250 characters are truncated in skill listings. GitHub issue #9817 documents multiline description bugs.
**Why it happens:** Features and triggers accumulated over v1.0-v1.6 in the description field.
**Consequences:** Skill may not appear in Claude's available skills list. Auto-triggering fails.
**Prevention:** Rewrite to under 250 characters. Move trigger conditions into SKILL.md body.
**Detection:** `wc -c` on description field -- must be under 250.
**Confidence:** HIGH -- confirmed via official docs and GitHub bug report.

---

### Pitfall 3: Incomplete Rename Leaves Orphan References

**What goes wrong:** Renaming from `chandao`/`zentao` to `worklet` misses references in string literals, config keys, log messages, CI scripts.
**Why it happens:** References scattered across 6 Python modules, SKILL.md (625 lines), release.yml, README, CHANGELOG.
**Consequences:** Config files written to `.chandao/` instead of `.worklet/`. User-Agent identifies as old tool. Release package named wrong.
**Prevention:**
1. Create exhaustive grep-based rename checklist BEFORE starting
2. Post-rename verification: `grep -ri "chandao\|zentao" scripts/ SKILL.md .github/`
3. Whitelist CHANGELOG.md historical entries only
**Detection:** Automated grep as pre-commit step.
**Confidence:** HIGH -- directly verified in codebase.

---

### Pitfall 4: Removing Java Without Updating All References

**What goes wrong:** Deleting JAR and java-src/ but leaving Java references in SKILL.md (detection, commands, fallback), release.yml (JAR copy), README.
**Why it happens:** Java referenced in 5+ distinct locations across files.
**Consequences:** SKILL.md instructs Claude to detect/prefer Java when no JAR exists.
**Prevention:** Before deleting files, search ALL Java references. Remove atomically: files + references in one operation.
**Detection:** Post-removal grep for `java`, `jar`, `jdk` in all non-CHANGELOG files.
**Confidence:** HIGH -- directly verified in codebase.

---

### Pitfall 5: Config Migration Silently Loses User Credentials

**What goes wrong:** Changing `.chandao/config.properties` to `.worklet/config.properties` means all existing users lose configuration instantly.
**Why it happens:** PROJECT.md says "no backward compat" but users may not remember passwords.
**Consequences:** Users blocked until re-entering credentials. Orphan `.chandao/` with plaintext passwords on disk.
**Prevention:**
1. On first run, check for `.chandao/config.properties`
2. Display one-time migration prompt
3. If confirmed: copy, set 0600 permissions, suggest deleting old file
**Detection:** Check if new config loader includes `.chandao/` fallback.
**Confidence:** HIGH.

---

### Pitfall 6: PyMuPDF AGPL License Contaminates the MIT-Licensed Skill

**What goes wrong:** PyMuPDF/pymupdf4llm is the fastest and highest-quality PDF extractor, making it a tempting choice. But it is licensed under AGPL-3.0, a viral copyleft license. Using it in an MIT-licensed Skill requires either (a) relicensing the entire project under AGPL, or (b) purchasing a commercial license from Artifex.
**Why it happens:** PyMuPDF's AGPL license is easy to miss -- it is often recommended in "best PDF library" articles without mentioning the license implications.
**Consequences:**
- The Skill becomes AGPL-tainted. Users who embed it in proprietary workflows violate the license.
- GitHub issues opened against the project for license incompatibility (documented pattern: browser-use #2610, doctr #486, DeepSeek-OCR #223)
- Artifex actively monitors and enforces AGPL compliance
**Prevention:** Use `pdfplumber` (MIT/BSD licensed) instead. It handles text + table extraction well enough for requirement documents. For scanned PDFs, delegate to Claude's multimodal vision.
**Detection:** `pip show PyMuPDF` should not appear in any environment used by the Skill.
**Confidence:** HIGH -- extensively documented license concern across the Python ecosystem.

---

### Pitfall 7: Python 3.6 Constraint Is Already Broken and Blocks Modern Libraries

**What goes wrong:** PROJECT.md specifies Python 3.6+ citing "enterprise environments." But:
- The codebase already uses `@dataclass` (requires Python 3.7+)
- `python-docx` 1.2.0 requires Python >= 3.9
- `requests` 2.33.x requires Python >= 3.10
- `pdfplumber` requires Python >= 3.8
- Python 3.6 reached EOL in December 2021, 3.7 in June 2023, 3.8 in October 2024, 3.9 in October 2025
**Why it happens:** Constraint set in v1.0 and never validated against actual code or dependency requirements.
**Consequences:** False compatibility claim. Cannot use any modern library without violating the stated constraint.
**Prevention:** Set minimum to Python >= 3.10 for v2.0. This is a major version -- the right time for this change. 3.10 is the oldest version still receiving security patches.
**Detection:** `python3.6 -c "import dataclasses"` fails, proving 3.6 compat is already broken.
**Confidence:** HIGH -- verified against PyPI requirements for all chosen libraries.

---

### Pitfall 8: GitHub Repository Rename Breaks CI/CD and Release Artifacts

**What goes wrong:** Renaming `zulinliu/zentao-workflow` to `zulinliu/worklet` on GitHub causes hidden breakages: release artifact names, directory names in zip, installation docs, GitHub Actions references.
**Why it happens:** GitHub auto-redirects git operations but NOT CI artifact names, release titles, or internal paths.
**Consequences:** Release zip contains `zentao-workflow/` directory. Installation docs point to wrong paths.
**Prevention:** Update release.yml BEFORE (or simultaneously with) the GitHub rename. Rename GitHub LAST.
**Detection:** `grep -r "zentao-workflow" .github/ README.md` should return zero matches before rename.
**Confidence:** HIGH.

---

## Moderate Pitfalls

---

### Pitfall 9: HTML-to-Markdown Replacement Without Test Corpus

**What goes wrong:** Replacing the 40+ regex chain with `markdownify` without a regression test suite. The new converter may handle different edge cases differently.
**Why it happens:** Temptation to just swap the implementation and assume library quality.
**Consequences:** Downloaded requirements have different formatting, broken links, corrupted tables.
**Prevention:**
1. BEFORE replacing, create a test corpus from actual Zentao HTML output (paragraphs, tables, code, images, lists)
2. Write parameterized tests with input HTML -> expected Markdown
3. Run tests against both old regex chain and new markdownify implementation
4. Fix any regressions with custom markdownify converters
**Detection:** Diff output of old vs new converter on the test corpus.
**Confidence:** HIGH.

---

### Pitfall 10: Trigger Keyword Expansion Causes False Activation

**What goes wrong:** Adding generic triggers like "develop", "optimize", "refactor" causes the Skill to activate during unrelated coding conversations.
**Why it happens:** Trying to make the tool more general-purpose with overly broad keywords.
**Consequences:** Skill hijacks unrelated conversations. Users disable it.
**Prevention:**
1. Keep triggers specific: "worklet", "zentao", file path patterns
2. Require compound triggers: "develop requirement" not "develop" alone
3. Test: install skill, have normal coding conversation, verify NO false activation
**Confidence:** HIGH.

---

### Pitfall 11: Streaming Download Creates Partial Files

**What goes wrong:** Switching from `response.content` (atomic) to `stream=True` + `iter_content` introduces partial file corruption when connections drop mid-download.
**Why it happens:** Streaming writes create a file that exists but is truncated.
**Consequences:** Corrupted attachments that look valid (correct filename, non-zero size).
**Prevention:** Atomic write pattern: write to `.tmp`, rename on completion, delete on failure.
**Detection:** Compare `os.path.getsize()` against Content-Length header.
**Confidence:** HIGH.

---

### Pitfall 12: Environment Detection Cache Goes Stale

**What goes wrong:** Cached Python version or superpowers path becomes wrong after system updates.
**Why it happens:** File-based cache has no mechanism to detect environment changes.
**Prevention:**
1. Short TTL (24 hours)
2. Quick validation on cache hit (check if cached binary path exists)
3. `--no-cache` flag for force re-detection
4. Consider: detection takes <1 second. Caching may not be worth the invalidation complexity.
**Confidence:** MEDIUM.

---

### Pitfall 13: `.worklet/` Directory Not in `.gitignore` Leads to Credential Leak

**What goes wrong:** `.worklet/config.properties` with plaintext credentials gets committed.
**Prevention:**
1. Config init step must add `.worklet/` to `.gitignore`
2. Set file permissions 0600 on creation
3. Add warning comment in config file
**Detection:** `git ls-files --cached .worklet/` should return empty.
**Confidence:** HIGH.

---

### Pitfall 14: pdfplumber Pulls Pillow (Large C Extension)

**What goes wrong:** pdfplumber depends on Pillow (10-50MB depending on platform) for its visual debugging feature. This is heavier than expected for "lightweight PDF reading."
**Why it happens:** pdfplumber's table extraction and visual debugging rely on image processing.
**Consequences:** Slower installation, larger footprint, potential build failures on systems without image codec dev headers.
**Prevention:**
1. Accept Pillow as a transitive dependency -- it is widely pre-installed in Python environments
2. If footprint is critical, consider `pypdf` (pure Python, zero deps) as a fallback for environments where pdfplumber installation fails
3. Document the dependency in installation instructions
**Confidence:** MEDIUM -- the trade-off (table extraction quality vs dependency weight) favors pdfplumber for requirement documents that often contain tables.

---

## Minor Pitfalls

---

### Pitfall 15: Filename Sanitization Truncation for Chinese Text

**What goes wrong:** 50-character filename limit is ~16 Chinese characters. Similar long titles may be indistinguishable after truncation.
**Prevention:** Increase to 80 characters, or use ID as primary filename.
**Confidence:** MEDIUM.

---

### Pitfall 16: superpowers Detection Coupled to Installation Path

**What goes wrong:** Detection checks `~/.claude/plugins/cache/...` but npx installation uses a different path.
**Prevention:** Detect by capability (run command, check exit code), not by file path.
**Confidence:** MEDIUM.

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Rename (chandao->worklet) | Pitfall 3: Orphan references | Pre-rename grep checklist; post-rename verification |
| Java removal | Pitfall 4: Leftover Java refs | Atomic: delete files + update references together |
| SKILL.md rewrite | Pitfall 1: Wrong variable syntax | Use `${CLAUDE_SKILL_DIR}` |
| SKILL.md rewrite | Pitfall 2: Description too long | Under 250 chars, third person |
| SKILL.md rewrite | Pitfall 10: Over-triggering | Specific compound keywords |
| Config migration | Pitfall 5: Lost credentials | One-time migration prompt |
| Config migration | Pitfall 13: Credential leak | `.worklet/` in `.gitignore` |
| Env detection | Pitfall 12: Stale cache | TTL + validation |
| Env detection | Pitfall 16: superpowers path | Capability-based detection |
| Code quality | Pitfall 9: HTML converter swap | Test corpus BEFORE changing |
| Code quality | Pitfall 11: Streaming partial files | Atomic write pattern |
| Multi-format support | Pitfall 6: AGPL contamination | Use pdfplumber, NOT PyMuPDF |
| Multi-format support | Pitfall 14: Pillow dependency | Accept or fallback to pypdf |
| Python version | Pitfall 7: False 3.6 claim | Set >= 3.10 for v2.0 |
| GitHub rename | Pitfall 8: CI/CD breakage | Rename last |

## Sources

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [PyMuPDF License Discussion](https://github.com/pymupdf/PyMuPDF/discussions/971)
- [browser-use License Issue #2610](https://github.com/browser-use/browser-use/issues/2610)
- [Python Version Status](https://devguide.python.org/versions/)
- [requests PyPI](https://pypi.org/project/requests/) -- Python 3.10+ requirement
- [python-docx PyPI](https://pypi.org/project/python-docx/) -- Python 3.9+ requirement
- [pdfplumber PyPI](https://pypi.org/project/pdfplumber/)
- [GitHub Docs: Renaming a Repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository)

# Phase 5: SKILL.md Rewrite and Release - Research

**Researched:** 2026-04-05
**Domain:** Claude Code Skill packaging, SKILL.md format, GitHub release automation
**Confidence:** MEDIUM-HIGH

## Summary

Phase 5 requires rewriting SKILL.md with Worklet branding, updating all documentation to v2.0.0, and executing the GitHub release. The core work involves updating trigger keywords from Zentao-specific to generic development terms, replacing all path references with `${CLAUDE_SKILL_DIR}`, and ensuring the skill properly prompts users for input source (Zentao API vs local file). The GitHub release workflow is already configured and functional - only documentation updates are needed.

**Primary recommendation:** Follow the pm-prd-writer SKILL.md format for structure, use `${CLAUDE_SKILL_DIR}` for all path references per D-04, and use the existing release.yml as-is (already correctly configured for worklet packaging).

## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** SKILL.md 触发词使用通用开发关键词：开发需求、优化功能、修复bug、重构、开发、优化（移除 zentao/chandao 等专属词）
- **D-02:** SKILL.md description 单行 <250 字符，英文优先 + 命令式语气
- **D-03:** 所有路径变量改用 `${CLAUDE_SKILL_DIR}`
- **D-04:** 需求入口主动询问用户来源（禅道 API 或本地文件）
- **D-05:** VERSION 和所有文档同步为 2.0.0

### Claude's Discretion
- SKILL.md 内部步骤结构
- 询问用户来源的具体交互方式
- 文档更新的详细程度

### Deferred Ideas
None — final phase

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| SKILL-01 | SKILL.md 全面重写：新名称、新流程、新触发词 | SKILL.md structure confirmed via pm-prd-writer reference |
| SKILL-02 | description 单行 <250 字符，英文优先 + 命令式语气 | pm-prd-writer uses Chinese description; decision D-02 overrides |
| SKILL-03 | 触发词改为通用开发关键词（开发需求/优化功能/修复bug/重构/开发/优化） | D-01 locks specific trigger words |
| SKILL-04 | 所有路径变量改用 ${CLAUDE_SKILL_DIR} | Standard Claude Code variable, confirmed in existing SKILL.md |
| SKILL-05 | 需求入口主动询问用户来源（禅道 API / 本地文件） | New Step 2.5 needed in SKILL.md workflow |
| DOC-01 | CLAUDE.md 全面更新（新项目名、新架构说明、新开发命令） | CLAUDE.md exists, needs full rewrite |
| DOC-02 | CONTRIBUTING.md 更新（移除 Java 构建说明、更新开发流程） | CONTRIBUTING.md exists, remove Java references |
| DOC-04 | assets/tech_plan_template.md 更新为源无关格式 | Template file needs update |
| DOC-05 | references/ 目录审查（保留通用指南，移除或更新 Java 专属内容） | references/ contains Java/React guides |
| REL-01 | VERSION 更新为 2.0.0，全文档版本号同步 | VERSION already shows 2.0.0 |
| REL-02 | CHANGELOG.md 更新 v2.0.0 完整变更记录 | CHANGELOG.md structure verified |
| REL-03 | README.md 全面重写（新名称 Worklet、新功能、新安装说明） | README.md exists, needs full rewrite |
| REL-04 | release.yml CI/CD 更新（移除 Java 相关、更新目录结构和产物名称） | release.yml already updated to worklet |
| REL-05 | GitHub 仓库重命名为 worklet | User action required - cannot be automated |

## Standard Stack

### Claude Code Skill Structure
| Component | Format | Source |
|-----------|--------|--------|
| Skill manifest | SKILL.md with YAML frontmatter | pm-prd-writer reference |
| Entry point variable | `${CLAUDE_SKILL_DIR}` | Standard Claude Code |
| Release automation | `.github/workflows/release.yml` | Already configured |
| Version management | `VERSION` file (SemVer) | Already configured |

### Release Package Contents
```
worklet/
├── SKILL.md              # Skill manifest (required)
├── scripts/              # Built-in tools
│   ├── worklet.py        # CLI entry
│   ├── worklet/          # Python package
│   └── requirements.txt  # Dependencies
├── assets/               # Templates
└── references/          # Analysis guides
```

## Architecture Patterns

### SKILL.md Format (Verified via pm-prd-writer)
```yaml
---
name: {skill-name}
description: |
  {single line <250 chars, describes when to trigger}
  {additional context about what the skill does}
---

# Skill Title

## Section 1
[content]

## Section 2
[content]
```

**Key observations from pm-prd-writer:**
- `name` field: lowercase, hyphens allowed (e.g., `worklet` or `space-prd-writer`)
- `description` field: multi-line, contains trigger conditions and scope
- Main content: Markdown with structured sections

### Path Variable Usage
```bash
# Correct format per D-03
${CLAUDE_SKILL_DIR}/scripts/worklet.py

# Incorrect (old format from current SKILL.md)
{SKILL_DIR}/scripts/worklet.py
```

### GitHub Release Flow
1. Push to `main` branch triggers workflow
2. Read version from `VERSION` file
3. Create `worklet-{version}.zip` package
4. Extract changelog notes for release body
5. Create GitHub release via softprops/action-gh-release@v1

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Skill discovery mechanism | Custom entry point logic | Claude Code built-in `${CLAUDE_SKILL_DIR}` | Platform-provided |
| Release packaging | Custom shell scripts | Existing release.yml | Already configured, tested |
| Version tagging | Manual git tags | release.yml automation | Triggers on main push |
| Changelog generation | Manual release notes | sed-based extraction from CHANGELOG.md | Already in release.yml |

## Common Pitfalls

### Pitfall 1: SKILL.md description too long
**What goes wrong:** Description exceeds 250 characters, causing display issues
**How to avoid:** Keep single line, use pm-prd-writer as length reference (10893 total chars but line is concise)
**Warning signs:** Character count >250 in first line of description

### Pitfall 2: Hardcoded paths instead of ${CLAUDE_SKILL_DIR}
**What goes wrong:** Skill breaks when installed in different location
**How to avoid:** Replace all `{SKILL_DIR}` and hardcoded paths with `${CLAUDE_SKILL_DIR}`
**Warning signs:** Any path starting with `/home/liuzl/agent/` or `~/.claude/`

### Pitfall 3: GitHub repo rename breaks existing URLs
**What goes wrong:** Old GitHub URLs in documentation become 404
**How to avoid:** Update all GitHub URLs from `zulinliu/zentao-workflow` to `zulinliu/worklet`
**Warning signs:** Any URL containing `zentao-workflow`

### Pitfall 4: CHANGELOG entry missing for v2.0.0
**What goes wrong:** Release notes are empty or show wrong content
**How to avoid:** Add complete v2.0.0 entry to CHANGELOG.md before merging to main
**Warning signs:** Unreleased section in CHANGELOG.md

## Code Examples

### SKILL.md name Field Format
```yaml
---
name: worklet
description: |
  Worklet - 从需求到代码一键启动的开发者工作流助手
```

### ${CLAUDE_SKILL_DIR} Usage
```bash
# In SKILL.md steps
python3 ${CLAUDE_SKILL_DIR}/scripts/worklet.py -t story -i 39382

# In Bash commands
cp ${CLAUDE_SKILL_DIR}/assets/config_template.toml ~/.worklet/config.toml
```

### User Source Selection Prompt
```
AskUserQuestion:
  questions:
    - question: "需求从哪里获取？"
      header: "需求来源"
      options:
        - label: "禅道 API"
          description: "从禅道服务器下载需求/任务/Bug"
        - label: "本地文件"
          description: "从本地文件/文件夹读取"
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Zentao-specific triggers | Generic dev triggers | Phase 5 | Broader applicability |
| `{SKILL_DIR}` variable | `${CLAUDE_SKILL_DIR}` | Phase 5 | Standard Claude Code |
| Java + Python runtime | Python only | Phase 1-4 | Simpler, smaller package |
| Zentao workflow focus | Multi-source support | Phase 2-3 | Can handle local files |

**Deprecated/outdated:**
- Java runtime detection code - removed in Phase 4
- Zentao-specific keywords (zentao, chandao) - removed in Phase 5
- `.chandao/config.properties` path - now `.worklet/config.toml`

## Open Questions

1. **GitHub repo rename timing**
   - What we know: REL-05 requires renaming `zentao-workflow` to `worklet` on GitHub
   - What's unclear: Whether this should happen before or after the v2.0.0 release
   - Recommendation: User should rename before Phase 5 execution to ensure URLs are correct

2. **Old release packages**
   - What we know: Previous releases named `zentao-workflow-v*.zip`
   - What's unclear: Whether old releases should be archived or deleted
   - Recommendation: Keep existing releases, new ones will use `worklet-*.zip`

3. **references/ content scope**
   - What we know: references/ contains Java_project_guide.md and react_project_guide.md
   - What's unclear: Whether to keep React guide (still relevant) or remove entirely
   - Recommendation: Keep React guide, remove Java guide (no longer relevant after Java removal)

## Environment Availability

Step 2.6: SKIPPED (no external dependencies for this phase - documentation and release work only)

## Validation Architecture

Step skipped - Phase 5 is documentation/release focused, no code changes requiring tests.

### Phase Requirements -> Test Map (Not Applicable)
This phase involves documentation updates and release automation only. No unit tests required.

## Sources

### Primary (HIGH confidence)
- `~/.claude/skills/pm-prd-writer/SKILL.md` - Verified SKILL.md format
- `.github/workflows/release.yml` - Verified release automation configuration
- `pyproject.toml` - Verified entry points and dependencies

### Secondary (MEDIUM confidence)
- CHANGELOG.md - Verified changelog structure
- release.yml - Verified workflow structure

### Tertiary (LOW confidence)
- Web search for Claude Code SKILL.md format - Unable to find official documentation

## Metadata

**Confidence breakdown:**
- SKILL.md format: HIGH - Verified via live skill example
- Path variable usage: HIGH - Standard Claude Code variable
- Release workflow: HIGH - release.yml already configured correctly
- Trigger keywords: HIGH - Locked by D-01 decision

**Research date:** 2026-04-05
**Valid until:** 90 days (documentation format stable)

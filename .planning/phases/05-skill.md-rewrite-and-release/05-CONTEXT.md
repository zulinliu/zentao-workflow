# Phase 5: SKILL.md Rewrite and Release - Context

**Gathered:** 2026-04-05
**Status:** Ready for planning

<domain>
## Phase Boundary

Rewritten SKILL.md file with Worklet branding, updated docs, CI/CD, changelog, and GitHub repo rename. Phase 5 is the final phase that delivers the complete v2.0.0 release.

</domain>

<decisions>
## Implementation Decisions

### D-01: SKILL.md 触发词
- **决策:** 使用通用开发关键词触发
- **触发词:** 开发需求、优化功能、修复bug、重构、开发、优化
- **移除:** zentao、chandao 等专属词

### D-02: SKILL.md 描述
- **决策:** 单行描述，<250 字符，英文优先
- **描述:** "Worklet - 从需求到代码一键启动的开发者工作流助手"

### D-03: 路径引用
- **决策:** 使用 ${CLAUDE_SKILL_DIR} 引用所有路径
- **替换:** 移除所有硬编码路径

### D-04: 入口询问
- **决策:** 需求入口主动询问用户来源（禅道 API 或本地文件）

### D-05: 版本号
- **决策:** VERSION 和所有文档同步为 2.0.0

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — SKILL-01~05, DOC-01~02, DOC-04~05, REL-01~05
- `.planning/ROADMAP.md` §Phase 5 — Phase 5 目标、成功标准

### Prior Phase Context
- `.planning/phases/01-foundation-and-rename/01-CONTEXT.md`
- `.planning/phases/02-core-pipeline/02-CONTEXT.md`
- `.planning/phases/03-extended-sources-and-testing/03-CONTEXT.md`
- `.planning/phases/04-pipeline-assembly-and-cli/04-CONTEXT.md`

</canonical_refs>

<deferred>
## Deferred Ideas

None — this is the final phase

</deferred>

---

*Phase: 05-skill-md-rewrite-and-release*
*Context gathered: 2026-04-05*

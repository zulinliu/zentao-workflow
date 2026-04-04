# Worklet - 开发工作流助手

## What This Is

Worklet (Workflow + Applet) 是一个 Claude Code Skill，为开发者提供轻量级的开发工作流自动化。它从多种来源（禅道 API、本地文件/文件夹）获取需求/任务/Bug 文档，结合项目代码自动生成技术实现方案，并驱动编码执行。v2.0.0 从"禅道专用工具"升级为"通用开发工作流助手"。

## Core Value

**让开发者从需求到代码一键启动**——无论需求来自禅道系统还是本地文档，都能自动读取、理解、并生成可执行的技术实现方案。

## Requirements

### Validated

- ✓ Python 版禅道 API 客户端（登录、查看、下载） — v1.0
- ✓ Story/Task/Bug 下载及 Markdown 导出 — v1.0
- ✓ 附件和内嵌图片下载 — v1.0
- ✓ 工作区配置优先级（工作区 > 全局） — v1.3
- ✓ superpowers:brainstorming 集成生成技术方案 — v1.5
- ✓ 子任务检测与关联内容下载 — v1.6

### Active

- [ ] 项目全面重命名：zentao-workflow → Worklet，chandao_fetch → worklet
- [ ] 删除 Java 版本：JAR、源码、所有 Java 相关引用
- [ ] 多源需求入口：禅道 API + 文件/文件夹（Markdown/PDF/Word/图片）
- [ ] 通用触发关键词：开发需求/优化功能/修复bug/重构/开发/优化等
- [ ] 环境检测优化：先试后检 + 缓存标记（`.worklet/config.properties`）
- [ ] 配置/存储目录迁移：`.chandao/` → `.worklet/`（项目根优先 → `~/.worklet/`）
- [ ] superpowers 安装方式升级为 npx
- [ ] 修复 client.py：download timeout、流式大文件下载、具体异常类型
- [ ] 修复 service.py：移除无用 re.findall、并发附件下载
- [ ] 修复 config.py：文件权限 0600、配置校验
- [ ] 修复 exporter.py：HTML→Markdown 用 html.parser 替代 40+ 正则
- [ ] 子任务检测逻辑从 SKILL.md 下沉到 Python 代码
- [ ] SKILL.md 全面重写：新流程、新触发词、移除 Java 引用
- [ ] `.worklet/` 加入 `.gitignore` 保护
- [ ] Python 单元测试（client/service/exporter/config）
- [ ] 全量代码审计并修复所有已知问题（16 项）
- [ ] GitHub 仓库重命名为 worklet

### Out of Scope

- v1.x 旧配置兼容（`.chandao/`） — 大版本升级，不做向后兼容
- Java 版本维护 — v2.0 彻底移除
- 禅道写操作（创建/更新/删除） — 安全约束，只读
- 实时同步/Webhook — 超出 Skill 工具定位
- 项目级批量下载（`fetchProject`） — 复杂度高，延后
- GUI 界面 — CLI Skill 定位

## Context

**技术环境：**
- 运行时：Python 3.6+（v2.0 移除 Java）
- 依赖：requests (HTTP)、html.parser (HTML 解析)
- Skill 框架：Claude Code Skill (SKILL.md YAML frontmatter)
- 集成：superpowers 插件（brainstorming、subagent-driven-development）

**前身：**
- 项目原名 zentao-workflow，v1.0-v1.6 专注禅道系统集成
- v2.0 扩展为通用开发工作流，支持多种需求来源

**现有代码库状态：**
- Python 模块：`scripts/chandao_fetch/`（6 个文件）— 需全面重命名
- Java 模块：`scripts/java-src/` + `chandao-fetch.jar` — 需完全删除
- SKILL.md：600+ 行 — 需全面重写
- 无 Python 测试 — 需新建

**已知问题（v2.0 修复清单）：**
1. client.py download 无 timeout，大文件整体加载内存
2. service.py 无用 re.findall、附件串行下载
3. config.py 无权限保护、无配置校验
4. exporter.py 40+ 正则链脆弱
5. 版本号不一致（VERSION vs README）
6. 子任务检测逻辑在 SKILL 层而非代码层

## Constraints

- **运行时**: Python 3.6+ — 需保持低版本兼容（企业环境）
- **安全**: API 客户端只读操作，密码文件 0600 权限
- **依赖**: 仅 `requests` 库，避免引入重量级依赖
- **Skill 体积**: 移除 Java 后应显著减小 release 包体积
- **命名**: 所有 chandao/zentao 命名统一改为 worklet

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 移除 Java 版本 | 减少维护成本，Python 已足够稳定 | — Pending |
| 配置目录 .worklet/ | 与新品牌一致，项目根优先 | — Pending |
| 不兼容 v1.x | 大版本升级，减少迁移代码复杂度 | — Pending |
| superpowers 用 npx 安装 | 比 `claude plugins add` 更稳定 | — Pending |
| HTML 解析用 html.parser | 标准库自带，无需额外依赖 | — Pending |
| 文件入口支持 MD/PDF/Word/图片 | 覆盖主流需求文档格式 | — Pending |
| GitHub 仓库重命名 | 与项目新定位一致 | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-04 after initialization*

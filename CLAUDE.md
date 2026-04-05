# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## 项目说明

这是一个 Claude Code Skill 项目，用于自动化开发需求/任务/Bug 下载与技术实现方案设计。v2.0.0 从"禅道专用工具"升级为"通用开发工作流助手"。

## 版本信息

- **版本**: 2.0.0
- **作者**: liuzl
- **许可证**: MIT

## 开发命令

### Python 版本测试

```bash
cd scripts
pip install -r requirements.txt
python3 -m worklet -t bug -i 66445 -o /tmp/test-output
python3 -m worklet -t story -i 39382 -o /tmp/test-output
python3 -m worklet -t task -i 61215 -o /tmp/test-output
```

## 架构说明

### 技能执行流程（SKILL.md v2.0.0）

1. **Step 1: 环境检测** - 检测 Python 和 superpowers 技能依赖
2. **Step 2: 配置初始化** - 检查配置文件，引导用户创建
3. **Step 2.5: 需求来源选择** - 询问用户从禅道 API 还是本地文件获取
4. **Step 3: 获取需求内容** - 从禅道 API 或本地文件获取
5. **Step 4: 技术实现方案设计** - 调用 superpowers:brainstorming 生成方案
6. **Step 5: 输出方案** - 展示方案摘要
7. **Step 6: 开始编码** - 调用 superpowers:subagent-driven-development 或 executing-plans

### v2.0.0 核心变更

| 指标 | v1.6.x | v2.0.0 | 提升 |
|------|--------|--------|------|
| 需求来源 | 禅道 API | 禅道 API + 本地文件 | 多源支持 |
| 触发词 | 禅道专属 | 通用开发关键词 | 广泛适用 |
| 运行时 | Java + Python | Python only | 轻量化 |

### Python 模块架构

```
scripts/worklet/
├── __main__.py    # CLI 入口
├── config.py      # 配置管理（读取 .worklet/config.toml）
├── client.py      # API 客户端（只读操作，禁止写操作）
├── models.py      # 数据模型（Story/Task/Bug/Attachment）
├── service.py     # 业务逻辑（下载+附件处理）
└── exporter.py    # Markdown 导出（处理图片路径转换）
```

**安全约束**: WorkletClient 只支持只读操作（登录、查看、下载），禁止创建/更新/删除。

## 关键技术点

### 附件路径处理

- MD 文件位置: `{output}/{type}/{id}-title.md`
- 附件目录: `{output}/attachments/{type}/{id}/`
- **相对路径**: `../attachments/{type}/{id}/filename`

### 内嵌图片下载

- 从内容中提取 `<img src="...">` 标签
- 自动下载图片到附件目录
- 转换为 Markdown 格式: `![](../attachments/...)`

### 配置文件

- 位置: `~/.worklet/config.toml`（全局）或 `.worklet/config.toml`（项目级）
- 格式: TOML
- 优先级: 命令行 > 配置文件 > 默认值

## 修改 SKILL.md 注意事项

1. **触发条件**在 YAML frontmatter 的 `description` 字段
2. **步骤编号**保持连续（Step 1, Step 2...）
3. **占位符**使用 `{变量名}` 格式
4. **示例**使用通用值，不要包含真实敏感信息

## 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 下载失败 | 网络问题 | 检查禅道服务器是否可达 |
| 登录失败 | 账号密码错误 | 检查配置文件中的凭据 |
| ID 不存在 | 无权限或已删除 | 确认 ID 正确且有访问权限 |
| 附件下载失败 | 权限不足 | 检查输出目录写入权限 |
| superpowers 未安装 | 新环境 | 执行 `claude plugins add official superpowers` |

## 项目管理规范

> 详细规范见 [CONTRIBUTING.md](CONTRIBUTING.md)

### 分支策略

| 分支 | 用途 | 约束 |
|------|------|------|
| `main` | 生产分支 | 仅接受来自 dev 的 PR，合并后自动发版 |
| `dev` | 开发分支 | 日常开发在此进行 |

### 开发流程

```
feature/xxx → dev → (评审通过) → main → (自动发版)
```

### 关键约束

1. **CLAUDE.md 等开发文件** → 只提交到 dev，**禁止合并到 main**
2. **版本号管理** → 遵循语义化版本（SemVer），修改 VERSION 文件
3. **CHANGELOG** → 每次发版必须更新
4. **提交消息** → 使用规范格式：`feat:` / `fix:` / `docs:` / `release:`

### 发版检查清单

- [ ] VERSION 文件已更新
- [ ] CHANGELOG.md 已更新
- [ ] README.md 版本徽章已更新
- [ ] SKILL.md 版本号已更新
- [ ] 代码已评审通过
- [ ] 从 dev 合并到 main（自动触发发版）

## 提交规范

```bash
git commit -m "feat: 功能描述"   # 功能更新
git commit -m "fix: 修复描述"    # 问题修复
git commit -m "docs: 文档描述"   # 文档更新
git commit -m "release: v2.0.0"  # 版本发布
```

## 依赖说明

### 运行时依赖

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Python | 3.10+ | 运行时 |
| superpowers 插件 | 5.0.6+ | 技术方案设计必需 |

### 安装 superpowers

```bash
claude plugins add official superpowers
```

<!-- GSD:project-start source:PROJECT.md -->
## Project

**Worklet - 开发工作流助手**

Worklet (Workflow + Applet) 是一个 Claude Code Skill，为开发者提供轻量级的开发工作流自动化。它从多种来源（禅道 API、本地文件/文件夹）获取需求/任务/Bug 文档，结合项目代码自动生成技术实现方案，并驱动编码执行。v2.0.0 从"禅道专用工具"升级为"通用开发工作流助手"。

**Core Value:** **让开发者从需求到代码一键启动**——无论需求来自禅道系统还是本地文档，都能自动读取、理解、并生成可执行的技术实现方案。

### Constraints

- **运行时**: Python 3.10+ — v2.0 移除 Java
- **安全**: API 客户端只读操作，密码文件 0600 权限
- **依赖**: 仅 `requests` 库，避免引入重量级依赖
- **Skill 体积**: 移除 Java 后显著减小 release 包体积
- **命名**: 所有 chandao/zentao 命名统一改为 worklet
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.10+ - Core download tools and CLI implementation (`scripts/worklet/`)
- YAML - Skill manifest and CI/CD configuration
- Markdown - Documentation and output format
## Runtime
- Python 3.10+ - Runtime requirement
- superpowers 5.0.6+ (Claude Code plugin, required for technical plan generation)
- pip/pip3 (Python package manager)
- Lockfile: Python uses `scripts/requirements.txt`
## Frameworks
- requests 2.32.0+ (HTTP client for Python downloads, `scripts/worklet/client.py`)
- Python argparse (standard library, native CLI parsing in `scripts/worklet/__main__.py`)
- markdownify 0.18.0+ (HTML to Markdown conversion)
- tomli 2.0.0+ / tomli-w 1.0.0+ (TOML configuration)
## Key Dependencies
- requests 2.32.0+ (Python) - HTTP communication with Zentao API
- tomli 2.0.0+ (Python) - TOML reading for Python < 3.11
- tomli-w 1.0.0+ (Python) - TOML writing
- markdownify 0.18.0+ (Python) - HTML to Markdown conversion
## Configuration
- Configuration file: `.worklet/config.toml` (project-local) or `~/.worklet/config.toml` (global)
- Format: TOML format
- Priority order: Command-line arguments > workspace config > global config > defaults
- GitHub Actions: `.github/workflows/release.yml` (automated release packaging)
- Version: `VERSION` file (semantic versioning)
## Platform Requirements
- Python 3.10+ (for running Python version or development)
- Git (for version control)
- No external database or services required beyond Zentao API access
- superpowers plugin 5.0.6+ (Claude Code Skill dependency)
- Read/write access to workspace directory for outputs
- Network access to Zentao API endpoints (HTTP/HTTPS)
- Optional: Write access to `~/.worklet/` for global configuration storage
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- Python modules: snake_case (e.g., `worklet.py`, `client.py`, `exporter.py`)
- Test files: Python follows `{ModuleName}_test.py` pattern
- Python: snake_case (e.g., `export_story()`, `_download_attachments()`, `_process_content()`)
- Private methods prefixed with underscore
- Python: snake_case (e.g., `base_url`, `output_dir`, `connect_timeout`)
- Python: Python dataclasses with `str | None` for nullable fields
## Code Style
- Python: 4-space indentation per PEP 8
- Both: UTF-8 encoding enforced
- Both: Unix line endings (LF)
- Python: No linting tools configured; follows PEP 8 conventions informally
- Both: Documentation strings and comments wrap reasonably
- Python: Uses f-strings for string formatting (e.g., `f"{story.id} - {story.title}"`)
## Import Organization
- Python: Relative imports within package (e.g., `from .config import WorkletConfig`)
## Error Handling
- Python: Raises generic `Exception` with descriptive messages
- `__main__.main()` (Python): Catches and prints error messages; uses `--verbose` to show tracebacks
- Service layer (`WorkletService`, `service.py`): Catches attachment/image download failures but logs and continues
## Logging
- Python: `print()` statements, no structured logging framework
- Python: Direct `print()` statements to stdout for user feedback
## Comments
- Python: Module-level docstring at top (e.g., `"""Worklet - CLI entry module"""`)
- Python: Method docstrings with Args and Returns sections (Google style)
## Function Design
- Python: Functions under 80 lines; content processing delegated to exporter
- Python: Use dataclass models for data transfer; explicit keyword arguments for options
- Python: Return tuples or dataclass instances; raise Exception for errors rather than returning None
## Module Design
- Python: Explicit imports in `__main__.py`
- Python `__init__.py` is minimal (no re-exports)
## Configuration Management
## Security Constraints
- All API clients restricted to read-only: login, view details, download attachments
- Explicitly documented in code comments
- No write operations (create, update, delete, assign, close) implemented
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern Overview
- Client-server architecture for Zentao API interaction
- Layered service pattern with clear separation of concerns
- Source abstraction (ZentaoSource / FileSource)
- Read-only safety constraints on API client operations
- Modular markdown generation with content transformation pipeline
## Layers
- **CLI**: Parse and validate command-line arguments, handle user input. Location: `scripts/worklet/__main__.py`. Depends on: Configuration, Service layers.
- **Configuration**: Load and manage credentials, settings, and workspace configuration. Location: `scripts/worklet/config.py`. Format: TOML.
- **Client**: Interact with Zentao API endpoints securely (read-only operations only). Location: `scripts/worklet/client.py`. Depends on: HTTP library (requests), configuration. **Safety Constraint**: Only supports login, view, and download operations; explicitly blocks create/update/delete.
- **Models**: Represent domain entities (Story, Task, Bug, Attachment). Location: `scripts/worklet/models.py`.
- **Service**: Orchestrate data download, file attachment processing, and content transformation. Location: `scripts/worklet/service.py`.
- **Exporter**: Transform domain models to Markdown files with embedded attachments and images. Location: `scripts/worklet/exporter.py`.
## Data Flow
- **Configuration state**: Loaded once at startup, immutable during execution
- **Session state**: HTTP session maintained in WorkletClient, persists login cookie for multiple requests
- **Model state**: In-memory representations of Story/Task/Bug entities during processing
- **File I/O state**: Filesystem operations are append-only and idempotent (safe for retries)
## Key Abstractions
- **Source Types**: Handle Story, Task, Bug, and LocalFile as variants with common interface. Examples: `scripts/worklet/service.py` (ZentaoSource, FileSource).
- **Multi-source Configuration**: Support multiple deployment scenarios. Examples: `scripts/worklet/config.py` (WorkletConfig.load() method).
- **Path Handling**: Handle relative and absolute path transformations for attachment references. Examples: `scripts/worklet/exporter.py` (MarkdownExporter._process_content, image URL transformation).
- **Resource Extraction**: Extract, download, and transform embedded resources. Examples: Image extraction in `scripts/worklet/service.py`.
## Entry Points
- Location: `scripts/worklet/__main__.py` (main() function)
- Triggers: Direct execution via `python3 -m worklet -t story -i 39382`
- Responsibilities: Parse CLI args, instantiate WorkletConfig, create WorkletService, execute download
- Location: `SKILL.md` (orchestration steps)
- Triggers: User mentions "开发需求", "优化功能", "修复bug", "重构", etc.
- Responsibilities: Environment detection, configuration guidance, invoke Python runtime
## Error Handling
- **Configuration errors**: Check `is_initialized()` before execution; if false, print configuration prompt and exit with code 1
- **Network errors**: Catch connection timeouts and HTTP errors; wrap in Exception with context
- **File I/O errors**: Attachment download failures log but continue (non-blocking); file write failures propagate
- **Parsing errors**: JSON deserialization errors caught and logged with ID/type context
- **Subtask handling**: If task description is empty (detected by missing `## 任务描述` in markdown), auto-detect parent task and associated story, recursively download related content
## Cross-Cutting Concerns
- Python: `print()` statements to stdout (logs go to SKILL execution context)
- CLI validation: Check required parameters (`-t`, `-i` or `--ids`)
- Configuration validation: Ensure base_url, username, password are present before API calls
- Content validation: Verify JSON response status/result fields before model deserialization
- POST login with username/password to `/user-login.json`
- Response contains session cookie (auto-managed by requests)
- Subsequent API calls use authenticated session
- No persistent token storage; login happens per execution session
- Markdown filenames follow pattern: `{id}-{sanitized-title}.md`
- Attachment paths always relative: `../attachments/{type}/{id}/{filename}`
- Line endings and encoding: UTF-8 with LF (cross-platform)
- Safe filename sanitization: Remove/replace invalid characters
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd:profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->

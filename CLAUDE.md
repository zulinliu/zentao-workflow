# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## 项目说明

这是一个 Claude Code Skill 项目，用于自动化禅道需求/任务/Bug 下载与技术实现方案设计。

## 版本信息

- **版本**: 1.6.0
- **作者**: liuzl
- **许可证**: MIT

## 开发命令

### Java 版本构建

```bash
# 在 scripts/java-src 目录中执行
cd scripts/java-src
mvn clean package -DskipTests

# 复制 JAR 到 scripts 目录
cp target/chandao-fetch.jar ../
```

### Python 版本测试

```bash
cd scripts
pip install -r requirements.txt
python3 chandao_fetch.py -t bug -i 66445 -o /tmp/test-output
python3 chandao_fetch.py -t story -i 39382 -o /tmp/test-output
python3 chandao_fetch.py -t task -i 61215 -o /tmp/test-output
```

## 架构说明

### 技能执行流程（SKILL.md v1.5.0）

1. **Step 1: 环境检测** - 检测 Java/Python 和 superpowers 技能依赖
2. **Step 2: 配置初始化** - 检查配置文件，引导用户创建
3. **Step 3: 下载内容** - 调用内置工具下载需求/任务/Bug 及附件
4. **Step 4: 技术实现方案设计** - 调用 superpowers:brainstorming 生成方案
5. **Step 5: 输出方案** - 展示方案摘要
6. **Step 6: 开始编码** - 调用 superpowers:subagent-driven-development 或 executing-plans

### v1.5.0 核心变更

| 指标 | v1.4.x | v1.5.0 | 提升 |
|------|--------|--------|------|
| 设计阶段 | 3 个（架构+输出+编码） | 1 个（技术实现方案） | -67% |
| 代理数量 | 12-17 个 | 1-2 个 | -85%+ |
| 简单需求耗时 | 20+ 分钟 | 5-8 分钟 | -70%+ |

### Python 模块架构

```
scripts/chandao_fetch/
├── __main__.py    # CLI 入口
├── config.py      # 配置管理（读取 ~/.chandao/config.properties）
├── client.py      # API 客户端（只读操作，禁止写操作）
├── models.py      # 数据模型（Story/Task/Bug/Attachment）
├── service.py     # 业务逻辑（下载+附件处理）
└── exporter.py    # Markdown 导出（处理图片路径转换）
```

**安全约束**: ChandaoClient 只支持只读操作（登录、查看、下载），禁止创建/更新/删除。

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

- 位置: `~/.chandao/config.properties`
- 格式: Java Properties
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
git commit -m "release: v1.5.0"  # 版本发布
```

## 依赖说明

### 运行时依赖

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Java | 8+ | 优先使用 |
| Python | 3.6+ | 默认备选 |
| superpowers 插件 | 5.0.6+ | v1.5.0 技术方案设计必需 |

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

- **运行时**: Python 3.6+ — 需保持低版本兼容（企业环境）
- **安全**: API 客户端只读操作，密码文件 0600 权限
- **依赖**: 仅 `requests` 库，避免引入重量级依赖
- **Skill 体积**: 移除 Java 后应显著减小 release 包体积
- **命名**: 所有 chandao/zentao 命名统一改为 worklet
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.6+ - Core download tools and CLI implementation (`scripts/chandao_fetch/`)
- Java 8+ - Alternative runtime for fetch tool (`scripts/java-src/`)
- YAML - Skill manifest and CI/CD configuration
- Markdown - Documentation and output format
## Runtime
- Java 8+ (optional, for better performance) - Primary choice when available
- Python 3.6+ (default fallback) - Lightweight alternative
- superpowers 5.0.6+ (Claude Code plugin, required for v1.5.0+ technical plan generation)
- Maven 3.6+ (Java build, `scripts/java-src/pom.xml`)
- pip/pip3 (Python package manager)
- Lockfile: Python uses `scripts/requirements.txt`
## Frameworks
- requests 2.28.0+ (HTTP client for Python downloads, `scripts/chandao_fetch/client.py`)
- OkHttp 4.12.0 (Java HTTP client, see `scripts/java-src/pom.xml`)
- jcommander 1.82 (Java CLI argument parsing)
- Python argparse (standard library, native CLI parsing in `scripts/chandao_fetch/__main__.py`)
- Jackson 2.15.2 (Java JSON serialization/deserialization)
- requests JSON handling (Python native)
- SLF4J 2.0.9 + Logback 1.3.11 (Java structured logging)
- Python print statements (simple console logging in all modules)
- Apache Commons Lang3 3.13.0 (Java string and object utilities)
## Key Dependencies
- requests 2.28.0+ (Python) - HTTP communication with Zentao API, only requirement in `scripts/requirements.txt`
- OkHttp 4.12.0 (Java) - HTTP requests in `scripts/java-src/`
- Jackson databind 2.15.2 (Java) - JSON parsing for API responses in `scripts/java-src/`
- Maven Compiler Plugin 3.11.0 - Java compilation targeting JDK 1.8
- Maven Shade Plugin 3.5.1 - Fat JAR generation for standalone execution
- Maven Assembly Plugin 3.6.0 - Distribution packaging
- JUnit 4.13.2 (Java unit testing)
- Mockito 4.11.0 (Java mocking framework)
- OkHttp MockWebServer 4.12.0 (Java HTTP mocking)
- JaCoCo 0.8.11 (Java code coverage - 85% line coverage, 60% branch coverage enforced in `scripts/java-src/pom.xml`)
- Maven Surefire 3.1.2 (Java test execution)
## Configuration
- Configuration file: `~/.chandao/config.properties` (global) or `.chandao/config.properties` (workspace-local)
- Format: Java Properties format (key=value)
- Priority order: Command-line arguments > workspace config > global config > defaults
- Maven configuration: `scripts/java-src/pom.xml` (builds to `scripts/chandao-fetch.jar`)
- GitHub Actions: `.github/workflows/release.yml` (automated release packaging)
- Version: `VERSION` file (semantic versioning)
## Platform Requirements
- Java 8+ (for building Java version)
- Python 3.6+ (for running Python version or development)
- Maven 3.6+ (for Java builds)
- Git (for version control)
- Java 8+ OR Python 3.6+ (mutually exclusive, tool auto-selects Java if available)
- No external database or services required beyond Zentao API access
- superpowers plugin 5.0.6+ (Claude Code Skill dependency for v1.5.0+)
- Read/write access to workspace directory for outputs
- Network access to Zentao API endpoints (HTTP/HTTPS)
- Optional: Write access to `~/.chandao/` for global configuration storage
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- Java classes: PascalCase (e.g., `ChandaoClient.java`, `MarkdownExporter.java`)
- Python modules: snake_case (e.g., `chandao_fetch.py`, `client.py`, `exporter.py`)
- Test files: Java follows `{ClassName}Test.java` and `{ClassName}EdgeCaseTest.java`; Python has no test files in repo
- Java: camelCase (e.g., `exportStory()`, `parseAttachments()`, `sanitizeFileName()`)
- Python: snake_case (e.g., `export_story()`, `_download_attachments()`, `_process_content()`)
- Private methods prefixed with underscore in both languages
- Java: camelCase (e.g., `baseUrl`, `outputDir`, `connectTimeout`)
- Python: snake_case (e.g., `base_url`, `output_dir`, `connect_timeout`)
- Constants in Java: UPPER_SNAKE_CASE (e.g., `DEFAULT_CONFIG_FILE`)
- Java: Model classes use wrapper types and generics
- Python: Python dataclasses with `Optional[T]` for nullable fields
## Code Style
- Java: Standard Java formatting (4-space indentation)
- Python: 4-space indentation per PEP 8
- Both: UTF-8 encoding enforced
- Both: Unix line endings (LF)
- Java: Maven compiler enforces Java 1.8 target (`<maven.compiler.target>1.8</maven.compiler.target>`)
- Python: No linting tools configured; follows PEP 8 conventions informally
- Java: JaCoCo code coverage checking enforced in pom.xml with minimum line coverage of 85%
- Both: Documentation strings and comments wrap reasonably
- Python: Uses f-strings for string formatting (e.g., `f"{story.id} - {story.title}"`)
## Import Organization
- Java: No aliases, uses full package names
- Python: Relative imports within package (e.g., `from .config import ChandaoConfig`)
- Java (`ChandaoClient.java`):
- Python (`client.py`):
## Error Handling
- Java: Throws checked exceptions; callers decide handling
- Python: Raises generic `Exception` with descriptive messages
- `ChandaoFetchApplication.main()` (Java): Top-level try-catch logs and exits with code 1
- `__main__.main()` (Python): Catches and prints error messages; uses `--verbose` to show tracebacks
- Service layer (`ChandaoService`, `service.py`): Catches attachment/image download failures but logs and continues
## Logging
- Java: SLF4J with Logback backend (`logback.xml` configured in pom.xml)
- Python: `print()` statements, no structured logging framework
- Java logging levels:
- Example from `ChandaoClient.java`:
- Python: Direct `print()` statements to stdout for user feedback
## Comments
- Java: Class-level JavaDoc for public classes (e.g., `/** 禅道API客户端 */`)
- Java: Method-level JavaDoc for public methods with detailed parameter descriptions
- Python: Module-level docstring at top (e.g., `"""禅道数据抓取工具 - API客户端模块"""`)
- Python: Method docstrings with Args and Returns sections (Google style)
## Function Design
- Java: Methods stay under 100 lines; parsing logic broken into helpers (`parseAttachments()`, `fetchJson()`)
- Python: Functions under 80 lines; content processing delegated to exporter
- Java: Use builder patterns for command-line args; limit method parameters to 5 or fewer
- Python: Use dataclass models for data transfer; explicit keyword arguments for options
- Java: Explicit null checks before returning; use Optional-like patterns sparingly
- Python: Return tuples or dataclass instances; raise Exception for errors rather than returning None
- Java (`CommandLineArgs.getIdList()`):
- Python (`__main__.main()`):
## Module Design
- Java: All public classes exported; package structure mirrors functionality
- Python: Explicit imports in `__main__.py`
- Not used; imports are explicit and direct
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
- Client-server architecture for Zentao (禅道) API interaction
- Layered service pattern with clear separation of concerns
- Plugin-based execution (supports both Java and Python implementations)
- Read-only safety constraints on API client operations
- Modular markdown generation with content transformation pipeline
## Layers
- Purpose: Parse and validate command-line arguments, handle user input
- Location: 
- Contains: Argument parsing, validation, error handling
- Depends on: Configuration, Service layers
- Used by: End users, Claude Code Skill orchestration
- Purpose: Load and manage credentials, settings, and workspace configuration
- Location:
- Contains: Config file parsing (Java Properties format), multi-level config resolution
- Depends on: Filesystem access
- Used by: CLI, Service layers
- Purpose: Interact with Zentao API endpoints securely (read-only operations only)
- Location:
- Contains: HTTP session management, authentication, API calls for Story/Task/Bug retrieval
- Depends on: HTTP library (requests/OkHttp), configuration
- Used by: Service layer
- **Safety Constraint**: Only supports login, view, and download operations; explicitly blocks create/update/delete
- Purpose: Represent domain entities (Story, Task, Bug, Attachment)
- Location:
- Contains: Dataclass/POJO definitions with JSON deserialization
- Depends on: None (self-contained)
- Used by: Client and Service layers
- Purpose: Orchestrate data download, file attachment processing, and content transformation
- Location:
- Contains: Multi-ID handling, attachment download, embedded image extraction and transformation
- Depends on: Client, Models, Exporter layers
- Used by: CLI, SKILL orchestration
- Purpose: Transform domain models to Markdown files with embedded attachments and images
- Location:
- Contains: Markdown generation, path transformation (relative path calculation for attachments)
- Depends on: Models, Filesystem
- Used by: Service layer
## Data Flow
```
```
- **Configuration state**: Loaded once at startup, immutable during execution
- **Session state**: HTTP session maintained in ChandaoClient, persists login cookie for multiple requests
- **Model state**: In-memory representations of Story/Task/Bug entities during processing
- **File I/O state**: Filesystem operations are append-only and idempotent (safe for retries)
## Key Abstractions
- Purpose: Handle Story, Task, and Bug as variants with common interface
- Examples: `scripts/chandao_fetch/models.py` (Story, Task, Bug classes), `scripts/java-src/src/main/java/com/tsintergy/chandao/model/`
- Pattern: Each model type has specific fields but all support export to Markdown. Service layer dispatches to type-specific handlers.
- Purpose: Support multiple deployment scenarios (workspace-specific vs. global configuration)
- Examples: `scripts/chandao_fetch/config.py` (ChandaoConfig.load() method)
- Pattern: Priority chain - command line > workspace config > global config > defaults. Workspace config stored in `.chandao/config.properties`, global in `~/.chandao/config.properties`.
- Purpose: Handle relative and absolute path transformations for attachment references
- Examples: `scripts/chandao_fetch/exporter.py` (MarkdownExporter._process_content, image URL transformation)
- Pattern: Absolute URLs from API converted to relative markdown paths (`../attachments/{type}/{id}/filename`)
- Purpose: Extract, download, and transform embedded resources
- Examples: Image extraction regex in `scripts/chandao_fetch/service.py`, markdown generation in exporter
- Pattern: Extract `<img src="...">` → download file → update URL → generate markdown reference
## Entry Points
- Location: `scripts/chandao_fetch/__main__.py` (main() function)
- Triggers: Direct execution via `python3 chandao_fetch.py -t story -i 39382`
- Responsibilities: Parse CLI args, instantiate ChandaoConfig, create ChandaoService, execute download
- Location: `scripts/java-src/src/main/java/com/tsintergy/chandao/ChandaoFetchApplication.java` (main() method)
- Triggers: Direct execution via `java -jar chandao-fetch.jar -t story -i 39382`
- Responsibilities: Parse JCommander args, load config with workspace awareness, instantiate service, handle exceptions
- Location: `SKILL.md` (orchestration steps)
- Triggers: User mentions "禅道", "需求", "任务", "Bug", etc.
- Responsibilities: Environment detection, configuration guidance, invoke appropriate runtime version
## Error Handling
- **Configuration errors**: Check `is_initialized()` before execution; if false, print configuration prompt and exit with code 1
- **Network errors**: Catch connection timeouts and HTTP errors; wrap in Exception with context (e.g., "登录失败: HTTP 401")
- **File I/O errors**: Attachment download failures log but continue (non-blocking); file write failures propagate
- **Parsing errors**: JSON deserialization errors caught and logged with ID/type context
- **Subtask handling** (v1.6.0): If task description is empty (detected by missing `## 任务描述` in markdown), auto-detect parent task and associated story, recursively download related content
## Cross-Cutting Concerns
- Python: `print()` statements to stdout (logs go to SKILL execution context)
- Java: SLF4J + Logback configuration in `scripts/java-src/src/main/resources/logback.xml`
- CLI validation: Check required parameters (`-t`, `-i` or `--ids`)
- Configuration validation: Ensure base_url, username, password are present before API calls
- Content validation: Verify JSON response status/result fields before model deserialization
- POST login with username/password to `/user-login.json`
- Response contains session cookie (auto-managed by requests/OkHttp)
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

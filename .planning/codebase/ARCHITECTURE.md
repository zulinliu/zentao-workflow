# Architecture

**Analysis Date:** 2026-04-04

## Pattern Overview

**Overall:** Dual-runtime data extraction and content generation pipeline with superpowers skill integration

**Key Characteristics:**
- Client-server architecture for Zentao (禅道) API interaction
- Layered service pattern with clear separation of concerns
- Plugin-based execution (supports both Java and Python implementations)
- Read-only safety constraints on API client operations
- Modular markdown generation with content transformation pipeline

## Layers

**CLI (Command Line Interface):**
- Purpose: Parse and validate command-line arguments, handle user input
- Location: 
  - Python: `scripts/chandao_fetch/__main__.py`
  - Java: `scripts/java-src/src/main/java/com/tsintergy/chandao/cli/CommandLineArgs.java`
- Contains: Argument parsing, validation, error handling
- Depends on: Configuration, Service layers
- Used by: End users, Claude Code Skill orchestration

**Configuration Layer:**
- Purpose: Load and manage credentials, settings, and workspace configuration
- Location:
  - Python: `scripts/chandao_fetch/config.py`
  - Java: `scripts/java-src/src/main/java/com/tsintergy/chandao/config/ChandaoConfig.java`
- Contains: Config file parsing (Java Properties format), multi-level config resolution
- Depends on: Filesystem access
- Used by: CLI, Service layers

**API Client Layer:**
- Purpose: Interact with Zentao API endpoints securely (read-only operations only)
- Location:
  - Python: `scripts/chandao_fetch/client.py`
  - Java: `scripts/java-src/src/main/java/com/tsintergy/chandao/client/ChandaoClient.java`
- Contains: HTTP session management, authentication, API calls for Story/Task/Bug retrieval
- Depends on: HTTP library (requests/OkHttp), configuration
- Used by: Service layer
- **Safety Constraint**: Only supports login, view, and download operations; explicitly blocks create/update/delete

**Data Model Layer:**
- Purpose: Represent domain entities (Story, Task, Bug, Attachment)
- Location:
  - Python: `scripts/chandao_fetch/models.py`
  - Java: `scripts/java-src/src/main/java/com/tsintergy/chandao/model/*.java`
- Contains: Dataclass/POJO definitions with JSON deserialization
- Depends on: None (self-contained)
- Used by: Client and Service layers

**Service Layer:**
- Purpose: Orchestrate data download, file attachment processing, and content transformation
- Location:
  - Python: `scripts/chandao_fetch/service.py`
  - Java: `scripts/java-src/src/main/java/com/tsintergy/chandao/service/ChandaoService.java`
- Contains: Multi-ID handling, attachment download, embedded image extraction and transformation
- Depends on: Client, Models, Exporter layers
- Used by: CLI, SKILL orchestration

**Exporter/Output Layer:**
- Purpose: Transform domain models to Markdown files with embedded attachments and images
- Location:
  - Python: `scripts/chandao_fetch/exporter.py`
  - Java: `scripts/java-src/src/main/java/com/tsintergy/chandao/service/MarkdownExporter.java`
- Contains: Markdown generation, path transformation (relative path calculation for attachments)
- Depends on: Models, Filesystem
- Used by: Service layer

## Data Flow

**Content Download Flow:**

1. **User triggers skill** → Provides ID or URL (e.g., "需求 39382" or URL with story-view-39382)
2. **CLI parses input** → Extracts type (story/task/bug) and ID
3. **Load configuration** → Read from workspace `.chandao/config.properties` or global `~/.chandao/config.properties`
4. **Client login** → POST to `/user-login.json` with credentials
5. **Fetch content** → GET from API endpoint (e.g., `/story-get-39382.json`)
6. **Parse JSON response** → Deserialize to Story/Task/Bug model with nested Attachment objects
7. **Download attachments** → Iterate attachments, download to `attachments/{type}/{id}/`
8. **Extract images** → Parse HTML `<img>` tags from content fields, download images
9. **Transform content** → Update image URLs from absolute to relative paths (`../attachments/...`)
10. **Generate Markdown** → Build markdown structure with fields, description, verification, attachments
11. **Write output** → Save to `{workspace}/{type}/{id}-{title}.md`

**Markdown File Structure Output:**
```
{workspace}/
├── story/
│   └── 39382-需求标题.md
├── task/
│   └── 61563-任务名称.md
├── bug/
│   └── 66445-Bug标题.md
└── attachments/
    ├── story/39382/
    │   ├── image1.png
    │   └── document.pdf
    ├── task/61563/
    └── bug/66445/
```

**State Management:**

- **Configuration state**: Loaded once at startup, immutable during execution
- **Session state**: HTTP session maintained in ChandaoClient, persists login cookie for multiple requests
- **Model state**: In-memory representations of Story/Task/Bug entities during processing
- **File I/O state**: Filesystem operations are append-only and idempotent (safe for retries)

## Key Abstractions

**Content Type Abstraction:**
- Purpose: Handle Story, Task, and Bug as variants with common interface
- Examples: `scripts/chandao_fetch/models.py` (Story, Task, Bug classes), `scripts/java-src/src/main/java/com/tsintergy/chandao/model/`
- Pattern: Each model type has specific fields but all support export to Markdown. Service layer dispatches to type-specific handlers.

**Configuration Hierarchy:**
- Purpose: Support multiple deployment scenarios (workspace-specific vs. global configuration)
- Examples: `scripts/chandao_fetch/config.py` (ChandaoConfig.load() method)
- Pattern: Priority chain - command line > workspace config > global config > defaults. Workspace config stored in `.chandao/config.properties`, global in `~/.chandao/config.properties`.

**Path Management Abstraction:**
- Purpose: Handle relative and absolute path transformations for attachment references
- Examples: `scripts/chandao_fetch/exporter.py` (MarkdownExporter._process_content, image URL transformation)
- Pattern: Absolute URLs from API converted to relative markdown paths (`../attachments/{type}/{id}/filename`)

**Content Transformation Pipeline:**
- Purpose: Extract, download, and transform embedded resources
- Examples: Image extraction regex in `scripts/chandao_fetch/service.py`, markdown generation in exporter
- Pattern: Extract `<img src="...">` → download file → update URL → generate markdown reference

## Entry Points

**CLI Entry (Python):**
- Location: `scripts/chandao_fetch/__main__.py` (main() function)
- Triggers: Direct execution via `python3 chandao_fetch.py -t story -i 39382`
- Responsibilities: Parse CLI args, instantiate ChandaoConfig, create ChandaoService, execute download

**CLI Entry (Java):**
- Location: `scripts/java-src/src/main/java/com/tsintergy/chandao/ChandaoFetchApplication.java` (main() method)
- Triggers: Direct execution via `java -jar chandao-fetch.jar -t story -i 39382`
- Responsibilities: Parse JCommander args, load config with workspace awareness, instantiate service, handle exceptions

**Skill Entry (via Claude Code):**
- Location: `SKILL.md` (orchestration steps)
- Triggers: User mentions "禅道", "需求", "任务", "Bug", etc.
- Responsibilities: Environment detection, configuration guidance, invoke appropriate runtime version

## Error Handling

**Strategy:** Fail-fast with detailed error messages; graceful degradation for optional features (attachments, images)

**Patterns:**

- **Configuration errors**: Check `is_initialized()` before execution; if false, print configuration prompt and exit with code 1
- **Network errors**: Catch connection timeouts and HTTP errors; wrap in Exception with context (e.g., "登录失败: HTTP 401")
- **File I/O errors**: Attachment download failures log but continue (non-blocking); file write failures propagate
- **Parsing errors**: JSON deserialization errors caught and logged with ID/type context
- **Subtask handling** (v1.6.0): If task description is empty (detected by missing `## 任务描述` in markdown), auto-detect parent task and associated story, recursively download related content

## Cross-Cutting Concerns

**Logging:** 
- Python: `print()` statements to stdout (logs go to SKILL execution context)
- Java: SLF4J + Logback configuration in `scripts/java-src/src/main/resources/logback.xml`

**Validation:**
- CLI validation: Check required parameters (`-t`, `-i` or `--ids`)
- Configuration validation: Ensure base_url, username, password are present before API calls
- Content validation: Verify JSON response status/result fields before model deserialization

**Authentication:**
- POST login with username/password to `/user-login.json`
- Response contains session cookie (auto-managed by requests/OkHttp)
- Subsequent API calls use authenticated session
- No persistent token storage; login happens per execution session

**Output Consistency:**
- Markdown filenames follow pattern: `{id}-{sanitized-title}.md`
- Attachment paths always relative: `../attachments/{type}/{id}/{filename}`
- Line endings and encoding: UTF-8 with LF (cross-platform)
- Safe filename sanitization: Remove/replace invalid characters

---

*Architecture analysis: 2026-04-04*

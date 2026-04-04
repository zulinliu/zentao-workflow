# External Integrations

**Analysis Date:** 2026-04-04

## APIs & External Services

**Zentao Project Management System:**
- Service: Zentao (开源项目管理系统)
- What it's used for: Download stories (需求), tasks (任务), and bugs (缺陷) details and metadata
- SDK/Client: Custom implementation in `scripts/chandao_fetch/client.py` (Python) and `scripts/java-src/src/main/java/com/tsintergy/chandao/client/` (Java)
- Authentication: HTTP POST login with username/password to `/user-login.json` endpoint (see `scripts/chandao_fetch/client.py` lines 44-69)
- Read-only constraint: Client only supports queries (login, view, download) - no write operations permitted (see `scripts/chandao_fetch/client.py` lines 19-24)

**Zentao API Endpoints Used:**
- `{base_url}/user-login.json` - Authentication
- `{base_url}/story-view-{id}.json` - Fetch story details
- `{base_url}/task-view-{id}.json` - Fetch task details
- `{base_url}/bug-view-{id}.json` - Fetch bug details
- `{base_url}/file-download-{id}.json` - Download attachments
- Embedded image paths extracted from HTML content and downloaded

**Claude Code Superpowers Plugin (v1.5.0+):**
- Service: Official superpowers plugin for Claude Code
- What it's used for: Technical implementation plan generation (brainstorming and code execution)
- Dependencies:
  - superpowers v5.0.6+
  - Required skills: `brainstorming`, `subagent-driven-development`, `requesting-code-review` (optional)
- Installation: `claude plugins add official superpowers` (auto-prompted if missing)
- Integration point: SKILL.md Step 4 (see `SKILL.md` lines 257-310)

## Data Storage

**Local File System:**
- Output structure: `{workspace}/` (specified via config or CLI argument)
- Markdown files: `{workspace}/{type}/{id}-{title}.md`
- Attachments directory: `{workspace}/attachments/{type}/{id}/`
- Configuration file: `~/.chandao/config.properties` (global) or `.chandao/config.properties` (workspace-local)
- No database required - all data stored as local files

**File Organization** (from `scripts/chandao_fetch/exporter.py` and `scripts/chandao_fetch/service.py`):
- Story exports: `story/{id}-{title}.md` with attachments in `attachments/story/{id}/`
- Task exports: `task/{id}-{name}.md` with attachments in `attachments/task/{id}/`
- Bug exports: `bug/{id}-{title}.md` with attachments in `attachments/bug/{id}/`
- Relative paths to attachments: `../attachments/{type}/{id}/filename` (for internal Markdown references)

**No Caching:** Not detected - all downloads are fresh from Zentao

## Authentication & Identity

**Auth Provider:** Custom implementation (Zentao native session-based auth)
- Implementation: HTTP session cookies maintained by `requests.Session()` in `scripts/chandao_fetch/client.py`
- Credentials flow:
  1. User provides username/password via CLI or config file
  2. Client POSTs to `/user-login.json` with credentials (line 57, `client.py`)
  3. Session automatically persists cookies for subsequent API calls
  4. No token generation - relies on session state

**Configuration Sources** (priority order, see `scripts/chandao_fetch/config.py` lines 38-65):
1. Command-line arguments (highest priority) - `--url`, `--username`, `--password`
2. Workspace config file - `.chandao/config.properties` in project root
3. Global config file - `~/.chandao/config.properties` in user home (lowest priority)

**Security Constraints:**
- Passwords stored in local config files only (no transmission to external services)
- Client only supports read operations - no data modification (see `scripts/chandao_fetch/client.py` lines 19-24)
- Session timeout handled by Zentao server

## Monitoring & Observability

**Error Tracking:**
- Not detected - no external error tracking service
- Errors logged to console via Python `print()` statements or Java Logback

**Logs:**
- Python: Console output via `print()` statements in all modules (`client.py`, `service.py`, `exporter.py`)
- Java: SLF4J + Logback (configured in `scripts/java-src/`)
- Log levels: INFO (default) and ERROR (on exceptions)
- No log aggregation or external service integration

**Structured Logging (Java only):**
- SLF4J API 2.0.9 for logging abstraction
- Logback 1.3.11 for implementation (config typically in `logback.xml`)

## CI/CD & Deployment

**Hosting:**
- GitHub as repository host
- GitHub Releases for distribution (automated)

**CI Pipeline:**
- GitHub Actions workflow: `.github/workflows/release.yml`
- Trigger: `push` to `main` branch
- Build steps:
  1. Checkout code
  2. Read version from `VERSION` file
  3. Create release package (zip with SKILL.md, scripts, assets, references - excluding java-src)
  4. Generate release notes from CHANGELOG.md
  5. Create GitHub Release with automated deployment package

**Release Package Contents:**
```
zentao-workflow/
├── SKILL.md                          # Main skill file
├── scripts/
│   ├── chandao-fetch.jar             # Compiled Java executable
│   ├── chandao_fetch.py              # Python entry point
│   ├── requirements.txt               # Python dependencies
│   └── chandao_fetch/                # Python module
├── assets/                           # Templates
│   ├── config_template.properties    # Config example
│   └── tech_plan_template.md         # Plan template
└── references/                       # Documentation
```

**Excluded from Release:**
- `scripts/java-src/` (source code only, compiled JAR included)
- `CLAUDE.md`, `CONTRIBUTING.md`, `README.md` (development docs)
- `.github/` (CI/CD configuration)
- `.git/` (version control metadata)

## Environment Configuration

**Required env vars:** None - all configuration via `config.properties` file

**Config requirements for operation:**
- `zentao.url` - Zentao server address (e.g., https://zentao.example.com)
- `zentao.username` - Login account
- `zentao.password` - Login password

**Optional config:**
- `output.dir` - Output directory (defaults to current working directory)
- `connect.timeout` - Connection timeout in ms (default 30000)
- `read.timeout` - Read timeout in ms (default 60000)
- `download.threads` - Number of parallel download threads (default 3)

**Secrets location:**
- Local config files only: `~/.chandao/config.properties` or `.chandao/config.properties`
- Never transmitted to external services or included in git history
- User responsible for protecting config files (contains credentials)

## Webhooks & Callbacks

**Incoming:**
- Not applicable - Zentao workflow is purely client-initiated

**Outgoing:**
- Not detected - No webhooks or callbacks to external services

## Data Transformation

**Content Processing:**
- HTML to Markdown conversion in `scripts/chandao_fetch/exporter.py`
  - Inline images: `<img src="...">` tags extracted and downloaded
  - Relative path conversion: Image paths converted to Markdown references (`![](../attachments/...)`)
  - HTML table preservation: Tables retained as-is in Markdown output

**Attachment Handling:**
- Filenames sanitized for filesystem compatibility (`_sanitize_filename()` in `exporter.py`)
- Extension-based type detection (image, document, etc.)
- Automatic subdirectory creation by content type and ID

---

*Integration audit: 2026-04-04*

# Codebase Structure

**Analysis Date:** 2026-04-04

## Directory Layout

```
/home/liuzl/agent/zentao-workflow/
├── SKILL.md                    # Skill definition & execution steps (触发条件、技能流程)
├── README.md                   # Installation, features, quick start
├── CLAUDE.md                   # Development guidelines (仅 dev 分支)
├── CHANGELOG.md                # Version history and updates
├── VERSION                     # Current version: 1.5.0
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guidelines
│
├── scripts/                    # Execution tools (runtime binaries and source)
│   ├── chandao-fetch.jar       # Java version (compiled binary)
│   ├── chandao_fetch.py        # Python version (wrapper entry point)
│   │
│   ├── chandao_fetch/          # Python module (packaged as installable)
│   │   ├── __init__.py         # Module initialization
│   │   ├── __main__.py         # CLI entry point
│   │   ├── config.py           # Configuration management
│   │   ├── client.py           # Zentao API client
│   │   ├── models.py           # Data models (Story, Task, Bug, Attachment)
│   │   ├── service.py          # Business logic orchestration
│   │   ├── exporter.py         # Markdown generation
│   │   └── __pycache__/        # Generated (gitignored)
│   │
│   ├── java-src/               # Java source (excluded from release builds)
│   │   ├── pom.xml             # Maven build config
│   │   ├── README.md           # Java build instructions
│   │   └── src/
│   │       ├── main/java/com/tsintergy/chandao/
│   │       │   ├── ChandaoFetchApplication.java
│   │       │   ├── cli/CommandLineArgs.java
│   │       │   ├── config/ChandaoConfig.java
│   │       │   ├── client/ChandaoClient.java
│   │       │   ├── model/
│   │       │   │   ├── Story.java
│   │       │   │   ├── Task.java
│   │       │   │   ├── Bug.java
│   │       │   │   └── Attachment.java
│   │       │   └── service/
│   │       │       ├── ChandaoService.java
│   │       │       └── MarkdownExporter.java
│   │       └── test/java/com/tsintergy/chandao/
│   │           ├── config/ChandaoConfigTest.java
│   │           ├── client/ChandaoClientTest.java
│   │           ├── model/*.Test.java
│   │           └── service/*.Test.java
│   │
│   └── requirements.txt         # Python dependencies (requests, etc)
│
├── assets/                     # Templates and templates
│   ├── config_template.properties  # Configuration file template
│   └── tech_plan_template.md       # Technical plan output template
│
├── references/                 # Project type analysis guides
│   ├── java_project_guide.md   # Guidance for Java projects
│   └── react_project_guide.md  # Guidance for React projects
│
├── .github/workflows/          # CI/CD automation
│   └── release.yml             # Automated release (excludes java-src)
│
└── .planning/codebase/         # Generated (this directory)
    ├── ARCHITECTURE.md
    └── STRUCTURE.md
```

## Directory Purposes

**scripts/**
- Purpose: Runtime tools for downloading Zentao content (executes during SKILL steps)
- Contains: Compiled Java JAR, Python module, source code, dependencies
- Key files: `chandao-fetch.jar` (primary), `chandao_fetch.py` (fallback)
- Generated: `__pycache__`, `chandao-fetch.jar` (from java-src)
- Committed: Python source, `requirements.txt`, JAR file; java-src source code only

**scripts/chandao_fetch/**
- Purpose: Python implementation of content download tool
- Contains: Modular Python package with separated concerns (CLI, config, client, models, service, export)
- Entry flow: `__main__.py` → `config.py` → `service.py` → `client.py` + `exporter.py`
- Installable: Can be used as `python3 -m chandao_fetch` or `python3 chandao_fetch.py`

**scripts/java-src/**
- Purpose: Java source code (Maven project for compilation)
- Contains: Complete Java implementation with tests
- Build output: `chandao-fetch.jar` copied to `scripts/` directory after `mvn clean package`
- **Not included in release builds** - only source repository contains this
- Dependencies: OkHttp (HTTP), Jackson (JSON), JCommander (CLI), SLF4J (logging)

**assets/**
- Purpose: Templates for configuration and output
- Contains: `config_template.properties` (shows configuration file structure), `tech_plan_template.md` (output format reference)
- Usage: Referenced in documentation, used as templates during skill execution

**references/**
- Purpose: Context guides for brainstorming skill integration
- Contains: `java_project_guide.md` (analyzes typical Java projects), `react_project_guide.md` (analyzes React projects)
- Usage: Read by superpowers:brainstorming skill when generating technical implementation plans

**.github/workflows/**
- Purpose: Automated CI/CD for release builds
- Contains: `release.yml` - triggers on version updates, builds and packages
- Excludes: `java-src/` directory (only release binaries), dev documentation (`CLAUDE.md`, `CONTRIBUTING.md`)

## Key File Locations

**Entry Points:**
- `scripts/chandao_fetch/__main__.py` - Python CLI entry; parses args, manages config, orchestrates download
- `scripts/java-src/src/main/java/com/tsintergy/chandao/ChandaoFetchApplication.java` - Java CLI entry; same responsibilities
- `SKILL.md` - Skill orchestration entry; describes when/how the tool is invoked

**Configuration:**
- `scripts/chandao_fetch/config.py` - Python configuration management with multi-level priority loading
- `scripts/java-src/src/main/java/com/tsintergy/chandao/config/ChandaoConfig.java` - Java configuration counterpart
- `.chandao/config.properties` - Workspace-specific config (created in working directory)
- `~/.chandao/config.properties` - Global config (created in home directory)

**Core Logic:**
- `scripts/chandao_fetch/service.py` - Python orchestrator; handles download workflow, attachment/image processing
- `scripts/java-src/src/main/java/com/tsintergy/chandao/service/ChandaoService.java` - Java service layer
- `scripts/chandao_fetch/client.py` - Python API client; manages HTTP session, login, content fetching
- `scripts/java-src/src/main/java/com/tsintergy/chandao/client/ChandaoClient.java` - Java API client

**Models & Export:**
- `scripts/chandao_fetch/models.py` - Python data models (Story, Task, Bug, Attachment)
- `scripts/java-src/src/main/java/com/tsintergy/chandao/model/*.java` - Java model classes
- `scripts/chandao_fetch/exporter.py` - Python markdown generation with relative path handling
- `scripts/java-src/src/main/java/com/tsintergy/chandao/service/MarkdownExporter.java` - Java exporter

**Testing:**
- `scripts/java-src/src/test/java/com/tsintergy/chandao/` - JUnit test suite for Java version
- Python version: No dedicated test files in repository (tested during SKILL execution)

**Documentation:**
- `README.md` - User-facing documentation (installation, quick start, features)
- `SKILL.md` - Complete skill execution steps (for Claude Code orchestration)
- `CLAUDE.md` - Development guidelines (architecture, build commands, constraints) - **dev branch only**
- `CHANGELOG.md` - Version history with detailed updates per version
- `scripts/java-src/README.md` - Java-specific build instructions

## Naming Conventions

**Files:**

- **Executable scripts**: Lowercase with underscores: `chandao_fetch.py`
- **Documentation**: UPPERCASE: `README.md`, `SKILL.md`, `CLAUDE.md`, `CHANGELOG.md`
- **Configuration templates**: Lowercase with extension: `config_template.properties`
- **Source files**:
  - Python: `snake_case.py` (e.g., `chandao_fetch.py`, `__main__.py`)
  - Java: `PascalCase.java` (e.g., `ChandaoFetchApplication.java`)

**Directories:**

- **Packages**: Lowercase hierarchical: `chandao_fetch/`, `com/tsintergy/chandao/`
- **Module organization**: Functional domains: `cli/`, `config/`, `client/`, `model/`, `service/`
- **Content output**: Type-based: `story/`, `task/`, `bug/`, `attachments/`
- **Special directories**: Dotfiles for configs: `.chandao/`, `.github/`

**Output Files:**

- **Content files**: `{id}-{sanitized-title}.md` (e.g., `39382-需求标题.md`)
- **Technical plans**: `{type}_{id}_技术实现方案.md` (e.g., `story_39382_技术实现方案.md`)
- **Configuration**: `config.properties` (Java Properties format)

## Where to Add New Code

**New Feature in Download Tool:**

**Implementation:**
- Python: `scripts/chandao_fetch/{module}.py` (create new module if needed)
- Java: `scripts/java-src/src/main/java/com/tsintergy/chandao/{package}/{Class}.java`

**Tests:**
- Java: `scripts/java-src/src/test/java/com/tsintergy/chandao/{package}/{Class}Test.java`

**Example - Adding new API client method:**
- Python: Add method to `scripts/chandao_fetch/client.py` (ChandaoClient class)
- Java: Add method to `scripts/java-src/src/main/java/com/tsintergy/chandao/client/ChandaoClient.java`

**New Content Type (e.g., Initiative, Epic):**

1. **Add model:**
   - Python: New dataclass in `scripts/chandao_fetch/models.py`
   - Java: New class in `scripts/java-src/src/main/java/com/tsintergy/chandao/model/`

2. **Add client method:**
   - Python: `def get_initiative(self, item_id)` in `scripts/chandao_fetch/client.py`
   - Java: `public Initiative getInitiative(int id)` in ChandaoClient

3. **Add exporter method:**
   - Python: `def export_initiative(self, initiative)` in `scripts/chandao_fetch/exporter.py`
   - Java: `public Path exportInitiative(Initiative initiative)` in MarkdownExporter

4. **Add service handler:**
   - Python: Add case in `scripts/chandao_fetch/service.py` `_fetch_by_id()` method
   - Java: Add case in ChandaoService `execute()` method

5. **Update CLI:**
   - Python: Add choice to `--type` argument in `scripts/chandao_fetch/__main__.py`
   - Java: Add to choices in `scripts/java-src/src/main/java/com/tsintergy/chandao/cli/CommandLineArgs.java`

**Skill Workflow Enhancement:**

- Location: `SKILL.md` (the only orchestration document)
- Pattern: Add numbered Step and update trigger conditions
- Format: YAML frontmatter `description` field contains trigger keywords
- Example: v1.6.0 added Steps 3.5 (subtask detection) and updated Step 3.2-3.6 accordingly

**Documentation Updates:**

- User docs: `README.md` (features, quick start, FAQ)
- Development: `CLAUDE.md` (dev guidelines, build commands) - **dev branch only**
- Changelog: `CONTRIBUTING.md` and `CHANGELOG.md` (commit message format, version updates)

## Special Directories

**scripts/java-src/:**
- Purpose: Source code for Java version compilation
- Generated: `target/` directory during Maven build (gitignored)
- Committed: `pom.xml`, `README.md`, all source files under `src/`
- **Important**: This directory is **excluded from release builds** (see `.github/workflows/release.yml`)
  - Reason: Keep release packages lightweight; only JAR binary needed for execution
  - Distribution: Only available in git repository; not in GitHub Releases download

**scripts/__pycache__/:**
- Purpose: Python bytecode cache
- Generated: Yes (during Python execution)
- Committed: No (gitignored)

**.github/workflows/**
- Purpose: CI/CD automation
- Generated: No (committed)
- Committed: Yes (`release.yml` for automated versioning and packaging)

**.chandao/ (in workspace and home):**
- Purpose: Configuration directory (created at runtime)
- Generated: Yes (created by tool on first run)
- Committed: No (gitignored; credentials stored locally)
- Locations: 
  - Workspace: `.chandao/config.properties` (project-specific)
  - Home: `~/.chandao/config.properties` (global fallback)

**.planning/codebase/ (this directory):**
- Purpose: GSD codebase mapping output
- Generated: Yes (created by GSD mapper)
- Committed: Yes (documentation artifacts)
- Files: `ARCHITECTURE.md`, `STRUCTURE.md`, and other analysis documents

## Module Dependencies

**Python module dependency graph:**
```
__main__.py
  ├── config.py (ChandaoConfig)
  ├── service.py (ChandaoService)
  │   ├── client.py (ChandaoClient)
  │   ├── exporter.py (MarkdownExporter)
  │   └── models.py (Story, Task, Bug, Attachment)
  └── models.py (direct reference for validation)
```

**Java package hierarchy:**
```
ChandaoFetchApplication (main entry)
  ├── cli/CommandLineArgs (arg parsing)
  ├── config/ChandaoConfig (configuration)
  └── service/ChandaoService (orchestration)
      ├── client/ChandaoClient (API interaction)
      ├── model/* (domain objects)
      └── service/MarkdownExporter (output generation)
```

---

*Structure analysis: 2026-04-04*

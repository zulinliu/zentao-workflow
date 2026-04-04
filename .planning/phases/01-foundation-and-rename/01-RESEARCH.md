# Phase 1: Foundation and Rename - Research

**Researched:** 2026-04-04
**Domain:** Python project rename, package restructuring, TOML config, pyproject.toml setup
**Confidence:** HIGH

## Summary

Phase 1 is a full-project rename from chandao/zentao naming to worklet, combined with Java artifact removal, Python version bump (3.6+ to 3.10+), config format migration (Java Properties to TOML), and new data model stubs. The grep audit found 453 occurrences of chandao/zentao across 36 files. The rename scope inside `scripts/` is well-bounded: 6 Python modules plus 1 wrapper entry point, with class names ChandaoConfig, ChandaoClient, ChandaoService all needing rename to WorkletConfig, WorkletClient, WorkletService. The Java removal is clean -- one 6.7MB JAR and one 308KB source directory, plus references in SKILL.md, release.yml, CLAUDE.md, and .claude/settings.local.json.

The TOML config migration is straightforward. Python 3.11+ includes `tomllib` in the stdlib; since the project targets 3.10+, the standard pattern is a conditional import (`tomllib` on 3.11+, `tomli` backport on 3.10). For writing TOML, `tomli-w` is the only dependency since `tomllib`/`tomli` are read-only. The pyproject.toml setup uses setuptools with `[tool.setuptools.packages.find] where = ["scripts"]` per the user's locked decision D-02.

**Primary recommendation:** Execute the rename in dependency order -- (1) delete Java, (2) rename package directory and files, (3) update all internal imports and class names, (4) create new data model stubs, (5) migrate config to TOML, (6) create pyproject.toml, (7) update peripheral files (.gitignore, .release-ignore, release.yml, SKILL.md references, .claude/settings.local.json), (8) clean up __pycache__.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01: Package directory structure** -- Keep `scripts/` hierarchy, rename `scripts/chandao_fetch/` to `scripts/worklet/` and `scripts/chandao_fetch.py` to `scripts/worklet.py`
- **D-02: pyproject.toml location** -- Project root, using `[tool.setuptools.packages.find] where = ["scripts"]` with setuptools backend (`requires = ["setuptools>=68.0"]`)
- **D-03: Data model strategy** -- New models (Worklet, RawContent, Attachment dataclass + BaseSource/BaseReader ABC) as placeholders; old models (Story/Task/Bug) renamed (remove Chandao prefix), kept alongside new models; migration deferred to Phase 2
- **D-04: Config format** -- TOML format, file `.worklet/config.toml`, using tomli (read) + tomli-w (write) as dependencies
- **D-05: Python version** -- Python >= 3.10, use `X | Y` union types, `match/case`, built-in generics `list[T]`/`dict[K, V]`
- **D-06: Output directory structure** -- Unified under `.worklet/` (config.toml + story/task/bug/files/attachments)
- **D-07: CLI style** -- Keep old `-t/-i` style, retain `scripts/worklet.py` wrapper
- **D-08: Java deletion scope** -- Delete `scripts/chandao-fetch.jar`, `scripts/java-src/`, all Java references in SKILL.md/README.md/CLAUDE.md, clean `.claude/settings.local.json`

### Claude's Discretion
- Java deletion git operation order (files first vs references first)
- `.gitignore` pattern syntax for `.worklet/`
- `__pycache__/` cleanup strategy
- Whether to keep `requirements.txt` alongside pyproject.toml
- Whether `references/` directory content needs adjustment

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| FOUND-01 | Full rename chandao_fetch to worklet (package, class, folder, config keys) | Grep audit: 453 occurrences across 36 files; rename map and import dependency chain documented |
| FOUND-02 | Delete Java version (JAR, java-src/, all references) | Java artifacts located: 6.7MB JAR + 308KB java-src; references in SKILL.md, release.yml, CLAUDE.md, settings.local.json |
| FOUND-03 | Python version bump to 3.10+ | Python 3.12.3 available on system; 3.10+ features (union types, match/case, built-in generics) verified working |
| FOUND-04 | Data model restructure (Worklet/RawContent/Attachment + BaseSource/BaseReader ABC) | Existing models.py analyzed; new dataclass shapes defined in D-03; ABC pattern straightforward |
| FOUND-05 | WorkletConfig replaces ChandaoConfig, .worklet/ config directory | Existing config.py analyzed; config priority chain preserved; path changes documented |
| FOUND-06 | Config file 0600 permissions | os.chmod with stat.S_IRUSR/S_IWUSR verified working on this Linux platform |
| FOUND-07 | .worklet/ auto-added to .gitignore | Current .gitignore has chandao-data patterns; replacement patterns documented |
| FOUND-08 | .gitignore update (chandao to worklet paths) | Current entries: chandao-data/, chandao-data-*/, attachments/; need worklet equivalents |
| FOUND-09 | .release-ignore update (remove Java paths and comments) | Current file has `scripts/java-src/` and `chandao-data/` entries to replace |
| FOUND-10 | .claude/settings.local.json cleanup | 4 Java-related permission rules identified for removal |
| FOUND-11 | requirements.txt update | Currently: `requests>=2.28.0`; needs `requests>=2.32.0` + tomli/tomli-w |
| FOUND-12 | Entry file rename chandao_fetch.py to worklet.py | Wrapper script analyzed; single import to update |
| FOUND-13 | Clean __pycache__/ | Located: scripts/chandao_fetch/__pycache__/ with 7 .pyc files |
| FOUND-14 | Output directory unification to .worklet/ | Current: outputs to workspace root; new: all under .worklet/ |
| FOUND-15 | __init__.py version update to 2.0.0 | Current: `__version__ = "1.0.0"`; also VERSION file needs 2.0.0 |
| FOUND-16 | Create pyproject.toml | setuptools config with `where = ["scripts"]` package discovery; dependency and metadata structure documented |
| DOC-03 | Config template rename | assets/config_template.properties needs conversion to TOML format template |
</phase_requirements>

## Project Constraints (from CLAUDE.md)

- **Commit format:** Use `feat:` / `fix:` / `docs:` / `release:` prefix convention
- **Branch strategy:** dev branch for development, main for production (but .planning/config.json has `branching_strategy: "none"` -- GSD workflow controls branches)
- **Security:** API clients must remain read-only; no write operations
- **Python style:** 4-space indentation, PEP 8, UTF-8 encoding, Unix LF line endings
- **Imports:** Relative imports within package (e.g., `from .config import WorkletConfig`)
- **Module docstrings:** Google style docstrings
- **Functions:** Python functions under 80 lines
- **GSD Workflow:** All file changes through GSD commands

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| requests | >=2.32.0 | HTTP client for Zentao API | Already in use; 2.32.0+ has security fixes (CVE-2024-35195) |
| tomli | >=2.0.0 | TOML reading (Python 3.10 backport) | Standard backport of stdlib tomllib; only needed on Python <3.11 |
| tomli-w | >=1.0.0 | TOML writing | Companion to tomli/tomllib; stdlib has no TOML writer |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| setuptools | >=68.0 | Build backend for pyproject.toml | Build system requirement only, not runtime |
| pytest | >=8.0.0 | Test framework | Phase 3 will use this; Phase 1 sets up pyproject.toml test config |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| tomli + tomli-w | tomlkit | tomlkit preserves comments and formatting but adds more complexity; tomli/tomli-w is simpler for our config read/write use case |
| tomli (for 3.10) | Require Python 3.11+ | Would avoid the tomli dependency entirely, but D-05 explicitly says 3.10+ |

**Installation:**
```bash
pip install requests>=2.32.0 tomli>=2.0.0 tomli-w>=1.0.0
```

**Version verification (2026-04-04):**
| Package | Registry Latest | Verified |
|---------|----------------|----------|
| requests | 2.33.1 | Yes |
| tomli | 2.4.1 | Yes |
| tomli-w | 1.2.0 | Yes |
| setuptools | 82.0.1 | Yes |

## Architecture Patterns

### Target Project Structure (after Phase 1)
```
zentao-workflow/               # repo name unchanged until Phase 5
├── pyproject.toml             # NEW: project metadata and dependencies
├── VERSION                    # updated to 2.0.0
├── SKILL.md                   # updated: Java refs removed, Python paths updated
├── CLAUDE.md                  # updated: Java sections removed (Phase 5 full rewrite)
├── .gitignore                 # updated: .worklet/ added, chandao-data removed
├── .release-ignore            # updated: java-src removed, chandao-data removed
├── .claude/settings.local.json # cleaned: Java copy permissions removed
├── .github/workflows/release.yml # updated: Java refs removed, worklet naming
├── assets/
│   └── config_template.toml   # RENAMED from .properties, converted to TOML
├── scripts/
│   ├── worklet.py             # RENAMED from chandao_fetch.py
│   ├── worklet/               # RENAMED from chandao_fetch/
│   │   ├── __init__.py        # version 2.0.0, exports renamed classes
│   │   ├── __main__.py        # CLI entry, WorkletConfig/WorkletService imports
│   │   ├── config.py          # WorkletConfig, TOML format, .worklet/ paths
│   │   ├── client.py          # WorkletClient (renamed from ChandaoClient)
│   │   ├── models.py          # Existing models renamed + new Worklet/RawContent stubs
│   │   ├── service.py         # WorkletService (renamed from ChandaoService)
│   │   └── exporter.py        # MarkdownExporter (unchanged class name)
│   └── requirements.txt       # KEPT: for SKILL.md pip install compatibility
└── references/                # content unchanged in Phase 1
```

### Pattern 1: Conditional TOML Import (Python 3.10 compatibility)
**What:** Use stdlib tomllib on 3.11+, fall back to tomli on 3.10
**When to use:** Any module that reads TOML
**Example:**
```python
# Source: https://github.com/hukkin/tomli (official README pattern)
import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

# Usage is identical either way:
with open("config.toml", "rb") as f:
    config = tomllib.load(f)
```

### Pattern 2: TOML Config Write with 0600 Permissions
**What:** Write config files with restricted permissions to protect credentials
**When to use:** Any config file that contains passwords
**Example:**
```python
import os
import stat
from pathlib import Path
import tomli_w

def save_config(path: Path, data: dict) -> None:
    """Save config with restricted permissions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        tomli_w.dump(data, f)
    # Restrict to owner read/write only
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
```

### Pattern 3: ABC-based Source Plugin (placeholder for Phase 2)
**What:** Abstract base classes for extensible source system
**When to use:** Phase 1 defines the ABC shapes; Phase 2 implements them
**Example:**
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Worklet:
    id: str
    title: str
    content: str                    # markdown
    source_type: str                # 'zentao', 'file', 'folder'
    attachments: list["Attachment"]
    metadata: dict = field(default_factory=dict)

@dataclass
class RawContent:
    raw: str
    format: str                     # 'html', 'markdown', 'text'

@dataclass
class Attachment:
    id: str
    title: str
    path: Path | None = None

class BaseSource(ABC):
    @abstractmethod
    def fetch(self, identifier: str) -> Worklet: ...

class BaseReader(ABC):
    @abstractmethod
    def read(self, path: Path) -> RawContent: ...
```

### Pattern 4: pyproject.toml with Custom Package Directory
**What:** setuptools config pointing to scripts/ as the package root
**When to use:** Project root pyproject.toml discovering packages in a subdirectory
**Example:**
```toml
# Source: https://setuptools.pypa.io/en/latest/userguide/package_discovery.html
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "worklet"
version = "2.0.0"
description = "Developer workflow assistant - from requirement to code in one step"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [{name = "liuzl"}]
dependencies = [
    "requests>=2.32.0",
    "tomli>=2.0.0; python_version < '3.11'",
    "tomli-w>=1.0.0",
]

[tool.setuptools.packages.find]
where = ["scripts"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### Anti-Patterns to Avoid
- **Partial rename:** Do NOT leave any `chandao` or `zentao` string in `scripts/` -- the success criterion is zero grep hits. This includes docstrings, comments, and variable names that reference the old tool name.
- **Breaking import chains:** When renaming the package directory, ALL relative imports must be updated in the same commit. A half-renamed package will fail to import.
- **Forgetting the wrapper:** `scripts/worklet.py` imports `from worklet.__main__ import main` -- this must match the renamed package directory name exactly.
- **Mixing TOML and Properties:** The new config module must ONLY read/write TOML. Do not leave any `.properties` parsing code. (Users with existing `~/.chandao/config.properties` will need to manually create `.worklet/config.toml` -- v2.0.0 is a breaking change by design, per requirements "Out of Scope: v1.x old config compatibility".)

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| TOML parsing | Custom key=value parser | tomllib / tomli | Edge cases: multiline strings, nested tables, arrays, escaping |
| TOML writing | String concatenation | tomli-w | Proper quoting, escaping, TOML spec compliance |
| File permissions | Manual octal chmod | `os.chmod(path, stat.S_IRUSR \| stat.S_IWUSR)` | Named constants are clearer and cross-platform correct |
| Python version compat | Version string parsing | `sys.version_info >= (3, 11)` tuple comparison | Standard pattern, no string parsing bugs |

**Key insight:** The config format migration from Java Properties to TOML is the most error-prone part. Java Properties has simple key=value syntax; TOML has tables, types, and structure. Use the library -- do not try to manually format TOML strings.

## Runtime State Inventory

> This phase is a rename/refactor -- runtime state inventory is required.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | `~/.chandao/config.properties` with real credentials (url, username, password) and `~/.chandao/chandao-fetch.log` (322KB) | **No migration** -- v2.0.0 is a breaking change. Old config stays. New code reads `.worklet/config.toml`. Users create new config manually. Document in changelog. |
| Live service config | GitHub Actions workflow `release.yml` references `zentao-workflow` directory name, `chandao-fetch.jar`, `chandao_fetch.py`, `chandao_fetch` package in build steps | **Code edit** -- update all paths in release.yml. No external service state (no Datadog, no Tailscale, etc.) |
| OS-registered state | None -- no systemd units, no cron jobs, no Windows Task Scheduler tasks. The tool runs on-demand via Claude Code Skill invocation. | None required |
| Secrets and env vars | No env vars reference chandao/zentao by name. Credentials are in `~/.chandao/config.properties` only. No CI/CD secrets reference the old name. | None required -- credentials are user-local config files, not code |
| Build artifacts | `scripts/chandao_fetch/__pycache__/` with 7 .pyc files (cpython-312); `scripts/chandao-fetch.jar` (6.7MB compiled JAR) | **Delete** both: `rm -rf` the __pycache__ directory and the JAR file |

## Common Pitfalls

### Pitfall 1: Incomplete Grep After Rename
**What goes wrong:** After renaming, some occurrences of "chandao" or "zentao" survive in comments, docstrings, or config templates, causing the success criterion `grep -r "chandao\|zentao" scripts/` to fail.
**Why it happens:** Developers focus on code identifiers (class names, imports) and miss string literals in comments and documentation embedded in source files.
**How to avoid:** Run `grep -ri "chandao\|zentao" scripts/` after every rename commit. Include case-insensitive search. Check ALL files, not just .py files.
**Warning signs:** The post-rename grep returns any output at all.

### Pitfall 2: Broken Relative Imports After Directory Rename
**What goes wrong:** Renaming `scripts/chandao_fetch/` to `scripts/worklet/` breaks all `from .xxx import YYY` relative imports because Python resolves them against the package directory name.
**Why it happens:** Relative imports (`from .config import WorkletConfig`) depend on the package being found by Python's import machinery. If `sys.path` doesn't include `scripts/` or the `__init__.py` is wrong, imports fail.
**How to avoid:** Rename directory and update ALL import statements in the same commit. Test with `python -c "from worklet import __version__"` from the scripts/ directory.
**Warning signs:** `ModuleNotFoundError: No module named 'worklet'` or `ImportError: cannot import name`.

### Pitfall 3: TOML Read Mode Must Be Binary
**What goes wrong:** Opening a TOML file with `open(path, "r")` text mode instead of `open(path, "rb")` binary mode.
**Why it happens:** The old Properties config used text mode. Both `tomllib.load()` and `tomli.load()` require binary file handles.
**How to avoid:** Always use `"rb"` for reading TOML: `with open(path, "rb") as f: data = tomllib.load(f)`.
**Warning signs:** `TypeError: expected binary file handle` from tomllib.

### Pitfall 4: pyproject.toml package-find not discovering worklet
**What goes wrong:** `[tool.setuptools.packages.find] where = ["scripts"]` fails to find the `worklet` package if `scripts/worklet/__init__.py` is missing or malformed.
**Why it happens:** setuptools auto-discovery requires `__init__.py` in every package directory it discovers.
**How to avoid:** Ensure `scripts/worklet/__init__.py` exists and is a valid Python file. Test with `pip install -e .` from the project root.
**Warning signs:** `pip install -e .` succeeds but `import worklet` fails.

### Pitfall 5: Success Criterion Contradiction on Config Format
**What goes wrong:** ROADMAP success criterion 4 says "WorkletConfig loads from .worklet/config.properties" but CONTEXT.md D-04 locks the format as TOML (`.worklet/config.toml`).
**Why it happens:** The ROADMAP was written before the discuss phase locked the TOML decision.
**How to avoid:** Follow CONTEXT.md D-04 (TOML format). The ROADMAP success criterion text should be treated as "WorkletConfig loads from .worklet/config.toml". Planner should note this discrepancy.
**Warning signs:** Building a Properties parser when TOML was decided.

### Pitfall 6: tomli-w writes bytes, not strings
**What goes wrong:** Passing a text-mode file handle to `tomli_w.dump()`.
**Why it happens:** Symmetry assumption: if you read with text mode, you write with text mode. But tomli-w also requires binary mode.
**How to avoid:** Always use `"wb"` for writing TOML: `with open(path, "wb") as f: tomli_w.dump(data, f)`.
**Warning signs:** `TypeError: expected binary file handle` from tomli_w.

## Code Examples

### TOML Config Read with Python 3.10+ Compatibility
```python
# Source: https://github.com/hukkin/tomli README + verified locally
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

def load_config(path: Path) -> dict:
    """Load TOML config file."""
    with open(path, "rb") as f:
        return tomllib.load(f)
```

### TOML Config Write with 0600 Permissions
```python
# Source: https://pypi.org/project/tomli-w/ + os.chmod docs
import os
import stat
from pathlib import Path
import tomli_w

def save_config(path: Path, data: dict) -> None:
    """Save config with owner-only permissions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        tomli_w.dump(data, f)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 0600
```

### Conditional Dependency in pyproject.toml
```toml
# Source: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
[project]
dependencies = [
    "requests>=2.32.0",
    "tomli>=2.0.0; python_version < '3.11'",
    "tomli-w>=1.0.0",
]
```

### Rename Map: Old to New Identifiers
```
# Files
scripts/chandao_fetch.py       -> scripts/worklet.py
scripts/chandao_fetch/         -> scripts/worklet/
scripts/chandao-fetch.jar      -> DELETED
scripts/java-src/              -> DELETED

# Classes
ChandaoConfig                  -> WorkletConfig
ChandaoClient                  -> WorkletClient
ChandaoService                 -> WorkletService

# Config paths
.chandao/config.properties     -> .worklet/config.toml
~/.chandao/config.properties   -> ~/.worklet/config.toml

# Config keys (inside TOML)
zentao.url                     -> [zentao] url
zentao.username                -> [zentao] username
zentao.password                -> [zentao] password

# Exports in __init__.py
"ChandaoConfig"                -> "WorkletConfig"
"ChandaoClient"                -> "WorkletClient"
"ChandaoService"               -> "WorkletService"

# Import statements (all modules)
from .config import ChandaoConfig  -> from .config import WorkletConfig
from .client import ChandaoClient  -> from .client import WorkletClient
from .service import ChandaoService -> from .service import WorkletService

# Wrapper script import
from chandao_fetch.__main__ import main -> from worklet.__main__ import main
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `Optional[str]` type hints | `str \| None` union syntax | Python 3.10 (PEP 604) | All type annotations should use new style |
| `from typing import List, Dict` | `list[str]`, `dict[str, int]` | Python 3.9+ (PEP 585) | Remove typing imports for builtins |
| `if/elif` dispatch | `match/case` statements | Python 3.10 (PEP 634) | Good for content_type dispatch in service.py |
| Java Properties config | TOML config with tomllib | Python 3.11 stdlib (PEP 680) | TOML is Python packaging standard |
| `setup.py` / `setup.cfg` | `pyproject.toml` with setuptools | PEP 621 (2021), widely adopted 2023+ | Single config file for project metadata |

**Deprecated/outdated:**
- `typing.Optional[T]` -- replaced by `T | None` on Python 3.10+
- `typing.List[T]`, `typing.Dict[K, V]` -- replaced by `list[T]`, `dict[K, V]` on Python 3.9+
- Java Properties format for Python config -- TOML is the Python ecosystem standard
- `setup.py` for project metadata -- pyproject.toml is the current standard

## Open Questions

1. **requirements.txt alongside pyproject.toml**
   - What we know: SKILL.md execution may run `pip install -r requirements.txt` directly. pyproject.toml declares the same dependencies.
   - What's unclear: Whether SKILL.md can be updated to use `pip install .` instead (but SKILL.md full rewrite is Phase 5).
   - Recommendation: **Keep requirements.txt** in Phase 1 with updated dependencies. It costs nothing and avoids breaking SKILL.md execution before Phase 5 rewrites it. This is Claude's discretion per CONTEXT.md.

2. **ROADMAP success criterion 4 says .worklet/config.properties but CONTEXT.md says .worklet/config.toml**
   - What we know: CONTEXT.md D-04 explicitly locks TOML format. ROADMAP was written before discuss.
   - What's unclear: Whether to update ROADMAP text.
   - Recommendation: Follow CONTEXT.md (TOML). Planner should note the ROADMAP text needs a minor correction.

3. **references/ directory content**
   - What we know: Contains `java_project_guide.md` and `react_project_guide.md`. These are guides for analyzing target projects, not for this tool itself.
   - What's unclear: Whether Java references inside `java_project_guide.md` count as "Java references to remove."
   - Recommendation: **Leave references/ unchanged** in Phase 1. These are reference materials for users' target projects. Phase 5 DOC-05 handles references/ review.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | All code | Yes | 3.12.3 | -- |
| pip3 | Package management | Yes | 24.0 | -- |
| requests | HTTP client | Yes (installed) | 2.31.0 | Needs upgrade to >=2.32.0 |
| tomli | TOML reading (3.10 compat) | Not installed | -- | Install via pip; not needed on 3.11+ (tomllib in stdlib) |
| tomli-w | TOML writing | Not installed | -- | Install via pip |
| pytest | Test framework | Yes (installed) | 9.0.2 | -- |
| setuptools | Build backend | Yes (installed) | 68.1.2 | Meets >=68.0 requirement |
| git | Version control | Yes | -- | -- |

**Missing dependencies with no fallback:**
- None -- all missing items (tomli, tomli-w) are installable via pip.

**Missing dependencies with fallback:**
- `tomli` is not needed at runtime on Python 3.12 (current system) since `tomllib` is available. But it must be declared in pyproject.toml for Python 3.10 compatibility.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.0.2 |
| Config file | None -- Wave 0 will add `[tool.pytest.ini_options]` in pyproject.toml |
| Quick run command | `cd /home/liuzl/agent/zentao-workflow && python -m pytest tests/ -x -q` |
| Full suite command | `cd /home/liuzl/agent/zentao-workflow && python -m pytest tests/ -v` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| FOUND-01 | No chandao/zentao strings in scripts/ | smoke | `grep -ri "chandao\|zentao" scripts/ && exit 1 \|\| exit 0` | N/A (shell check) |
| FOUND-02 | No Java artifacts exist | smoke | `test ! -f scripts/chandao-fetch.jar && test ! -d scripts/java-src/` | N/A (shell check) |
| FOUND-03 | Python >=3.10 declared | unit | `python -c "from worklet import __version__"` (import succeeds) | No -- Wave 0 |
| FOUND-04 | New data models importable | unit | `python -c "from worklet.models import Worklet, RawContent, BaseSource, BaseReader"` | No -- Wave 0 |
| FOUND-05 | WorkletConfig loads TOML from .worklet/ | unit | `pytest tests/test_config.py -x` | No -- Wave 0 |
| FOUND-06 | Config file has 0600 permissions | unit | `pytest tests/test_config.py::test_permissions -x` | No -- Wave 0 |
| FOUND-15 | __version__ == "2.0.0" | unit | `python -c "from worklet import __version__; assert __version__ == '2.0.0'"` | N/A (one-liner) |
| FOUND-16 | pyproject.toml valid and declares Python >=3.10 | smoke | `pip install -e . --dry-run` or parse pyproject.toml | N/A (shell check) |

### Sampling Rate
- **Per task commit:** `grep -ri "chandao\|zentao" scripts/ && echo FAIL || echo OK` + `python -c "from worklet import __version__; print(__version__)"`
- **Per wave merge:** Full grep audit + import validation + config permission test
- **Phase gate:** All success criteria from ROADMAP verified before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/` directory creation
- [ ] `tests/test_config.py` -- WorkletConfig load/save/permissions tests
- [ ] `tests/test_models.py` -- New data model import verification
- [ ] `[tool.pytest.ini_options]` in pyproject.toml -- testpaths = ["tests"]

*(Note: Wave 0 test creation may be minimal in Phase 1 since TEST-01 through TEST-06 are Phase 3 requirements. Phase 1 validation is primarily grep-based success criteria.)*

## Sources

### Primary (HIGH confidence)
- Local codebase analysis -- all 7 Python source files read and analyzed
- `pip3 index versions` -- package version verification for requests, tomli, tomli-w, setuptools
- Python 3.12.3 local testing -- `tomllib` stdlib availability, `os.chmod` 0600 permissions, Python 3.10+ syntax features all verified locally

### Secondary (MEDIUM confidence)
- [Python tomllib docs](https://docs.python.org/3/library/tomllib.html) -- stdlib TOML module reference
- [tomli GitHub README](https://github.com/hukkin/tomli) -- compatibility pattern for conditional import
- [PEP 680](https://peps.python.org/pep-0680/) -- rationale for tomllib addition to stdlib
- [setuptools package discovery docs](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html) -- `where` parameter for custom package directories
- [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) -- pyproject.toml writing guide

### Tertiary (LOW confidence)
- None -- all findings verified against primary or secondary sources

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all packages verified against PyPI registry, versions confirmed
- Architecture: HIGH -- based on locked decisions from CONTEXT.md and direct codebase analysis
- Pitfalls: HIGH -- all pitfalls verified through local testing or documented in official sources
- Runtime state: HIGH -- filesystem audit performed, all categories explicitly answered

**Research date:** 2026-04-04
**Valid until:** 2026-05-04 (stable domain, no fast-moving dependencies)

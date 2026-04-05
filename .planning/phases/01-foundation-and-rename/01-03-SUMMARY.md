---
phase: 01-foundation-and-rename
plan: "03"
subsystem: config
tags: [toml, tomli, tomli_w, dataclass, abc, config-migration]

# Dependency graph
requires:
  - phase: 01-foundation-and-rename
    provides: WorkletConfig class with .chandao paths, old Story/Task/Bug/Attachment models
affects:
  - Phase 2 (uses WorkletConfig for config, Worklet for unified model)

# Tech tracking
tech-stack:
  added: [tomli, tomli_w, dataclasses, abc.ABC]
  patterns: [TOML config format, 0600 file permissions, ABC abstract base classes]

key-files:
  created: [assets/config_template.toml]
  modified: [scripts/worklet/config.py, scripts/worklet/models.py]

key-decisions:
  - "TOML format with tomli (read) + tomli_w (write) per D-04"
  - "Config paths changed from .chandao/config.properties to .worklet/config.toml"
  - "Timeout units converted from milliseconds to seconds per D-04 TOML structure"
  - "Output directory defaults to .worklet/ under workspace/cwd per FOUND-14"
  - "Attachment.path field uses Path type (not download_path) per D-03"

patterns-established:
  - "Conditional import for tomllib (Python 3.11+ bundled, backport for 3.10)"
  - "0600 permissions enforced via os.chmod on config file write"
  - "New v2.0 models (Worklet, RawContent, BaseSource, BaseReader) as Phase 2 placeholders alongside preserved v1.x models"

requirements-completed: [FOUND-04, FOUND-05, FOUND-06, FOUND-14, DOC-03]

# Metrics
duration: 3min
completed: 2026-04-05
---

# Phase 01: Foundation and Rename — Plan 03 Summary

**TOML-based configuration system with 0600 permissions, new v2.0 data model stubs, and unified .worklet/ output directory**

## Performance

- **Duration:** 3 min
- **Started:** 2026-04-05T10:01:08Z
- **Completed:** 2026-04-05T10:04:31Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- WorkletConfig rewritten to use TOML format with tomli (read) and tomli_w (write)
- Config file permissions enforced at 0600 via os.chmod for credential security
- New v2.0 data model stubs (Worklet, RawContent, BaseSource, BaseReader) added as Phase 2 placeholders
- Attachment model updated with `path: Path | None` field per D-03
- Old models (Story, Task, Bug, Attachment) preserved for backward compatibility
- assets/config_template.properties deleted, replaced with TOML format at assets/config_template.toml

## Task Commits

Each task was committed atomically:

1. **Task 1: Rewrite WorkletConfig for TOML format with 0600 permissions** - `c38048d` (feat)
2. **Task 2: Add new data model stubs and convert config template to TOML** - `fbc820b` (feat)

## Files Created/Modified
- `scripts/worklet/config.py` - TOML-based WorkletConfig with 0600 permissions
- `scripts/worklet/models.py` - Added Worklet, RawContent, BaseSource, BaseReader + Attachment.path field
- `assets/config_template.toml` - New TOML config template (replaced .properties)
- `assets/config_template.properties` - Deleted (TOML replacement)

## Decisions Made
- Used conditional tomllib import (Python 3.11+ bundled, tomli backport for 3.10)
- Timeout values converted from milliseconds to seconds per D-04 TOML structure
- Output directory defaults to .worklet/ under workspace or cwd per FOUND-14
- Attachment.path uses Path type (not download_path) per D-03 locked decision

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Missing tomli_w module: installed via `pip install tomli_w --break-system-packages`

## Next Phase Readiness
- Phase 2 can import Worklet, RawContent, BaseSource, BaseReader from worklet.models
- WorkletConfig is ready for Phase 2 ZentaoSource integration
- Config template in TOML format at assets/config_template.toml

---
*Phase: 01-foundation-and-rename*
*Completed: 2026-04-05*

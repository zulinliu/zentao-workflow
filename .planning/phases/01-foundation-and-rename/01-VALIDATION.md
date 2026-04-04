---
phase: 1
slug: foundation-and-rename
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-04
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.2 |
| **Config file** | None — Wave 0 will add `[tool.pytest.ini_options]` in pyproject.toml |
| **Quick run command** | `cd /home/liuzl/agent/zentao-workflow && python -m pytest tests/ -x -q` |
| **Full suite command** | `cd /home/liuzl/agent/zentao-workflow && python -m pytest tests/ -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** `grep -ri "chandao\|zentao" scripts/ && echo FAIL || echo OK` + `python -c "from worklet import __version__; print(__version__)"`
- **After every plan wave:** Full grep audit + import validation + config permission test
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| TBD | 01 | 1 | FOUND-01 | smoke | `grep -ri "chandao\|zentao" scripts/ && exit 1 \|\| exit 0` | N/A (shell) | ⬜ pending |
| TBD | 01 | 1 | FOUND-02 | smoke | `test ! -f scripts/chandao-fetch.jar && test ! -d scripts/java-src/` | N/A (shell) | ⬜ pending |
| TBD | 01 | 1 | FOUND-03 | unit | `python -c "from worklet import __version__"` | No — Wave 0 | ⬜ pending |
| TBD | 01 | 1 | FOUND-04 | unit | `python -c "from worklet.models import Worklet, RawContent, BaseSource, BaseReader"` | No — Wave 0 | ⬜ pending |
| TBD | 01 | 1 | FOUND-05 | unit | `pytest tests/test_config.py -x` | No — Wave 0 | ⬜ pending |
| TBD | 01 | 1 | FOUND-06 | unit | `pytest tests/test_config.py::test_permissions -x` | No — Wave 0 | ⬜ pending |
| TBD | 01 | 1 | FOUND-15 | unit | `python -c "from worklet import __version__; assert __version__ == '2.0.0'"` | N/A (one-liner) | ⬜ pending |
| TBD | 01 | 1 | FOUND-16 | smoke | `pip install -e . --dry-run` | N/A (shell) | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/` directory creation
- [ ] `tests/test_config.py` — WorkletConfig load/save/permissions stubs
- [ ] `tests/test_models.py` — New data model import verification
- [ ] `[tool.pytest.ini_options]` in pyproject.toml — testpaths = ["tests"]

*Note: Full test suite (TEST-01 through TEST-06) is Phase 3 scope. Phase 1 validation is primarily grep-based success criteria with minimal unit stubs.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| .worklet/ in .gitignore | FOUND-07 | Requires git staging check | `echo "test" > .worklet/test && git status` should not show .worklet/ |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

---
phase: 02-core-pipeline
plan: "02-GAP-01"
type: execute
wave: 1
depends_on: []
files_modified:
  - pyproject.toml
autonomous: true
requirements:
  - INPUT-01

must_haves:
  truths:
    - "SourceRegistry auto-discovers sources via entry_points"
  artifacts:
    - path: "pyproject.toml"
      provides: "entry_points configuration for worklet.sources"
      contains: "[project.entry-points.\"worklet.sources\"]"
  key_links:
    - from: "scripts/worklet/sources/base.py"
      to: "pyproject.toml"
      via: "importlib.metadata.entry_points().select(group='worklet.sources')"
      pattern: "entry_points.*select.*worklet.sources"
---

<objective>
Fix entry_points configuration in pyproject.toml so SourceRegistry auto-discovery works.

Purpose: Enable auto-discovery of sources via entry_points (per INPUT-01 requirement).
Output: pyproject.toml with [project.entry-points."worklet.sources"] section containing zentao and markdown entries.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
## Current pyproject.toml state
@pyproject.toml

## SourceRegistry discovery code (base.py:16-25)
scripts/worklet/sources/base.py uses:
```python
importlib.metadata.entry_points().select(group='worklet.sources')
```

## Required entry_points format
```toml
[project.entry-points."worklet.sources"]
zentao = "worklet.sources.zentao:ZentaoSource"
markdown = "worklet.sources.markdown:MarkdownSource"
```
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add entry_points section to pyproject.toml</name>
  <files>pyproject.toml</files>
  <action>
    Read pyproject.toml first to confirm current state.

    Add the following section to pyproject.toml AFTER the [project] section and BEFORE [tool.setuptools.packages.find]:

    ```toml
    [project.entry-points."worklet.sources"]
    zentao = "worklet.sources.zentao:ZentaoSource"
    markdown = "worklet.sources.markdown:MarkdownSource"
    ```

    This maps the source names ('zentao', 'markdown') to their full module paths (worklet.sources.zentao:ZentaoSource, worklet.sources.markdown:MarkdownSource).
  </action>
  <verify>
    <automated>grep -A2 'project.entry-points."worklet.sources"' pyproject.toml && python3 -c "import importlib.metadata; eps = importlib.metadata.entry_points(); zentao = list(eps.select(group='worklet.sources', name='zentao')); print(f'zentao entries: {len(zentao)}')"</automated>
  </verify>
  <done>pyproject.toml contains [project.entry-points."worklet.sources"] with zentao and markdown entries, entry_points query returns ZentaoSource</done>
</task>

</tasks>

<verification>
- grep finds the entry-points section in pyproject.toml
- python entry_points query can find 'zentao' source entry
</verification>

<success_criteria>
- pyproject.toml has [project.entry-points."worklet.sources"] section
- Both 'zentao' and 'markdown' entries are present
- SourceRegistry._discover() will find these entries via importlib.metadata
</success_criteria>

<output>
After completion, create `.planning/phases/02-core-pipeline/02-GAP-01-SUMMARY.md`
</output>

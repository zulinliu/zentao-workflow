---
phase: 02-core-pipeline
plan: "02-GAP-02"
type: execute
wave: 1
depends_on: []
files_modified:
  - scripts/worklet/client.py
autonomous: true
requirements:
  - CLIENT-02

must_haves:
  truths:
    - "Large attachments download via stream=True with atomic .tmp rename"
  artifacts:
    - path: "scripts/worklet/client.py"
      provides: "download_attachment with atomic .tmp rename"
      contains: "NamedTemporaryFile.*rename"
  key_links:
    - from: "scripts/worklet/sources/zentao.py"
      to: "scripts/worklet/client.py"
      via: "download_attachment() call"
      pattern: "download_attachment.*dest"
    - from: "scripts/worklet/service.py"
      to: "scripts/worklet/client.py"
      via: "download_attachment() call"
      pattern: "download_attachment.*dest"
---

<objective>
Implement atomic .tmp rename pattern in download_attachment for CLIENT-02 requirement.

Purpose: Ensure large file downloads are atomic (write to .tmp, rename on success, cleanup on failure).
Output: Modified download_attachment method with atomic write pattern.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
## Current download_attachment implementation
@scripts/worklet/client.py:233-255

Current code:
```python
def download_attachment(self, attachment_id: int, timeout: tuple[float, float] | float | None = None) -> bytes:
    ...
    response = self.session.get(url, stream=True, timeout=timeout)
    response.raise_for_status()
    ...
    return response.content
```

## Required atomic pattern
1. Add `dest: Path | None = None` parameter
2. If `dest` is None, return bytes (backward compatible)
3. If `dest` is provided:
   - Create temp file alongside dest (same directory, .tmp suffix)
   - Stream response.content to temp file
   - On success: atomic rename temp -> dest
   - On failure: delete temp file, re-raise

## Callers that will pass dest path
- scripts/worklet/sources/zentao.py:171 - `content = self.client.download_attachment(att.id)` then `file_path = attach_dir / att.file_name`
- scripts/worklet/service.py:154 - same pattern

After this change, callers should pass the dest path for atomic writes.
</context>

<tasks>

<task type="auto">
  <name>Task 1: Implement atomic .tmp rename in download_attachment</name>
  <files>scripts/worklet/client.py</files>
  <action>
    <read_first>scripts/worklet/client.py</read_first>

    Modify the `download_attachment` method (lines 233-255) to:

    1. Add `dest: Path | None = None` parameter
    2. When `dest` is provided:
       - Create temp file in same directory as dest using `tempfile.NamedTemporaryFile(mode='wb', dir=dest.parent, suffix='.tmp', delete=False)`
       - Stream response to temp file via `shutil.copyfileobj(response.raw, tmp_file)` for memory efficiency
       - Close tmp file
       - On success: use `os.replace(tmp_name, dest)` for atomic rename
       - On failure: delete tmp file via `Path(tmp_name).unlink(missing_ok=True)`
    3. When `dest` is None: return response.content (backward compatible)

    Add `import shutil` and `import tempfile` and `from pathlib import Path` at the top of the file if not already present.

    The signature should be:
    ```python
    def download_attachment(self, attachment_id: int, timeout: tuple[float, float] | float | None = None, dest: Path | None = None) -> bytes | None:
    ```

    Important: Use `response.raw` with `shutil.copyfileobj` instead of `response.content` for true streaming to avoid loading large files into memory.
  </action>
  <verify>
    <automated>python3 -c "
from pathlib import Path
import tempfile
import os

# Check the method signature has dest parameter
from worklet.client import WorkletClient
import inspect
sig = inspect.signature(WorkletClient.download_attachment)
params = list(sig.parameters.keys())
print(f'Parameters: {params}')
assert 'dest' in params, 'dest parameter missing'

# Check tempfile and shutil are used (verify code exists)
import worklet.client as client_module
import inspect
source = inspect.getsource(client_module.WorkletClient.download_attachment)
assert 'NamedTemporaryFile' in source, 'NamedTemporaryFile not found in source'
assert 'shutil.copyfileobj' in source or 'copyfileobj' in source, 'streaming copy not found'
print('OK: atomic pattern implemented')
"</automated>
  </verify>
  <done>download_attachment accepts dest parameter, uses NamedTemporaryFile with atomic rename via os.replace, cleans up temp file on failure</done>
</task>

</tasks>

<verification>
- Method signature includes `dest: Path | None = None` parameter
- Code uses tempfile.NamedTemporaryFile for atomic writes
- Code uses shutil.copyfileobj for streaming (not response.content)
- Code uses os.replace for atomic rename
- Temp file deleted on failure
</verification>

<success_criteria>
- download_attachment() has optional dest parameter for atomic writes
- Large file downloads stream to temp file then atomically rename to final path
- Failed downloads do not leave partial .tmp files
- Backward compatible when dest=None (returns bytes)
</success_criteria>

<output>
After completion, create `.planning/phases/02-core-pipeline/02-GAP-02-SUMMARY.md`
</output>

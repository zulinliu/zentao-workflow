---
phase: 03-extended-sources-and-testing
status: planned
---

# Phase 3: Validation Strategy

## Validation Architecture

### Test Suite Design

| Test Category | Files | Coverage |
|---------------|-------|----------|
| Config tests | test_config.py | WorkletConfig load/save/validation |
| Source tests | test_sources.py | ZentaoSource/FileSource/FolderSource |
| Exporter tests | test_exporter.py | HTML→MD conversion, edge cases |
| Reader tests | test_readers.py | MD/PDF/DOCX/Image reading |

### Fixtures Required

- `temp_dir`: Temporary directory for test files
- `mock_config`: Mock WorkletConfig
- `sample_markdown`: Sample .md file
- `sample_pdf`: Sample PDF file
- `mock_zentao_response`: Mock API response

### MarkItDown Validation

- PDF text extraction via `MarkItDown().convert(path).text_content`
- DOCX text extraction via same API
- Image: copy-only, no processing

### Behavior Verification

| Behavior | Verification |
|----------|--------------|
| Lazy import | `try: import markitdown; except ImportError:` pattern |
| Skip + warning | Unsupported format prints warning |
| FolderSource recursive | `rglob(f"*.{{{exts}}}")` with `follow_symlinks=False` |

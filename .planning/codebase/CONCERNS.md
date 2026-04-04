# Codebase Concerns

**Analysis Date:** 2026-04-04

## Tech Debt

**Project Feature Incomplete - Project-Level Download:**
- Issue: `fetchProject()` method in Java codebase throws "项目下载功能待实现" (Project download feature not yet implemented)
- Files: `scripts/java-src/src/main/java/com/tsintergy/chandao/service/ChandaoService.java` (line 99-100)
- Impact: Users cannot use `-P` or `--project` flags to batch download all stories/tasks/bugs in a project; feature advertised in CLI but not functional
- Fix approach: Implement project-level API query to fetch all items under a project ID, then call existing `fetchById()` for each item

**Version Number Mismatch Across Documentation:**
- Issue: `VERSION` file shows 1.6.0, but `README.md` badge shows 1.5.0
- Files: 
  - `VERSION` (shows 1.6.0)
  - `README.md` line 3 (shows 1.5.0)
  - `CLAUDE.md` line 11 (shows 1.6.0)
  - `SKILL.md` line 4 and throughout (shows 1.6.0)
- Impact: Users unclear about actual current version; CI/CD pipeline may generate inconsistent release artifacts
- Fix approach: Update `README.md` badge to 1.6.0 to match VERSION file and other documentation

**Generic Exception Handling in Java Runtime:**
- Issue: Java code uses bare `Exception` class instead of specific exception types
- Files: 
  - `scripts/java-src/src/main/java/com/tsintergy/chandao/service/ChandaoService.java` (lines 45, 60, 94, 99)
  - Generic exceptions catch too broad error categories and lose stack trace context
- Impact: Harder to debug failures; error messages non-specific ("登录失败", "请指定要下载的ID或项目"); difficult for exception handling logic
- Fix approach: Replace generic `Exception` with specific types (`IOException` for network, `IllegalArgumentException` for parameters, etc.); ensure root cause included in exception messages

**Python Image Regex Pattern Incomplete:**
- Issue: Image regex pattern in `service.py` line 137 calls `re.findall()` but discards results without using return value
- Files: `scripts/chandao_fetch/service.py` line 137
- Impact: No functional issue (loop on line 138 processes correctly), but code pattern is confusing and potentially indicates incomplete refactoring
- Fix approach: Remove unnecessary `re.findall()` call; only use `re.finditer()` loop

**Missing Timeout Configuration in Python Runtime:**
- Issue: `ChandaoClient.download_attachment()` and `download_image()` in Python do not set request timeout
- Files: 
  - `scripts/chandao_fetch/client.py` lines 249, 265
  - Python requests will hang indefinitely on network stall without timeout
- Impact: Long downloads or slow networks can block skill execution indefinitely; user must force-kill Claude process
- Fix approach: Add timeout parameter to requests in `download_attachment()` and `download_image()` methods; use configured `read_timeout` value

## Known Bugs

**Subtask Description Field Incomplete - Workaround Only:**
- Symptoms: Subtasks (e.g., task 61563) return empty `desc` field from Zentao API; parent task info unavailable in subtask response
- Files: 
  - SKILL.md Step 3.5-3.6 documents the workaround
  - Code does not detect subtasks automatically; users must manually request related story/parent download
- Trigger: Creating or managing subtasks; the v1.6.0 changelog identifies task 61563 as test case
- Workaround: v1.6.0 added Step 3.5 to detect empty descriptions and prompt auto-download of related story + parent task; this is a SKILL-level workaround, not a client-level fix; API limitation remains
- Status: Documented in CHANGELOG.md as "Fixed" in v1.6.0, but actual fix is workflow automation, not API integration

**Untested Windows Path Handling in Python:**
- Symptoms: Path handling in `service.py` and `exporter.py` uses forward slashes and `Path` objects; Windows backslash paths may not work correctly
- Files: 
  - `scripts/chandao_fetch/service.py` lines 42, 53, 63 (Path construction)
  - `scripts/chandao_fetch/exporter.py` (Path construction with forward slashes in comments)
- Trigger: Running on Windows with non-ASCII directory names or spaces
- Status: Code uses `pathlib.Path` which is cross-platform, but relative paths in comments hardcode `/` which may confuse Windows users

## Security Considerations

**Plaintext Password Storage in Configuration File:**
- Risk: Credentials stored in `.chandao/config.properties` in plaintext; if workspace or home directory is compromised, credentials exposed
- Files: 
  - `scripts/chandao_fetch/config.py` lines 112-136 (writes plaintext password)
  - `scripts/java-src/src/main/java/com/tsintergy/chandao/config/ChandaoConfig.java` (similar plaintext storage)
- Current mitigation: Configuration file written with default umask (typically 0644 on Linux, readable by all); project assumes single-user development machines
- Recommendations: 
  - Add file permission enforcement: write config with mode 0600 (owner-read-write only)
  - Document in README.md that config file contains plaintext credentials and must not be committed
  - Consider environment variable support as alternative to file storage (already supported via command-line args)
  - Add `.chandao/` to `.gitignore` with explanatory comment

**Credential Passed via Command-Line Arguments:**
- Risk: `--password` flag visible in process list and shell history
- Files: 
  - `scripts/chandao_fetch/__main__.py` lines 34-35
  - Users may accidentally commit command history or share terminal recordings
- Current mitigation: None; skill documentation does not warn about this
- Recommendations: 
  - Add warning in SKILL.md Step 2: "Do not pass password via command-line; use configuration file only"
  - Consider interactive password prompt if both username and password are required but not provided

**Inadequate HTTP Error Validation:**
- Risk: Both Java and Python clients use generic `response.ok` / `isSuccessful()` checks, but don't validate JSON error responses from Zentao API
- Files: 
  - `scripts/chandao_fetch/client.py` lines 57-69 (checks HTTP status, but JSON error field ignored)
  - `scripts/java-src/src/main/java/com/tsintergy/chandao/client/ChandaoClient.java` lines 81-108
- Impact: 404 or 403 responses return valid JSON with error message, but code only checks HTTP status code
- Current mitigation: Error messages extracted from JSON response (lines 68 in Python, lines 106 in Java)
- Recommendations: 
  - Add explicit API error status validation before attempting JSON parsing
  - Validate `result` or `status` field in response before processing data

## Performance Bottlenecks

**Sequential Attachment Download in Serial:**
- Problem: Multiple attachments downloaded one-at-a-time in `_download_attachments()`
- Files: `scripts/chandao_fetch/service.py` lines 74-90 (loop on line 78)
- Cause: `requests.Session` configured with timeout but no connection pooling or concurrent requests; each attachment blocks until download completes
- Impact: If 20 attachments exist, download time = 20 × (network latency + transfer time); skill execution time increases proportionally
- Improvement path: 
  - Use `ThreadPoolExecutor` or `asyncio` for concurrent downloads (max 5-10 workers)
  - Add progress reporting with number completed / total
  - Implement retry logic with exponential backoff for failed downloads

**Image Extraction Regex Pattern Applied Multiple Times:**
- Problem: Image regex in `exporter.py` line 192 matches same content as service.py line 109
- Files: 
  - `scripts/chandao_fetch/exporter.py` lines 202-214
  - `scripts/chandao_fetch/service.py` lines 109-110 (nearly identical pattern)
- Impact: Content processed twice through regex; minor overhead but indicates incomplete refactoring
- Improvement path: Move image path conversion to service layer, store results in model object

**Large HTML-to-Markdown Conversion Without Streaming:**
- Problem: `_html_to_markdown()` loads entire content into memory and applies 40+ regex substitutions sequentially
- Files: `scripts/chandao_fetch/exporter.py` lines 216-302
- Cause: Each `re.sub()` creates new string copy; 50KB content = 50 string copies in memory
- Impact: For large specifications or bug reports (e.g., 1MB of HTML), conversion may consume significant memory
- Improvement path: Compile regex patterns once, use single-pass conversion or regex tokenizer; cache compiled patterns

## Fragile Areas

**HTML to Markdown Conversion - Complex Regex Chains:**
- Files: `scripts/chandao_fetch/exporter.py` lines 216-302
- Why fragile: 40+ sequential regex patterns applied to HTML content; order of application matters; edge cases not covered
  - Table conversion (lines 268-279) assumes simple `<td>` / `<th>` structure, breaks on nested tables or rowspan/colspan
  - Link conversion (line 265) doesn't handle relative links or anchor-only links correctly
  - List conversion (lines 241-246) doesn't handle nested lists
  - Code block conversion (line 261) treats `<pre>` content as plain text, losing syntax highlighting hints
- Safe modification: 
  - Add comprehensive test cases for each HTML tag type before modifying
  - Consider using HTML parser library (like `html.parser` or `beautifulsoup`) instead of regex chains
  - Test with samples from actual Zentao installations
- Test coverage: `MarkdownExporterTest.java` and `MarkdownExporterCoverageTest.java` exist but may not cover all edge cases

**API Response Data Structure Assumptions:**
- Files: 
  - `scripts/chandao_fetch/client.py` lines 102-108 (assumes `data.story` or `data` structure)
  - `scripts/java-src/src/main/java/com/tsintergy/chandao/client/ChandaoClient.java` lines 107-108
- Why fragile: Code assumes response structure but doesn't validate it; if Zentao API returns different field names or nesting, parsing silently fails and returns null values
- Safe modification: 
  - Add explicit schema validation for each response type (Story, Task, Bug)
  - Add test cases that mock API responses for each Zentao version
  - Log parsed data structure for debugging

**Filename Sanitization Length Limit:**
- Files: `scripts/chandao_fetch/exporter.py` line 335-339
- Why fragile: Hardcoded 50-character limit for sanitized filenames may truncate important title information and cause collisions
- Safe modification: 
  - Make length limit configurable
  - Hash remaining characters instead of truncating to preserve uniqueness
  - Document this limit in SKILL.md

**Configuration File Parsing No Validation:**
- Files: `scripts/chandao_fetch/config.py` lines 87-110
- Why fragile: Reads `.properties` file but doesn't validate:
  - Required keys missing (zentao.url)
  - URL format invalid
  - Credentials contain special characters that break parsing
  - Empty values allowed
- Safe modification: 
  - Add validation in `ChandaoConfig._load_from_file()` to check required fields
  - Validate URL format (must start with http/https)
  - Add unit tests for malformed config files

## Scaling Limits

**Batch Download Limited to Single Session:**
- Current capacity: CLI supports `--ids` with comma-separated list (line 59 in `__main__.py`), but all downloads use single login session
- Limit: If any single item fails to download, subsequent items may fail if error corrupts session state
- Scaling path: 
  - Implement session re-login between failed downloads
  - Add per-item error handling and continue on failure
  - Queue failed items for retry

**No Rate Limiting or Backoff:**
- Current capacity: Downloads proceed at maximum speed, no delay between requests
- Limit: Zentao server may rate-limit or block rapid request sequences; no retry logic implemented
- Scaling path: 
  - Add configurable delay between requests (e.g., 100ms)
  - Implement exponential backoff on HTTP 429 (Too Many Requests) or 503 (Service Unavailable)
  - Document rate limit settings

**Memory Usage for Large Attachments:**
- Current capacity: Entire file loaded into memory with `response.content` (Python client.py line 254)
- Limit: Multi-gigabyte files cannot be downloaded (OOM crash)
- Scaling path: 
  - Stream file to disk in chunks instead of loading entire file
  - Add progress indicator for large files
  - Implement resumable downloads

## Dependencies at Risk

**jackson-databind Security Updates Required:**
- Risk: `jackson-databind` v2.15.2 used in Java (pom.xml line 20); check for published CVEs
- Impact: JSON parsing security vulnerabilities could be exploited if processing untrusted Zentao API responses
- Migration plan: Regularly update Jackson to latest patch version; set up Dependabot alerts

**OkHttp 4.12.0 End of Life Approaching:**
- Risk: okhttp3 v4.12.0 (pom.xml line 29) released in Nov 2023; v5.x is current; v4.x may reach EOL
- Impact: Security patches may stop being released
- Migration plan: Plan upgrade to okhttp v5.x (breaking changes likely); test thoroughly with existing endpoints

**Python requests >= 2.28.0 Minimal Constraint:**
- Risk: `requirements.txt` specifies `requests>=2.28.0` but no upper bound
- Impact: Major version 3.x when released may introduce breaking changes
- Migration plan: Update to `requests>=2.28.0,<4.0` to pin major version

## Missing Critical Features

**Project-Level Download Unimplemented:**
- Problem: CLI accepts `--project-id` but not implemented
- Blocks: Users cannot bulk download all items in a project; must download individually by ID
- Fix approach: Implement by querying `/project-task-list.json` to enumerate all stories/tasks, then iterate

**No Dry-Run Mode:**
- Problem: Users cannot preview what would be downloaded without actually downloading
- Blocks: Users cannot validate configuration without generating files
- Fix approach: Add `--dry-run` flag to list items without downloading attachments

**No Resume/Checkpoint for Large Downloads:**
- Problem: If network fails mid-download (20+ attachments), must start over from item 1
- Blocks: Unreliable on slow networks or with large workspaces
- Fix approach: Store progress in JSON file, skip already-downloaded items on retry

## Test Coverage Gaps

**No End-to-End Integration Tests:**
- What's not tested: Actual connection to real Zentao server; full download + export workflow
- Files: All test files are unit tests with mocks; no integration test suite
- Risk: Breaking API changes in Zentao go undetected until user reports them
- Priority: **High** - should add optional integration tests against test Zentao instance

**Attachment Download Scenarios Minimally Tested:**
- What's not tested: 
  - Large files (>100MB)
  - Files with special characters in names
  - HTTP redirects or authentication challenges
  - Concurrent downloads from mixed fast/slow connections
  - Attachment count > 100
- Files: No dedicated attachment test class; coverage in `ChandaoServiceTest.java` is mock-based
- Risk: Real-world attachment downloads may fail silently
- Priority: **Medium** - add test fixtures for edge cases

**HTML-to-Markdown Edge Cases Not Covered:**
- What's not tested: 
  - Nested HTML structures (nested lists, nested tables)
  - Mixed inline and block elements
  - Non-standard Zentao HTML variants
  - Scripts or event handlers in content (security)
  - CDATA sections or unusual entity encodings
- Files: `MarkdownExporterTest.java` and `MarkdownExporterCoverageTest.java` exist but edge case coverage unclear
- Risk: Users may see malformed Markdown output for certain content types
- Priority: **Medium** - add parametrized tests with real Zentao HTML samples

**Python Package Import Errors Not Tested:**
- What's not tested: 
  - Missing `requests` library
  - Python version < 3.6
  - Encoding issues on different locales
- Files: No Python test suite found; only Java tests
- Risk: Users on Python 2 or without requests library get cryptic errors
- Priority: **Low** - add pre-flight checks in `__main__.py`

**Configuration File Parsing Malformed Input:**
- What's not tested: 
  - Missing `=` delimiter
  - Empty file
  - Non-UTF8 encoding
  - Very long lines
- Files: `ChandaoConfigTest.java` exists but coverage of error cases unclear
- Risk: Malformed config silently skipped; defaults used instead
- Priority: **Low** - add validation tests

---

*Concerns audit: 2026-04-04*

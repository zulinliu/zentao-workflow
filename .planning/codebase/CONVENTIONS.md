# Coding Conventions

**Analysis Date:** 2026-04-04

## Naming Patterns

**Files:**
- Java classes: PascalCase (e.g., `ChandaoClient.java`, `MarkdownExporter.java`)
- Python modules: snake_case (e.g., `chandao_fetch.py`, `client.py`, `exporter.py`)
- Test files: Java follows `{ClassName}Test.java` and `{ClassName}EdgeCaseTest.java`; Python has no test files in repo

**Functions/Methods:**
- Java: camelCase (e.g., `exportStory()`, `parseAttachments()`, `sanitizeFileName()`)
- Python: snake_case (e.g., `export_story()`, `_download_attachments()`, `_process_content()`)
- Private methods prefixed with underscore in both languages

**Variables:**
- Java: camelCase (e.g., `baseUrl`, `outputDir`, `connectTimeout`)
- Python: snake_case (e.g., `base_url`, `output_dir`, `connect_timeout`)
- Constants in Java: UPPER_SNAKE_CASE (e.g., `DEFAULT_CONFIG_FILE`)

**Types:**
- Java: Model classes use wrapper types and generics
  - `Long` for IDs (nullable)
  - `String` for text fields
  - `List<Attachment>` for collections
  - `Float` for numeric values (e.g., `estimate`, `consumed`)
- Python: Python dataclasses with `Optional[T]` for nullable fields
  - `Optional[int]` for IDs
  - `Optional[str]` for text
  - `List[T]` for collections

## Code Style

**Formatting:**
- Java: Standard Java formatting (4-space indentation)
- Python: 4-space indentation per PEP 8
- Both: UTF-8 encoding enforced
- Both: Unix line endings (LF)

**Linting:**
- Java: Maven compiler enforces Java 1.8 target (`<maven.compiler.target>1.8</maven.compiler.target>`)
- Python: No linting tools configured; follows PEP 8 conventions informally
- Java: JaCoCo code coverage checking enforced in pom.xml with minimum line coverage of 85%

**Line Length:**
- Both: Documentation strings and comments wrap reasonably
- Python: Uses f-strings for string formatting (e.g., `f"{story.id} - {story.title}"`)

## Import Organization

**Order:**
1. Standard library imports (Java: `java.*`, Python: `os`, `re`, `sys`)
2. Third-party imports (Java: `com.beust`, `okhttp3`, `org.slf4j`; Python: `requests`, `Path`)
3. Local imports (Java: `com.tsintergy.*`; Python: relative imports with `.module`)

**Path Aliases:**
- Java: No aliases, uses full package names
- Python: Relative imports within package (e.g., `from .config import ChandaoConfig`)

**Examples:**
- Java (`ChandaoClient.java`):
  ```java
  import com.fasterxml.jackson.databind.*;
  import com.tsintergy.chandao.config.ChandaoConfig;
  import com.tsintergy.chandao.model.Story;
  import okhttp3.*;
  import org.slf4j.Logger;
  ```

- Python (`client.py`):
  ```python
  import json
  import re
  from typing import List, Optional
  from urllib.parse import urljoin
  import requests
  from .config import ChandaoConfig
  from .models import Attachment, Bug, Story, Task
  ```

## Error Handling

**Patterns:**
- Java: Throws checked exceptions; callers decide handling
  - Example: `public boolean login() throws IOException`
  - Logs errors using SLF4J before throwing: `log.error("登录失败: {}", e.getMessage(), e);`
  - Exception wrapping: `throw new IOException("登录失败: " + message);`

- Python: Raises generic `Exception` with descriptive messages
  - Example: `raise Exception(f"登录失败: {message}")`
  - Try-catch blocks at service layer and CLI entry point
  - Graceful degradation: Attachment download failures are logged but don't stop processing

**Exception Handling Locations:**
- `ChandaoFetchApplication.main()` (Java): Top-level try-catch logs and exits with code 1
- `__main__.main()` (Python): Catches and prints error messages; uses `--verbose` to show tracebacks
- Service layer (`ChandaoService`, `service.py`): Catches attachment/image download failures but logs and continues

## Logging

**Framework:** 
- Java: SLF4J with Logback backend (`logback.xml` configured in pom.xml)
- Python: `print()` statements, no structured logging framework

**Patterns:**
- Java logging levels:
  - `log.info()`: Success messages (e.g., "登录成功: {username}")
  - `log.warn()`: Non-critical failures (e.g., attachment parsing failures)
  - `log.error()`: Critical failures with stack traces

- Example from `ChandaoClient.java`:
  ```java
  log.info("登录成功: {}", config.getUsername());
  log.warn("解析附件失败: {}", e.getMessage());
  log.error("执行失败: {}", e.getMessage(), e);
  ```

- Python: Direct `print()` statements to stdout for user feedback
  - `print("已加载配置文件: {path}")` - success
  - `print(f"下载附件失败: {att.id} - {att.title}: {e}")` - warnings
  - Verbose flag enables traceback printing: `traceback.print_exc()`

## Comments

**When to Comment:**
- Java: Class-level JavaDoc for public classes (e.g., `/** 禅道API客户端 */`)
- Java: Method-level JavaDoc for public methods with detailed parameter descriptions
- Python: Module-level docstring at top (e.g., `"""禅道数据抓取工具 - API客户端模块"""`)
- Python: Method docstrings with Args and Returns sections (Google style)

**Example from Python (`service.py`):**
```python
def _download_content_images(self, content: Optional[str], attach_dir: Path) -> Optional[str]:
    """下载内容中的图片

    只下载图片，不修改内容。图片路径的转换由exporter处理。

    Args:
        content: 原始内容（可能包含<img>标签）
        attach_dir: 附件保存目录

    Returns:
        原始内容（不变）
    """
```

**Example from Java (`ChandaoClient.java`):**
```java
/**
 * 禅道API客户端
 * 
 * 【安全约束】只允许查询操作，禁止新增/修改/删除
 * - 允许：登录、查看详情、下载附件
 * - 禁止：创建、更新、删除、指派、关闭等写操作
 */
public class ChandaoClient {
```

## Function Design

**Size:** 
- Java: Methods stay under 100 lines; parsing logic broken into helpers (`parseAttachments()`, `fetchJson()`)
- Python: Functions under 80 lines; content processing delegated to exporter

**Parameters:** 
- Java: Use builder patterns for command-line args; limit method parameters to 5 or fewer
- Python: Use dataclass models for data transfer; explicit keyword arguments for options

**Return Values:** 
- Java: Explicit null checks before returning; use Optional-like patterns sparingly
- Python: Return tuples or dataclass instances; raise Exception for errors rather than returning None

**Example of parameter design:**
- Java (`CommandLineArgs.getIdList()`):
  ```java
  public List<Long> getIdList() {
      List<Long> result = new ArrayList<>();
      if (ids != null && !ids.isEmpty()) {
          for (String s : ids.split(",")) {
              try {
                  result.add(Long.parseLong(s.trim()));
              } catch (NumberFormatException e) {
                  // skip invalid
              }
          }
      }
      if (id != null) {
          result.add(id);
      }
      return result;
  }
  ```

- Python (`__main__.main()`):
  ```python
  service = ChandaoService(config)
  service.execute(
      content_type=args.type,
      ids=ids,
      download_attachments=not (args.no_attachment and args.no_image)
  )
  ```

## Module Design

**Exports:**
- Java: All public classes exported; package structure mirrors functionality
  - `com.tsintergy.chandao.config.*` - Configuration
  - `com.tsintergy.chandao.client.*` - HTTP client
  - `com.tsintergy.chandao.model.*` - Data models
  - `com.tsintergy.chandao.service.*` - Business logic

- Python: Explicit imports in `__main__.py`
  ```python
  from .config import ChandaoConfig
  from .service import ChandaoService
  ```

**Barrel Files:** 
- Not used; imports are explicit and direct
- Python `__init__.py` is minimal (no re-exports)

## Configuration Management

**Precedence (Java & Python):**
1. Command-line arguments (highest priority)
2. Workspace config file: `.chandao/config.properties` (if workspace_dir provided)
3. Global config file: `~/.chandao/config.properties` (if exists)
4. Defaults (lowest priority)

**Java Implementation (`ChandaoConfig.load()`):**
```java
private static Path getConfigPath(String configPath) {
    if (configPath != null && !configPath.isEmpty()) {
        return Paths.get(configPath);
    }
    return Paths.get(System.getProperty("user.home"), DEFAULT_CONFIG_FILE);
}
```

**Python Implementation (`ChandaoConfig.load()`):**
```python
@classmethod
def _get_config_files(cls, workspace_dir: Optional[str], config_path: Optional[str]) -> List[Path]:
    """获取配置文件列表，按优先级排序"""
    files = []
    if config_path:
        files.append(Path(config_path))
    if workspace_dir:
        workspace_config = Path(workspace_dir) / cls.WORKSPACE_CONFIG
        files.append(workspace_config)
    global_config = Path.home() / ".chandao" / "config.properties"
    files.append(global_config)
    return files
```

## Security Constraints

**Read-Only Operations Only:**
- All API clients restricted to read-only: login, view details, download attachments
- Explicitly documented in code comments
- No write operations (create, update, delete, assign, close) implemented

From `ChandaoClient.java`:
```java
/**
 * 【安全约束】只允许查询操作，禁止新增/修改/删除
 * - 允许：登录、查看详情、下载附件
 * - 禁止：创建、更新、删除、指派、关闭等写操作
 */
```

---

*Convention analysis: 2026-04-04*

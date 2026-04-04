# Technology Stack

**Analysis Date:** 2026-04-04

## Languages

**Primary:**
- Python 3.6+ - Core download tools and CLI implementation (`scripts/chandao_fetch/`)
- Java 8+ - Alternative runtime for fetch tool (`scripts/java-src/`)

**Secondary:**
- YAML - Skill manifest and CI/CD configuration
- Markdown - Documentation and output format

## Runtime

**Environment:**
- Java 8+ (optional, for better performance) - Primary choice when available
- Python 3.6+ (default fallback) - Lightweight alternative
- superpowers 5.0.6+ (Claude Code plugin, required for v1.5.0+ technical plan generation)

**Package Manager:**
- Maven 3.6+ (Java build, `scripts/java-src/pom.xml`)
- pip/pip3 (Python package manager)
- Lockfile: Python uses `scripts/requirements.txt`

## Frameworks

**Core:**
- requests 2.28.0+ (HTTP client for Python downloads, `scripts/chandao_fetch/client.py`)
- OkHttp 4.12.0 (Java HTTP client, see `scripts/java-src/pom.xml`)

**CLI:**
- jcommander 1.82 (Java CLI argument parsing)
- Python argparse (standard library, native CLI parsing in `scripts/chandao_fetch/__main__.py`)

**Data Serialization:**
- Jackson 2.15.2 (Java JSON serialization/deserialization)
- requests JSON handling (Python native)

**Logging:**
- SLF4J 2.0.9 + Logback 1.3.11 (Java structured logging)
- Python print statements (simple console logging in all modules)

**Utilities:**
- Apache Commons Lang3 3.13.0 (Java string and object utilities)

## Key Dependencies

**Critical:**
- requests 2.28.0+ (Python) - HTTP communication with Zentao API, only requirement in `scripts/requirements.txt`
- OkHttp 4.12.0 (Java) - HTTP requests in `scripts/java-src/`
- Jackson databind 2.15.2 (Java) - JSON parsing for API responses in `scripts/java-src/`

**Infrastructure:**
- Maven Compiler Plugin 3.11.0 - Java compilation targeting JDK 1.8
- Maven Shade Plugin 3.5.1 - Fat JAR generation for standalone execution
- Maven Assembly Plugin 3.6.0 - Distribution packaging

**Testing & Quality:**
- JUnit 4.13.2 (Java unit testing)
- Mockito 4.11.0 (Java mocking framework)
- OkHttp MockWebServer 4.12.0 (Java HTTP mocking)
- JaCoCo 0.8.11 (Java code coverage - 85% line coverage, 60% branch coverage enforced in `scripts/java-src/pom.xml`)
- Maven Surefire 3.1.2 (Java test execution)

## Configuration

**Environment:**
- Configuration file: `~/.chandao/config.properties` (global) or `.chandao/config.properties` (workspace-local)
- Format: Java Properties format (key=value)
- Priority order: Command-line arguments > workspace config > global config > defaults

**Config file format** (see `scripts/assets/config_template.properties`):
```properties
zentao.url=https://your-zentao-server.com
zentao.username=your_username
zentao.password=your_password
output.dir=/path/to/output
connect.timeout=30000
read.timeout=60000
download.threads=3
```

**Build:**
- Maven configuration: `scripts/java-src/pom.xml` (builds to `scripts/chandao-fetch.jar`)
- GitHub Actions: `.github/workflows/release.yml` (automated release packaging)
- Version: `VERSION` file (semantic versioning)

## Platform Requirements

**Development:**
- Java 8+ (for building Java version)
- Python 3.6+ (for running Python version or development)
- Maven 3.6+ (for Java builds)
- Git (for version control)

**Production (Runtime):**
- Java 8+ OR Python 3.6+ (mutually exclusive, tool auto-selects Java if available)
- No external database or services required beyond Zentao API access
- superpowers plugin 5.0.6+ (Claude Code Skill dependency for v1.5.0+)

**File I/O Requirements:**
- Read/write access to workspace directory for outputs
- Network access to Zentao API endpoints (HTTP/HTTPS)
- Optional: Write access to `~/.chandao/` for global configuration storage

---

*Stack analysis: 2026-04-04*

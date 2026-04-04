# Testing Patterns

**Analysis Date:** 2026-04-04

## Test Framework

**Runner:**
- Java: JUnit 4.13.2 (Maven Surefire plugin)
- Config: `pom.xml` with Maven Surefire (`maven-surefire-plugin` v3.1.2)
- Python: No test framework (no tests present in codebase)

**Assertion Library:**
- Java: JUnit's `Assert.*` (static imports)
  - `assertEquals()`, `assertTrue()`, `assertFalse()`, `assertNull()`, `assertNotNull()`
  - `@Test(expected = IOException.class)` for exception testing

**Run Commands:**
```bash
# Java: Run all tests (Maven)
mvn test

# Java: Run specific test class
mvn test -Dtest=ChandaoConfigTest

# Java: Run with coverage
mvn test jacoco:report

# Python: No test runner (tests not implemented)
```

## Test File Organization

**Location:**
- Java: Mirrored package structure under `src/test/java`
  - Production: `src/main/java/com/tsintergy/chandao/{package}/{ClassName}.java`
  - Tests: `src/test/java/com/tsintergy/chandao/{package}/{ClassName}Test.java`

**Naming:**
- Java: `{ClassName}Test.java` for unit tests
- Java: `{ClassName}EdgeCaseTest.java` for edge case tests
- Java: `{ClassName}CoverageTest.java` for coverage-specific tests

**Structure:**
```
src/test/java/com/tsintergy/chandao/
├── config/
│   └── ChandaoConfigTest.java
├── client/
│   ├── ChandaoClientTest.java
│   └── ChandaoClientInternalTest.java
├── model/
│   ├── AttachmentTest.java
│   ├── BugTest.java
│   ├── StoryTest.java
│   └── TaskTest.java
└── service/
    ├── ChandaoServiceTest.java
    ├── MarkdownExporterTest.java
    ├── MarkdownExporterEdgeCaseTest.java
    └── MarkdownExporterCoverageTest.java
```

## Test Structure

**Suite Organization:**
Tests use JUnit 4 with `@Before` and `@After` lifecycle annotations:

```java
public class ChandaoConfigTest {
    
    private ChandaoConfig config;
    
    @Before
    public void setUp() {
        config = new ChandaoConfig();
    }
    
    @Test
    public void testGetBaseUrl() {
        config.setBaseUrl("https://zentao.example.com");
        assertEquals("https://zentao.example.com", config.getBaseUrl());
    }
}
```

**Patterns:**

1. **Setup/Teardown:**
   - `@Before`: Initialize test fixtures (e.g., temp directories, mocked servers)
   - `@After`: Clean up resources (e.g., delete temp files, shutdown servers)
   - Example from `MarkdownExporterTest.java`:
     ```java
     @Before
     public void setUp() throws IOException {
         tempOutputDir = Files.createTempDirectory("markdown-export-test");
         exporter = new MarkdownExporter(tempOutputDir.toString());
     }
     
     @After
     public void tearDown() throws IOException {
         deleteDirectory(tempOutputDir.toFile());
     }
     ```

2. **Assertion Pattern:**
   - Direct assertions on return values or object state
   - Files verified via `Files.exists()` and content checked with `Files.readAllBytes()`
   - Example from `MarkdownExporterTest.java`:
     ```java
     exporter.exportStory(story);
     Path storyFile = tempOutputDir.resolve("story/123-用户登录功能.md");
     assertTrue(Files.exists(storyFile));
     String content = new String(Files.readAllBytes(storyFile));
     assertTrue(content.contains("【用户登录功能】123"));
     ```

3. **Exception Testing:**
   - Uses `@Test(expected = IOException.class)` annotation
   - Example from `ChandaoClientTest.java`:
     ```java
     @Test(expected = IOException.class)
     public void testLogin_Failure_401() throws IOException {
         mockWebServer.enqueue(new MockResponse().setResponseCode(401));
         client.login();
     }
     ```

## Mocking

**Framework:** 
- Java: Mockito 4.11.0 for object mocking
- Java: OkHttp3 MockWebServer 4.12.0 for HTTP mocking

**Patterns:**

1. **HTTP Mocking with MockWebServer:**
   ```java
   private MockWebServer mockWebServer;
   
   @Before
   public void setUp() throws IOException {
       mockWebServer = new MockWebServer();
       mockWebServer.start();
       String baseUrl = mockWebServer.url("/").toString().replaceAll("/$", "");
       config.setBaseUrl(baseUrl);
   }
   
   @Test
   public void testLogin_Success() throws IOException {
       mockWebServer.enqueue(new MockResponse()
           .setResponseCode(200)
           .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
           .setBody("{\"result\":\"success\"}"));
       
       boolean result = client.login();
       assertTrue(result);
   }
   ```

2. **Reflection-based Private Method Testing:**
   - Used in `MarkdownExporterEdgeCaseTest.java` for private methods
   ```java
   @Test
   public void testProcessContent_Null() throws Exception {
       MarkdownExporter exporter = new MarkdownExporter("/tmp");
       Method method = MarkdownExporter.class.getDeclaredMethod("processContent", String.class);
       method.setAccessible(true);
       String result = (String) method.invoke(exporter, (String) null);
       assertEquals("", result);
   }
   ```

**What to Mock:**
- HTTP responses (using MockWebServer)
- Network failures (HTTP error codes)
- File system operations (create temp directories, verify file output)
- Private utilities (using reflection for edge cases)

**What NOT to Mock:**
- Core business logic (ChandaoConfig state management, MarkdownExporter formatting)
- Data model serialization/deserialization (use real objects)
- Configuration loading (test with real or temporary files)

## Fixtures and Factories

**Test Data:**
Model objects are created directly in test methods:

```java
@Test
public void testExportStory_WithProductName() throws IOException {
    Story story = new Story();
    story.setId(124L);
    story.setTitle("需求标题");
    story.setProductName("产品A");
    
    exporter.exportStory(story);
    
    Path storyFile = tempOutputDir.resolve("story/124-需求标题.md");
    String content = new String(Files.readAllBytes(storyFile));
    assertTrue(content.contains("产品A"));
}
```

**Location:**
- No separate fixture factory classes
- Test data created inline in each test method
- Shared fixtures (like temporary directories) created in `@Before` methods

## Coverage

**Requirements:** 
- Minimum line coverage: **85%** (enforced by JaCoCo in pom.xml)
- Minimum branch coverage: **60%**
- Main application class excluded from coverage: `ChandaoFetchApplication*`

**Configuration (pom.xml):**
```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <configuration>
        <excludes>
            <exclude>**/ChandaoFetchApplication*</exclude>
        </excludes>
    </configuration>
    <executions>
        <execution>
            <id>check</id>
            <goals>
                <goal>check</goal>
            </goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.85</minimum>
                            </limit>
                            <limit>
                                <counter>BRANCH</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.60</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

**View Coverage:**
```bash
mvn clean test jacoco:report
# Report generated in: target/site/jacoco/index.html
```

## Test Types

**Unit Tests:**
- Scope: Individual classes in isolation
- Approach: Test one class per test file (e.g., `ChandaoConfigTest` tests `ChandaoConfig`)
- Files: `{ClassName}Test.java`
- Examples:
  - `ChandaoConfigTest.java`: Tests configuration loading, saving, initialization checks
  - `ChandaoClientTest.java`: Tests login and API calls with MockWebServer
  - `MarkdownExporterTest.java`: Tests markdown export formatting

**Integration Tests:**
- Not explicitly separate; MarkdownExporter tests verify file I/O with real temp directories
- `ChandaoClientTest` simulates integration with MockWebServer
- No separate integration test directory

**E2E Tests:**
- Not implemented
- Python version has no tests at all

## Common Patterns

**Async Testing:**
- Not applicable; both Java and Python implementations are synchronous
- No async/await or Future patterns in codebase

**Error Testing:**
Explicit exception testing with `@Test(expected = ...)`:

```java
@Test(expected = IOException.class)
public void testLogin_Failure_401() throws IOException {
    mockWebServer.enqueue(new MockResponse().setResponseCode(401));
    client.login();
}
```

Alternative: Direct catch and assertion (rarely used):
```java
@Test
public void testIsInitialized_EmptyStrings() {
    config.setBaseUrl("");
    config.setUsername("");
    config.setPassword("");
    assertFalse(config.isInitialized());
}
```

**Null/Edge Case Testing:**
Comprehensive null handling in `MarkdownExporterEdgeCaseTest.java`:

```java
@Test
public void testProcessContent_Null() throws Exception {
    MarkdownExporter exporter = new MarkdownExporter("/tmp");
    Method method = MarkdownExporter.class.getDeclaredMethod("processContent", String.class);
    method.setAccessible(true);
    
    String result = (String) method.invoke(exporter, (String) null);
    assertEquals("", result);
}

@Test
public void testProcessContent_Empty() throws Exception {
    MarkdownExporter exporter = new MarkdownExporter("/tmp");
    Method method = MarkdownExporter.class.getDeclaredMethod("processContent", String.class);
    method.setAccessible(true);
    
    String result = (String) method.invoke(exporter, "");
    assertEquals("", result);
}
```

**File Output Testing:**
Tests verify output files exist and contain expected content:

```java
@Test
public void testExportBug_WithAttachments() throws IOException {
    Bug bug = new Bug();
    bug.setId(791L);
    bug.setTitle("带截图的Bug");
    
    Attachment screenshot = new Attachment();
    screenshot.setId(1L);
    screenshot.setTitle("error.png");
    screenshot.setExtension("png");
    bug.setAttachments(Arrays.asList(screenshot));
    
    exporter.exportBug(bug);
    
    Path bugFile = tempOutputDir.resolve("bug/791-带截图的Bug.md");
    String content = new String(Files.readAllBytes(bugFile));
    assertTrue(content.contains("error.png"));
    assertTrue(content.contains("![error.png]"));
}
```

## Python Testing Status

**Current State:**
- No unit tests implemented for Python modules
- Python version (`scripts/chandao_fetch/`) relies on manual testing with test IDs:
  - Bug: 66445
  - Story: 39382
  - Task: 61215

**Test Commands Used (Manual):**
```bash
cd scripts
pip install -r requirements.txt
python3 chandao_fetch.py -t bug -i 66445 -o /tmp/test-output
python3 chandao_fetch.py -t story -i 39382 -o /tmp/test-output
python3 chandao_fetch.py -t task -i 61215 -o /tmp/test-output
```

## Test Coverage Summary

**Well-Covered Areas:**
- `ChandaoConfig` (85+ test methods across 3 test classes)
- `MarkdownExporter` (20+ tests for various export scenarios)
- `ChandaoClient` API methods (login, fetch story/task/bug)

**Gaps:**
- `ChandaoService` main orchestration logic
- Python modules completely untested
- No E2E tests for complete workflow
- No load/stress testing

---

*Testing analysis: 2026-04-04*

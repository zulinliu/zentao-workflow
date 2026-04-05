# Phase 4: Pipeline Assembly and CLI - Context

**Gathered:** 2026-04-05
**Status:** Ready for planning

<domain>
## Phase Boundary

The tool auto-detects input type (folder vs file vs Zentao ID) and manages its runtime environment with smart caching. Phase 4 delivers InputParser auto-detection, environment caching, superpowers npx upgrade, and Java detection removal.

</domain>

<decisions>
## Implementation Decisions

### D-01: 输入类型检测 — 路径+扩展名检测
- **决策:** 使用 `Path().exists()` + 扩展名检测判断输入类型
- **逻辑:**
  1. `Path(identifier).exists()` 检查路径是否存在
  2. 如果存在且是文件：`is_file()` → 扩展名检测格式
  3. 如果存在且是文件夹：`is_dir()` → FolderSource
  4. 如果不存在：尝试 Zentao ID 正则匹配
- **理由:** 最清晰、最少副作用

### D-02: 环境缓存策略 — .worklet/ 缓存文件
- **决策:** 环境检测成功后写入 `.worklet/env_cache.json`，带 24h TTL
- **缓存内容:** `{backend: "python", version: "3.x", superpowers: true/false, cached_at: timestamp}`
- **TTL 逻辑:** 读取时检查 `cached_at`，超过 24h 则重新检测
- **理由:** 用户确认

### D-03: superpowers 安装 — npx
- **决策:** 使用 `npx -y superpowers` 安装和检测
- **检测:** `which npx` → `npx superpowers --version`
- **理由:** 无全局安装、版本可控

### D-04: Java 检测清理
- **决策:** 移除所有 Java 环境检测代码
- **验证:** `grep -r "java" scripts/` 应返回空

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — INPUT-09, ENV-01, ENV-02, ENV-03, ENV-04 完整需求定义
- `.planning/ROADMAP.md` §Phase 4 — Phase 4 目标、成功标准和依赖关系

### Prior Phase Context
- `.planning/phases/01-foundation-and-rename/01-CONTEXT.md` — Phase 1 决策
- `.planning/phases/02-core-pipeline/02-CONTEXT.md` — Phase 2 决策
- `.planning/phases/03-extended-sources-and-testing/03-CONTEXT.md` — Phase 3 决策

### Current Codebase
- `scripts/worklet/__main__.py` — CLI 入口，需修改支持 InputParser
- `scripts/worklet/sources/base.py` — SourceRegistry 已工作
- `scripts/worklet/sources/zentao.py` — ZentaoSource 实现
- `scripts/worklet/sources/file.py` — FileSource 实现
- `scripts/worklet/sources/folder.py` — FolderSource 实现

</canonical_refs>

<codebase_context>
## Existing Code Insights

### Reusable Assets
- `scripts/worklet/sources/` — 已有 ZentaoSource/FileSource/FolderSource 实现
- `scripts/worklet/__main__.py` — 现有 CLI 入口，需增加 InputParser

### Established Patterns
- SourceRegistry.entry_points 自动发现
- lazy import 模式

### Integration Points
- `__main__.py` — 新增 InputParser 调用
- `.worklet/` — 新增 env_cache.json 缓存

</codebase_context>

<specifics>
## Specific Ideas

InputParser 示例：
```python
def detect_input_type(identifier: str) -> str:
    path = Path(identifier)
    if path.exists():
        if path.is_file():
            return "file"  # FileSource
        elif path.is_dir():
            return "folder"  # FolderSource
    # 尝试 Zentao ID 正则
    if re.match(r'^(story|task|bug)-\d+$', identifier):
        return "zentao"  # ZentaoSource
    raise ValueError(f"Cannot detect input type: {identifier}")
```

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 04-pipeline-assembly-and-cli*
*Context gathered: 2026-04-05*

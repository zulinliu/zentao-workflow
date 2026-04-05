# Phase 3: Extended Sources and Testing - Context

**Gathered:** 2026-04-05
**Status:** Ready for planning

<domain>
## Phase Boundary

The tool handles PDF, DOCX, and image files as input sources, and the entire codebase has pytest coverage validating each component. Phase 3 delivers MarkItDown-based readers, full pytest suite, and FolderSource recursive scanning.

</domain>

<decisions>
## Implementation Decisions

### D-01: 库选择 — MarkItDown 统一方案
- **决策:** 使用 MarkItDown 一个库处理 PDF/DOCX/图片文本提取
- **理由:** 接口统一，维护成本低，`pip install markitdown` 即可
- **lazy import:** 可选依赖，不强制安装

### D-02: 测试策略 — 纯单元测试
- **决策:** 使用 pytest + conftest.py fixtures，针对 client/source/exporter/config 独立测试
- **框架:** pytest（已在 pyproject.toml 的 testpaths 配置）
- **Mock 策略:** 使用 unittest.mock 或 pytest-mock，不依赖外部 API 录制

### D-03: 图片处理 — 只复制
- **决策:** 图片只复制到 attachments/ 目录，生成 Markdown 引用
- **理由:** Claude 多模态视觉能力足够，不需要 OCR 或缩略图
- **依赖:** 无需 Pillow

### D-04: 错误处理 — 跳过 + 警告
- **决策:** 不支持的格式打印警告并跳过，不中断处理其他文件
- **理由:** 用户知道有问题但不影响整体流程
- **行为:** `print(f"Warning: unsupported format {ext}, skipping {path}")`

### D-05: 输入类型检测
- **决策:** 输入为文件夹时递归扫描，支持的文件类型: .md, .txt, .pdf, .docx, .png, .jpg, .jpeg, .gif
- **不支持:** 跳过 + 警告

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — INPUT-03, INPUT-04, INPUT-06, INPUT-07, INPUT-08, TEST-01~06 完整需求定义
- `.planning/ROADMAP.md` §Phase 3 — Phase 3 目标、成功标准和依赖关系

### Prior Phase Context
- `.planning/phases/01-foundation-and-rename/01-CONTEXT.md` — Phase 1 决策
- `.planning/phases/02-core-pipeline/02-CONTEXT.md` — Phase 2 决策（D-01 到 D-05）

### Current Codebase
- `scripts/worklet/models.py` — Worklet/RawContent/BaseSource/BaseReader v2.0 模型
- `scripts/worklet/sources/base.py` — SourceRegistry 自动发现机制
- `scripts/worklet/sources/markdown.py` — MarkdownReader 实现参考
- `pyproject.toml` — 项目依赖配置

</canonical_refs>

<codebase_context>
## Existing Code Insights

### Reusable Assets
- `scripts/worklet/sources/markdown.py` — MarkdownReader 实现，BaseReader ABC 子类，可参考结构
- `scripts/worklet/sources/base.py` — SourceRegistry 已被 GAP-01 修复，entry_points 自动发现可用

### Established Patterns
- lazy import 模式: `try: import markitdown; except ImportError: ...`
- Reader 实现: `class XxxReader(BaseReader)` 实现 `can_read()` + `read()` 方法
- Source 注册: entry_points group='worklet.sources' 自动发现

### Integration Points
- `scripts/worklet/sources/` — 新增 PdfReader, DocxReader, ImageReader
- `scripts/worklet/models.py` — BaseReader ABC 已定义，可直接继承

</codebase_context>

<specifics>
## Specific Ideas

MarkItDown 使用示例：
```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("document.pdf")
content = result.text_content  # 返回 Markdown 文本
```

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 03-extended-sources-and-testing*
*Context gathered: 2026-04-05*

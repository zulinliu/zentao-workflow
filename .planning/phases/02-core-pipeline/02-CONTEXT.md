# Phase 2: Core Pipeline - Context

**Gathered:** 2026-04-05
**Status:** Ready for planning

<domain>
## Phase Boundary

End-to-end Zentao + Markdown pipeline with fixed client, new exporter, and source abstractions. Phase 2 delivers a unified Worklet model, BaseSource/ZentaoSource/FileSource pipeline, and all CLIENT fixes (timeout, streaming, exception types, re.findall removal, subtask detection in Python).
</domain>

<decisions>
## Implementation Decisions

### D-01: 统一 Worklet 模型
- **决策:** Exporter 内部兼容 Story/Task/Bug → Worklet 转换
- **理由:** Exporter 保持对外接口不变，SKILL.md 无需修改。内部增加 `_to_worklet()` 方法处理 Story/Task/Bug → Worklet 的转换。
- **转换时机:** Exporter.export_* 方法内部做转换，不改变外部调用方式

### D-02: BaseSource ABC + SourceRegistry
- **BaseSource 抽象:**
  ```python
  class BaseSource(ABC):
      @abstractmethod
      def fetch(self, identifier: str) -> Worklet: ...
  ```
- **SourceRegistry:** 使用 `importlib.metadata` + `entry_points` 自动发现所有 BaseSource 实现，Phase 2 只注册 ZentaoSource
- **注册方式:** 通过 setuptools `entry_points={'worklet.sources': [...]}` 自动发现

### D-03: 子任务检测下沉到 Python
- **决策:** 从 SKILL.md 下沉到 Python 代码（CLIENT-05）
- **实现位置:** service.py 的 `_fetch_by_id()` 或专门的 `_detect_subtasks()` 方法
- **逻辑:** 检测 Story/Task 的 `parent` 字段，递归下载子任务内容
- **时机:** 在 `export_*` 之前执行，结果附加到 Worklet.metadata['subtasks']

### D-04: Exporter 使用 markdownify
- **决策:** HTML→Markdown 转换用 markdownify 库替代现有 40+ 正则链
- **依赖:** `markdownify>=0.18.0`
- **迁移策略:** exporter.py 中新增 `_html_to_markdown_markdownify()` 方法，通过配置开关切换，逐步替换旧正则方法直到稳定

### D-05: Client 修复（全部在 Phase 2 完成）
- **CLIENT-01:** download_attachment/download_image 添加 timeout 参数
- **CLIENT-02:** 大文件流式下载（stream=True + 原子写入 .tmp → rename）
- **CLIENT-03:** 通用 Exception 替换为具体异常类型（ConnectionError/TimeoutError/ValueError）
- **CLIENT-04:** service.py 移除无用 re.findall() 调用（第 126 行）

### Claude's Discretion
- InputParser 的具体实现路径（硬编码 vs 配置文件驱动）
- SourceRegistry 的 fallback 策略（当 entry_points 不可用时的备选）
- markdownify 配置选项（允许哪些 HTML 标签，如何处理图片路径）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — INPUT-01, INPUT-02, INPUT-05, CLIENT-01~05, EXPORT-01~03 完整需求定义
- `.planning/ROADMAP.md` §Phase 2 — Phase 2 目标、成功标准和依赖关系

### Prior Phase Context
- `.planning/phases/01-foundation-and-rename/01-CONTEXT.md` — Phase 1 决策（D-01 到 D-08）

### Codebase Analysis
- `.planning/codebase/STRUCTURE.md` — 当前目录结构和模块依赖图（注意：仍引用 chandao_fetch，已过时）
- `.planning/codebase/CONVENTIONS.md` — 命名规范、代码风格
- `.planning/codebase/STACK.md` — 技术栈和依赖清单（需更新：移除 Java 相关）

### Current Codebase
- `scripts/worklet/models.py` — 包含 Phase 1 重命名后的 Story/Task/Bug/Attachment + v2.0 占位模型
- `scripts/worklet/client.py` — 当前 client.py（需修复 timeout、streaming、异常类型）
- `scripts/worklet/service.py` — 当前 service.py（需移除 re.findall、下沉子任务检测）
- `scripts/worklet/exporter.py` — 当前 exporter.py（需引入 markdownify）
- `scripts/worklet/__init__.py` — 包入口，版本 2.0.0

### Configuration Template
- `assets/config_template.toml` — Phase 1 新建的 TOML 配置模板（Phase 2 需确认无需修改）

</canonical_refs>

<codebase_context>
## Existing Code Insights

### Reusable Assets
- `scripts/worklet/models.py` — Story/Task/Bug/Attachment dataclass（Phase 1 重命名后），Worklet/RawContent/BaseSource/BaseReader v2.0 占位
- `scripts/worklet/client.py` — 现有 API 逻辑基本可用，只需加 timeout 和异常类型
- `scripts/worklet/exporter.py` — MarkdownExporter 框架可用，_process_content/_html_to_markdown 需重写

### Established Patterns
- Python 模块内使用相对导入（`from .config import WorkletConfig`）
- 配置优先级链：命令行 > 工作区 > 全局 > 默认值 → 保持不变
- 安全约束：API 客户端只读 → 保持不变

### Integration Points
- `SKILL.md` — Phase 1 已更新引用 worklet.py，但调用参数和执行流程基本不变
- `pyproject.toml` — Phase 1 已创建，Phase 2 需添加 markdownify 依赖
- `scripts/worklet/models.py` — v2.0 Worklet 模型已定义占位符，Phase 2 实现具体逻辑

</codebase_context>

<specifics>
## Specific Ideas

- markdownify 配置示例：
  ```python
  from markdownify import MarkdownConverter
  class WorkletConverter(MarkdownConverter):
      def convert_img(self, node):
          return f'![]({node['src']})'
  ```
- 子任务检测逻辑位置：service.py 的 `_fetch_by_id()` 末尾，判断 `story.parent` 或 `task.parent` 是否存在，存在则递归

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-core-pipeline*
*Context gathered: 2026-04-05*

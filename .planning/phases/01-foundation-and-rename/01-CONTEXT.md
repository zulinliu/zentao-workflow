# Phase 1: Foundation and Rename - Context

**Gathered:** 2026-04-04
**Status:** Ready for planning

<domain>
## Phase Boundary

将整个项目从 chandao/zentao 重命名为 worklet，删除 Java 版本，建立新数据模型占位和配置结构。Phase 1 完成后，代码库中不应有任何 chandao/zentao 命名残留，Java 产物全部清除，新的 Worklet 数据模型和 TOML 配置结构已就位。

</domain>

<decisions>
## Implementation Decisions

### D-01: 包目录结构
- **决策:** 保持 `scripts/` 层级，从 `scripts/chandao_fetch/` 重命名为 `scripts/worklet/`
- **理由:** 对现有 SKILL.md 执行流程和 release 打包逻辑影响最小
- **具体结构:**
  ```
  scripts/
  ├── worklet.py          # wrapper 入口（从 chandao_fetch.py 重命名）
  ├── worklet/             # Python 包（从 chandao_fetch/ 重命名）
  │   ├── __init__.py
  │   ├── __main__.py
  │   ├── config.py
  │   ├── client.py
  │   ├── models.py
  │   ├── service.py
  │   └── exporter.py
  └── requirements.txt
  ```

### D-02: pyproject.toml 位置
- **决策:** 放在项目根目录，通过 `[tool.setuptools.packages.find] where = ["scripts"]` 指向包
- **构建后端:** setuptools（`requires = ["setuptools>=68.0"]`）

### D-03: 数据模型策略 — 粗粒度占位 + 新旧共存
- **新模型（占位）:** Worklet、RawContent、Attachment dataclass + BaseSource/BaseReader ABC
  ```python
  @dataclass
  class Worklet:
      id: str
      title: str
      content: str          # markdown
      source_type: str      # 'zentao', 'file', 'folder'
      attachments: list[Attachment]
      metadata: dict        # source-specific fields

  @dataclass
  class RawContent:
      raw: str              # original content
      format: str           # 'html', 'markdown', 'text'

  @dataclass
  class Attachment:
      id: str
      title: str
      path: Path | None = None

  class BaseSource(ABC):
      @abstractmethod
      def fetch(self, identifier: str) -> Worklet: ...

  class BaseReader(ABC):
      @abstractmethod
      def read(self, path: Path) -> RawContent: ...
  ```
- **旧模型:** Story/Task/Bug 只做重命名（ChandaoXxx → 无前缀），保留原有字段，与新模型共存
- **迁移时机:** Phase 2 实现流水线时做合并

### D-04: 配置文件格式 — TOML
- **决策:** 从 Java Properties 迁移到 TOML 格式
- **文件名:** `.worklet/config.toml`
- **解析库:** tomli（读）+ tomli-w（写），作为 dependencies 声明
- **结构:**
  ```toml
  [zentao]
  url = "https://server.com"
  username = "user"
  password = "pass"

  [output]
  dir = ".worklet/"

  [network]
  connect_timeout = 30
  read_timeout = 60
  ```

### D-05: Python 版本和语法
- **版本要求:** Python >= 3.10
- **语法策略:** 充分利用 3.10+ 新特性
  - `X | Y` union types（替代 `Optional[T]` 和 `Union[X, Y]`）
  - `match/case` 语句（适合 content type 分发等场景）
  - 内置泛型 `list[T]`、`dict[K, V]`（不需要 `from typing import List, Dict`）

### D-06: 下载输出目录结构
- **决策:** 统一在 `.worklet/` 下，配置和输出共存
- **结构:**
  ```
  .worklet/
  ├── config.toml        # 配置文件
  ├── story/             # 需求 Markdown
  ├── task/              # 任务 Markdown
  ├── bug/               # Bug Markdown
  ├── files/             # 本地文件输入副本
  └── attachments/       # 所有附件
      ├── story/{id}/
      ├── task/{id}/
      └── bug/{id}/
  ```

### D-07: CLI 调用风格
- **决策:** 保持旧 `-t/-i` 风格，保留 `scripts/worklet.py` wrapper
- **调用方式:**
  ```bash
  python3 worklet.py -t story -i 39382
  python3 worklet.py -t bug --ids 66445,66446
  # Phase 3+ 新增:
  python3 worklet.py -f /path/to/req.md
  python3 worklet.py -d /path/to/folder/
  ```

### D-08: Java 删除范围
- 删除 `scripts/chandao-fetch.jar`
- 删除 `scripts/java-src/` 整个目录
- 清除 SKILL.md、README.md、CLAUDE.md 中所有 Java 相关引用
- 清理 `.claude/settings.local.json` 中旧的 Java 复制权限规则

### Claude's Discretion
- Java 删除的具体 git 操作顺序（先删文件还是先改引用）
- `.gitignore` 中 `.worklet/` 的具体 pattern 写法
- `__pycache__/` 清理策略
- requirements.txt 是否保留（pyproject.toml 已声明依赖，但 SKILL.md 执行时可能直接 pip install -r）
- references/ 目录内容是否需要调整

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — FOUND-01 到 FOUND-16 + DOC-03 的完整需求定义
- `.planning/ROADMAP.md` §Phase 1 — Phase 1 目标、成功标准和依赖关系

### Codebase Analysis
- `.planning/codebase/STRUCTURE.md` — 当前目录结构和模块依赖图
- `.planning/codebase/CONVENTIONS.md` — 命名规范、代码风格、配置管理模式
- `.planning/codebase/STACK.md` — 技术栈和依赖清单

### Configuration Template
- `assets/config_template.properties` — 当前配置模板（需迁移为 TOML 格式）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/chandao_fetch/config.py` — ChandaoConfig 类，需重构为 WorkletConfig + TOML 解析
- `scripts/chandao_fetch/models.py` — Story/Task/Bug/Attachment dataclass，重命名后可作为旧模型保留
- `scripts/chandao_fetch/__main__.py` — CLI argparse 逻辑，重命名后基本可复用

### Established Patterns
- Python 模块内使用相对导入（`from .config import ChandaoConfig`）→ 重命名时需全量替换
- 配置优先级链：命令行 > 工作区 > 全局 > 默认值 → 保持不变，只改路径和格式
- 安全约束：API 客户端只读 → 保持不变

### Integration Points
- `SKILL.md` — 引用 `scripts/chandao_fetch.py` 和 `scripts/chandao-fetch.jar`，需更新路径
- `.github/workflows/release.yml` — 引用 Java 相关路径，需清理
- `.claude/settings.local.json` — 可能有 Java JAR 复制的权限规则

</code_context>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-foundation-and-rename*
*Context gathered: 2026-04-04*

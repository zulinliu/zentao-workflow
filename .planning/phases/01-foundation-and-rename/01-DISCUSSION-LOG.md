# Phase 1: Foundation and Rename - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-04
**Phase:** 01-foundation-and-rename
**Areas discussed:** 包目录结构, 数据模型设计, 配置键名和格式, 构建和打包方式, 下载输出目录结构, 入口文件和调用方式

---

## 包目录结构

### Q1: 重命名后的 Python 包应该放在哪里？

| Option | Description | Selected |
|--------|-------------|----------|
| scripts/worklet/ (推荐) | 保持原来的 scripts/ 层级，对 SKILL.md 和 release 打包影响最小 | ✓ |
| src/worklet/ | 提升到项目根目录，更标准化，但需较大调整 | |
| worklet/（根目录） | 最简洁，但会和文档文件混在一起 | |

**User's choice:** scripts/worklet/ (推荐)
**Notes:** 无额外说明

### Q2: pyproject.toml 放在哪里？

| Option | Description | Selected |
|--------|-------------|----------|
| 项目根目录（推荐） | 符合 PEP 621 标准，需额外 package-dir 配置 | ✓ |
| scripts/ 目录下 | 与包同级，更紧凑但不太常规 | |

**User's choice:** 项目根目录（推荐）
**Notes:** 无额外说明

### Q3: scripts/worklet.py wrapper 入口脚本是否保留？

| Option | Description | Selected |
|--------|-------------|----------|
| 保留 wrapper（推荐） | 保留 scripts/worklet.py，SKILL.md 用 python3 worklet.py 调用 | ✓ |
| 去掉，用 -m 调用 | 更干净，但 SKILL.md 需要先 cd scripts/ | |

**User's choice:** 保留 wrapper（推荐）
**Notes:** 无额外说明

---

## 数据模型设计

### Q4: 新数据模型做到什么程度？

| Option | Description | Selected |
|--------|-------------|----------|
| 粗粒度占位（推荐） | 定义类名、核心字段、ABC 接口签名，具体实现留到 Phase 2 | ✓ |
| 完整定义 | Phase 1 就把所有字段、方法、辅助函数定义好 | |
| Claude 决定 | 信任下游代理来设计 | |

**User's choice:** 粗粒度占位（推荐）
**Notes:** 无额外说明

### Q5: 旧模型和新模型如何共存？

| Option | Description | Selected |
|--------|-------------|----------|
| 保留旧模型 + 重命名 | 只重命名，Phase 2 再迁移合并 | |
| 合并到新模型 | Phase 1 就一步到位 | |
| 共存（推荐） | 旧模型只重命名，新模型以占位形式共存 | ✓ |

**User's choice:** 共存（推荐）
**Notes:** 无额外说明

---

## 配置键名和格式

### Q6: 配置文件格式怎么选？

| Option | Description | Selected |
|--------|-------------|----------|
| Properties + 改前缀 | 保持 Java Properties 格式，只改键名前缀 | |
| TOML 格式（推荐） | 迁移到 TOML，结构更清晰，支持嵌套 | ✓ |

**User's choice:** TOML 格式（推荐）
**Notes:** 无额外说明

### Q7: TOML 解析库怎么选？

| Option | Description | Selected |
|--------|-------------|----------|
| tomli + tomli-w（推荐） | 3.10 兼容，3.11+ 可切换内置 tomllib | ✓ |
| 只用 tomllib（3.11+） | 无额外依赖但版本要求更高 | |

**User's choice:** tomli + tomli-w（推荐）
**Notes:** 无额外说明

---

## 构建和打包方式

### Q8: pyproject.toml 用什么构建后端？

| Option | Description | Selected |
|--------|-------------|----------|
| setuptools（推荐） | 最成熟稳定，生态最广 | ✓ |
| hatchling | 更现代，内置环境管理 | |
| poetry | 强大但重，对轻量级工具过度 | |

**User's choice:** setuptools（推荐）
**Notes:** 无额外说明

### Q9: Python 3.10+ 新语法特性怎么用？

| Option | Description | Selected |
|--------|-------------|----------|
| 充分利用新语法（推荐） | X | Y unions、match/case、内置泛型 | ✓ |
| 保守风格 | 只用 Optional[T] 和 typing 模块 | |

**User's choice:** 充分利用新语法（推荐）
**Notes:** 无额外说明

---

## 下载输出目录结构

### Q10: .worklet/ 目录内部结构怎么组织？

| Option | Description | Selected |
|--------|-------------|----------|
| 统一在 .worklet/ 下（推荐） | 配置和输出共存，按类型分子目录 | ✓ |
| 配置和输出分开 | 配置在 .worklet/，输出在用户指定目录 | |

**User's choice:** 统一在 .worklet/ 下（推荐）
**Notes:** 无额外说明

---

## 入口文件和调用方式

### Q11: CLI 调用风格怎么定？

| Option | Description | Selected |
|--------|-------------|----------|
| 保持旧 CLI 风格（推荐） | -t/-i 参数风格，Phase 3+ 扩展 -f/-d | ✓ |
| 子命令风格 | worklet fetch story 39382 / worklet read file.md | |

**User's choice:** 保持旧 CLI 风格（推荐）
**Notes:** 无额外说明

---

## Claude's Discretion

- Java 删除的 git 操作顺序
- .gitignore 中 .worklet/ 的具体 pattern 写法
- __pycache__/ 清理策略
- requirements.txt 是否保留
- references/ 目录内容是否需要调整

## Deferred Ideas

None — discussion stayed within phase scope

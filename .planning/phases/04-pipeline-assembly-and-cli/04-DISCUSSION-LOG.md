# Phase 4: Pipeline Assembly and CLI - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-05
**Phase:** 04-pipeline-assembly-and-cli
**Areas discussed:** 输入类型自动检测, 环境缓存策略, superpowers 安装, Java 检测清理

---

## 输入类型自动检测

| Option | Description | Selected |
|--------|-------------|----------|
| 路径+扩展名检测 | 先检查存在性 → 文件/文件夹 → 扩展名检测 → Zentao ID 正则 | ✓ |
| try-first 策略 | 先尝试 Zentao API → 失败则文件 → 再失败则文件夹 | |
| 混合策略 | Path.exists() → 扩展名检测 → Zentao ID 正则 | |

**User's choice:** 路径+扩展名检测
**Notes:** 最清晰，最少副作用

---

## 环境缓存策略

| Option | Description | Selected |
|--------|-------------|----------|
| .worklet/ 缓存文件 | .worklet/env_cache.json 带 24h TTL | ✓ |
| 不缓存 | 每次启动都检测 | |

**User's choice:** .worklet/ 缓存文件
**Notes:** 带 24h TTL

---

## superpowers 安装

| Option | Description | Selected |
|--------|-------------|----------|
| npx 安装 | which npx && npx superpowers --version | ✓ |
| plugins add | claude plugins add official superpowers | |
| pip 安装 | pip install superpowers | |

**User's choice:** npx 安装
**Notes:** 无全局安装、版本可控

---

## Java 检测清理

**User's choice:** 移除所有 Java 环境检测代码
**Notes:** Phase 1 已删除 Java 版本，Phase 4 清理残留检测代码

---

## Deferred Ideas

无


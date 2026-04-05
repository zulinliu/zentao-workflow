# Phase 3: Extended Sources and Testing - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-05
**Phase:** 03-extended-sources-and-testing
**Areas discussed:** 库选择策略, 测试策略, 图片处理范围, 错误处理

---

## 库选择策略

| Option | Description | Selected |
|--------|-------------|----------|
| MarkItDown 统一 | 一个库搞定 PDF/DOCX/图片文本提取，接口统一 | ✓ |
| 分库 + lazy import | pypdf + python-docx，按需加载，依赖更少但代码更分散 | |
| 混用方案 | pypdf + python-docx + Pillow，Phase 2 已引入 markdownify | |

**User's choice:** MarkItDown 统一
**Notes:** MarkItDown 一个库搞定所有格式，维护成本低

---

## 测试策略

| Option | Description | Selected |
|--------|-------------|----------|
| 纯单元测试 | pytest + conftest.py fixtures，针对 client/source/exporter/config 独立测试 | ✓ |
| Mock + 录制 | vcrpy 录制真实 API 响应，replay 模式 | |
| pytest-mock | 测试夹具 + pytest-mock，fixture 管理 mock 对象 | |

**User's choice:** 纯单元测试
**Notes:** Phase 2 已验证的策略，pytest 框架

---

## 图片处理范围

| Option | Description | Selected |
|--------|-------------|----------|
| 只复制 | 只复制图片到 attachments/ 目录，生成 Markdown 引用 | ✓ |
| 生成缩略图 | 复制 + 生成缩略图，节省 Claude 视觉 token | |
| 缩略图+Pillow | Pillow 生成缩略图，减小视觉处理体积 | |

**User's choice:** 只复制
**Notes:** Claude 多模态已足够，Pillow 增加额外依赖

---

## 错误处理

| Option | Description | Selected |
|--------|-------------|----------|
| 跳过 + 警告 | 跳过不支持的格式，打印警告继续处理其他文件 | ✓ |
| 静默跳过 | 跳过不支持的格式，静默处理其他文件 | |
| 直接报错 | 遇到不支持的格式立即抛出异常 | |

**User's choice:** 跳过 + 警告
**Notes:** 用户知道有问题但不中断流程

---

## Claude's Discretion

无 — 所有决策均已由用户明确选择

---

## Deferred Ideas

无


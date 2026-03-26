# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-03-26

### Added
- GitHub Actions 自动发版工作流
- 发布包包含 `zentao-workflow/` 目录层，解压即用
- 项目管理和发版规范文档

### Fixed
- 修复 HTML 转 Markdown 问题，支持完整标签转换（h1-h6、p、ul、ol、li、strong、em、code、a 等）
- 修复禅道配置初始化流程，一次性主动收集所有配置信息
- 处理 HTML 实体（&nbsp;、&lt;、&gt; 等）

## [1.0.0] - 2025-03-26

### Added

- Initial release of zentao-workflow skill
- 双运行时支持（Java 8+ 和 Python 3.6+）
- 自动环境检测和运行时选择
- 交互式禅道服务器配置
- 下载需求/任务/Bug 及附件
- 下载内容中嵌入的图片
- 生成开发技术方案文档
- 跨平台支持（Windows、macOS、Linux）
- Java 项目分析指南
- React 项目分析指南
- 技术方案模板

### Features

- **智能触发**: 当提到"禅道"、"需求"、"任务"、"Bug"等关键词时自动激活
- **双运行时**: 内置 Java 和 Python 版本，自动选择最佳运行时（Java > Python）
- **附件下载**: 下载所有附件和嵌入图片
- **技术方案**: 基于项目代码分析生成详细开发方案
- **跨平台**: 支持 Windows、macOS、Linux

### Technical Details

- Java 版本: Maven 构建，需要 Java 8+
- Python 版本: 纯 Python + requests 库
- Markdown 导出，附件使用相对路径: `../attachments/{type}/{id}/`

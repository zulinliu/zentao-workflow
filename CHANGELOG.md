# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] - 2025-03-26

### Added
- **方案质量自动评审**（可选功能）：
  - 架构方案完成后可选择启动3个评审代理进行自动评审
  - 编码方案完成后可选择启动3个评审代理进行自动评审
  - 评审角度：完整性检查、可行性检查、一致性/覆盖性检查
  - 支持根据评审建议自动优化方案
  - 生成评审报告文档

### Changed
- **子代理数量优化**：
  - 架构方案快速模式：3个并行代理（原1个）
  - 架构方案深度模式：6个并行代理（原3个）
  - 编码方案快速模式：3个并行代理
  - 编码方案深度模式：5个并行代理
- **代理任务细化**：每个代理有明确的分析任务，避免重复工作

## [1.3.0] - 2025-03-26

### Added
- **多项目配置支持**：
  - 配置文件优先级：工作区配置 > 全局配置
  - 存储目录动态确定，不再持久化到配置文件
  - 支持多项目并行开发，每个项目独立存储禅道内容

## [1.2.0] - 2025-03-26

### Added
- **快速/深度模式选择**：
  - 架构方案设计支持快速模式（1个代理，2-3分钟）和深度模式（3个并行代理，5-15分钟）
  - 编码方案设计支持快速模式（核心步骤）和深度模式（详细伪代码和测试计划）
- **进度提示**：在方案设计过程中定期输出进度提示，提升用户体验
- **子代理并行优化**：深度模式使用3个并行探索代理分析业务代码、实现模式、数据模型

### Changed
- **方案命名优化**：
  - "技术方案" 重命名为 "架构方案"
  - "设计方案" 重命名为 "编码方案"
- 简化方案文档结构，聚焦核心内容

## [1.1.3] - 2025-03-26

### Fixed
- **用户交互一致性**：
  - 配置已存在时也会询问确认存储目录
  - 下载完成后必须使用 AskUserQuestion 询问用户是否开始设计
  - 禁止下载完成后直接进入 Plan 模式

## [1.1.2] - 2025-03-26

### Fixed
- 修正 SKILL.md 中 Python 脚本路径为 `scripts/chandao_fetch.py`
- 添加 Windows/Linux/macOS 跨平台路径处理说明
- 强调使用双引号包裹路径避免空格问题

## [1.1.1] - 2025-03-26

### Fixed
- 修复 Windows 上 Java 日志中文乱码问题
  - 更新 logback.xml 添加 UTF-8 编码
  - Java 命令添加 `-Dfile.encoding=UTF-8` 参数

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

# Zentao Workflow Skill

[![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)](https://github.com/zulinliu/zentao-workflow)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-purple.svg)](https://claude.ai/code)
[![Release](https://img.shields.io/github/release/zulinliu/zentao-workflow.svg)](https://github.com/zulinliu/zentao-workflow/releases)

禅道开发工作流助手 - 自动化禅道需求/任务/Bug 下载与开发方案设计。

## 快速安装

### 推荐方式：从 Releases 下载

前往 [Releases 页面](https://github.com/zulinliu/zentao-workflow/releases) 下载最新版本的 `zentao-workflow-vx.x.x.zip`。

```bash
# Linux/macOS
cd ~/.claude/skills
unzip ~/Downloads/zentao-workflow-v1.4.0.zip -d zentao-workflow

# Windows PowerShell
cd $env:USERPROFILE\.claude\skills
Expand-Archive $env:USERPROFILE\Downloads\zentao-workflow-v1.4.0.zip -DestinationPath zentao-workflow
```

重启 Claude Code 即可使用。

### 其他方式

<details>
<summary>方法二：从 GitHub 克隆</summary>

```bash
git clone https://github.com/zulinliu/zentao-workflow.git
cp -r zentao-workflow ~/.claude/skills/
```

</details>

<details>
<summary>方法三：手动复制</summary>

将整个项目目录复制到 Claude Code 技能目录：
- Linux/macOS: `~/.claude/skills/`
- Windows: `%USERPROFILE%\.claude\skills\`

</details>

## 环境要求

只需满足以下**任一**环境：

| 运行时 | 版本要求 | 优先级 |
|--------|----------|--------|
| Java | 8+ | 高（优先使用） |
| Python | 3.6+ | 中（默认备选） |

## 功能特性

### 核心功能
- **智能触发** - 支持多种触发格式（`禅道需求39382`、`开发需求39382`、`39382需求` 等）
- **双运行时支持** - 内置 Java 和 Python 两个版本，自动选择最佳运行时
- **跨平台兼容** - 支持 Windows、macOS、Linux
- **交互式配置** - 引导用户完成禅道服务器配置
- **附件完整下载** - 下载所有附件和内容中嵌入的图片

### v1.4.0 新增功能
- **方案质量自动评审**（可选）
  - 架构方案/编码方案完成后可启动 3 个评审代理
  - 评审角度：完整性检查、可行性检查、一致性检查
  - 支持根据评审建议自动优化方案
- **快速/深度模式选择**
  - 快速模式：2-3 分钟完成，适合简单需求
  - 深度模式：5-15 分钟完成，适合复杂需求
- **多项目配置支持**
  - 工作区配置优先，支持多项目并行开发

## 快速开始

```
你: 帮我开发禅道需求 39382

Claude: [触发 zentao-workflow 技能]
        检测运行环境...
        ✓ Java 1.8.0 已检测到，使用 Java 版本

        首次使用需要配置禅道信息...
        ✓ 配置已完成

        正在下载需求 39382...
        ✓ 下载完成
          - MD 文件: story/39382-需求标题.md
          - 附件: 3 个文件已下载
          - 图片: 2 张图片已下载

        是否开始设计架构方案？

        [用户选择：是，开始设计]

        请选择设计模式：
        1. 快速模式（推荐）- 2-3分钟完成
        2. 深度模式 - 5-15分钟完成

        [用户选择：快速模式]

        🚀 启动快速模式架构分析...
        [✓] 阶段 1/4: 阅读禅道需求内容
        [✓] 阶段 2/4: 查看附件和图片
        [✓] 阶段 3/4: 探索项目代码
        [✓] 阶段 4/4: 编写架构方案

        ✓ 架构方案已完成
          文件: story_39382_架构方案.md

        是否启动自动评审检查方案质量？
```

### 支持的输入格式

| 格式 | 示例 |
|------|------|
| 类型+ID | 需求39382、任务12345、Bug67890 |
| ID+类型 | 39382需求、12345任务、67890Bug |
| 前缀+类型+ID | 禅道需求39382、开发任务12345 |
| 纯 ID | 39382 |
| URL | https://zentao.example.com/story-view-39382.html |

### 触发关键词

- 禅道、zentao、chandao
- 需求、开发需求、story
- 任务、task
- Bug、缺陷
- 下载禅道、获取需求

## 方案设计流程

### 1. 架构方案设计

| 模式 | 耗时 | 代理数 | 输出内容 |
|------|------|--------|----------|
| 快速模式 | 2-3分钟 | 3个并行 | 核心架构设计、接口设计 |
| 深度模式 | 5-15分钟 | 6个并行 | 完整架构分析、风险评估 |

**包含内容**：
- 需求分析 - 需求背景、功能点拆解、验收标准
- 技术设计 - 技术选型、架构设计、接口设计
- 影响范围 - 涉及的模块和文件

### 2. 编码方案设计

| 模式 | 耗时 | 代理数 | 输出内容 |
|------|------|--------|----------|
| 快速模式 | 2-3分钟 | 3个并行 | 核心实现步骤、关键代码位置 |
| 深度模式 | 5-10分钟 | 5个并行 | 详细步骤、伪代码、测试计划 |

**包含内容**：
- 实现步骤 - 详细的分步骤实现
- 代码定位 - 需要修改的文件和位置
- 测试计划 - 单元测试、集成测试设计

### 3. 方案质量评审（可选）

启动 3 个评审代理并行检查：
1. **完整性检查** - 功能点覆盖、验收标准可验证性
2. **可行性检查** - 技术选型合理性、风险识别
3. **一致性检查** - 架构风格一致性、无破坏性改动

## 输出文件结构

```
{workspace}/
├── .chandao/
│   └── config.properties          # 工作区配置（可选）
├── story_39382_架构方案.md        # 架构方案文档
├── story_39382_架构方案_评审.md   # 架构方案评审报告（如有）
├── story_39382_编码方案.md        # 编码方案文档
├── story_39382_编码方案_评审.md   # 编码方案评审报告（如有）
├── story/                         # 需求 Markdown 文件
│   └── 39382-需求标题.md
├── task/                          # 任务 Markdown 文件
│   └── 12345-任务名称.md
├── bug/                           # Bug Markdown 文件
│   └── 67890-Bug标题.md
└── attachments/                   # 附件目录
    ├── story/39382/
    ├── task/12345/
    └── bug/67890/
```

## 常见问题

### Q: 没有安装 Java 或 Python 怎么办？

技能会自动检测并提示安装。默认推荐安装 Python（更轻量）。

### Q: 如何配置多项目支持？

每个工作区可以有自己的 `.chandao/config.properties` 文件，优先级高于全局配置。

### Q: 下载失败怎么办？

常见原因：
1. 网络无法访问禅道服务器
2. 用户名或密码错误
3. ID 不存在或无权限访问

## 版本历史

| 版本 | 主要更新 |
|------|----------|
| 1.4.0 | 方案质量自动评审、子代理数量优化 |
| 1.3.0 | 多项目配置支持 |
| 1.2.0 | 快速/深度模式选择、进度提示 |
| 1.1.x | 交互优化、跨平台兼容性修复 |
| 1.0.0 | 初始版本 |

查看 [CHANGELOG.md](CHANGELOG.md) 获取详细更新记录。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 作者

- **liuzl** - [GitHub](https://github.com/zulinliu)

---

**版本**: 1.4.0 | **作者**: liuzl | **许可证**: MIT

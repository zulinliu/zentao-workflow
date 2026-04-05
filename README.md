# Worklet - 开发工作流助手

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/zulinliu/worklet)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-purple.svg)](https://claude.ai/code)
[![Release](https://img.shields.io/github/release/zulinliu/worklet.svg)](https://github.com/zulinliu/worklet/releases)

Worklet (Workflow + Applet) 是一个 Claude Code Skill，为开发者提供轻量级的开发工作流自动化。它从多种来源（禅道 API、本地文件/文件夹）获取需求/任务/Bug 文档，结合项目代码自动生成技术实现方案，并驱动编码执行。v2.0.0 从"禅道专用工具"升级为"通用开发工作流助手"。

## 快速安装

### 推荐方式：从 Releases 下载

前往 [Releases 页面](https://github.com/zulinliu/worklet/releases) 下载最新版本的 `worklet-v2.0.0.zip`。

```bash
# Linux/macOS
cd ~/.claude/skills
unzip ~/Downloads/worklet-v2.0.0.zip -d worklet

# Windows PowerShell
cd $env:USERPROFILE\.claude\skills
Expand-Archive $env:USERPROFILE\Downloads\worklet-v2.0.0.zip -DestinationPath worklet
```

重启 Claude Code 即可使用。

### 其他方式

<details>
<summary>方法二：从 GitHub 克隆</summary>

```bash
git clone https://github.com/zulinliu/worklet.git
cp -r worklet ~/.claude/skills/
```

</details>

<details>
<summary>方法三：手动复制</summary>

将整个项目目录复制到 Claude Code 技能目录：
- Linux/macOS: `~/.claude/skills/`
- Windows: `%USERPROFILE%\.claude\skills\`

</details>

## 环境要求

### 运行时

| 运行时 | 版本要求 |
|--------|----------|
| Python | 3.10+ |

### 技能依赖

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| superpowers 插件 | 5.0.6+ | 技术方案设计必需，如未安装会提示自动安装 |

## 功能特性

- **多源需求入口** - 支持禅道 API 和本地文件/文件夹（Markdown/PDF/Word/图片）
- **智能自动检测** - InputParser 自动识别输入类型并选择最佳处理方式
- **跨平台兼容** - 支持 Windows、macOS、Linux
- **环境缓存** - 24小时 TTL 缓存避免重复检测
- **交互式配置** - 引导用户完成服务器配置
- **附件完整下载** - 下载所有附件和内容中嵌入的图片
- **技术方案生成** - 结合项目代码自动生成可执行的技术实现方案

### v2.0.0 重大更新

- **通用开发工作流** - 从"禅道专用工具"升级为"通用开发工作流助手"
- **多源输入支持** - 禅道 API + 本地文件/文件夹
- **Python only** - 移除 Java 运行时依赖，体积更小
- **环境缓存优化** - 24h TTL 缓存提升性能

<details>
<summary>v1.x 历史功能</summary>

### v1.5.0 功能
- **集成 superpowers 技能链** - 技术方案设计效率提升 70%+
- **合并架构方案和编码方案**

### v1.4.x 功能
- **方案质量自动评审**（可选）
- **快速/深度模式选择**
- **多项目配置支持**

</details>

## 快速开始

```
你: 帮我处理一个开发需求

Claude: [触发 worklet 技能]
        检测运行环境...
        ✓ Python 3.10+ 已检测到

        请选择需求来源：
        1. 禅道 API（需要配置禅道服务器）
        2. 本地文件/文件夹

        首次使用需要配置信息...
        ✓ 配置已完成

        正在处理需求...
        ✓ 处理完成

        是否开始设计开发技术方案？
```

### 支持的输入格式

**禅道 API 模式：**

| 格式 | 示例 |
|------|------|
| 纯 ID | 38817 |
| URL | https://zentao.example.com/story-view-38817.html |
| 关键词+ID | 开发需求38817、任务12345 |

**本地文件模式：**

| 格式 | 示例 |
|------|------|
| 单文件 | ./requirements.md |
| 文件夹 | ./docs/requirements/ |
| 混合 | ./需求.md + ./附件/ |

### 触发关键词

- 开发需求、优化功能、修复bug、重构、开发、优化
- 需求、任务、Bug（禅道场景）
- 本地文件处理（.md/.pdf/.docx/.jpg/.png）

## 技术实现方案设计

v1.5.0+ 使用 `superpowers:brainstorming` 技能，一次完成所有设计工作。

**技术实现方案包含**：
1. **需求分析** - 背景、功能点拆解、验收标准
2. **架构设计** - 技术选型、模块设计、接口设计
3. **实现步骤** - 详细编码步骤（5-10 步）

**执行方式选择**：
- **子代理驱动**（推荐）- 使用 `superpowers:subagent-driven-development`
- **内联执行** - 使用 `superpowers:executing-plans`
- **手动执行** - 保留方案，手动实现

## 输出文件结构

```
{workspace}/
├── .worklet/
│   └── config.toml                # 工作区配置（可选）
├── story_39382_技术实现方案.md    # 技术实现方案文档
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

### Q: 没有安装 Python 怎么办？

技能会自动检测并提示安装。

### Q: 如何修改已保存的配置？

编辑 `~/.worklet/config.toml` 文件（项目根目录优先）。

### Q: 支持哪些本地文件格式？

支持的格式：
- Markdown (.md, .txt)
- Word (.docx)
- PDF (.pdf)
- 图片 (.jpg, .jpeg, .png, .gif)

## 版本历史

| 版本 | 主要更新 |
|------|----------|
| 2.0.0 | 从禅道专用工具升级为通用开发工作流、多源输入支持、Python only |
| 1.6.0 | 子任务检测与关联内容下载逻辑 |
| 1.5.0 | 集成 superpowers 技能链、合并架构/编码方案、效率提升 70%+ |
| 1.4.x | 方案质量自动评审、快速/深度模式选择、多项目配置支持 |
| 1.0.0 | 初始版本 |

查看 [CHANGELOG.md](CHANGELOG.md) 获取详细更新记录。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 作者

- **liuzl** - [GitHub](https://github.com/zulinliu)

---

**版本**: 2.0.0 | **作者**: liuzl | **许可证**: MIT

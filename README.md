# Zentao Workflow Skill

[![Version](https://img.shields.io/badge/version-1.6.0-blue.svg)](https://github.com/zulinliu/zentao-workflow)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-purple.svg)](https://claude.ai/code)
[![Release](https://img.shields.io/github/release/zulinliu/zentao-workflow.svg)](https://github.com/zulinliu/zentao-workflow/releases)

禅道开发工作流助手 - 自动化禅道需求/任务/Bug 下载与技术实现方案设计。

## 快速安装

### 推荐方式：从 Releases 下载

前往 [Releases 页面](https://github.com/zulinliu/zentao-workflow/releases) 下载最新版本的 `zentao-workflow-vx.x.x.zip`。

```bash
# Linux/macOS
cd ~/.claude/skills
unzip ~/Downloads/zentao-workflow-v1.6.0.zip -d zentao-workflow

# Windows PowerShell
cd $env:USERPROFILE\.claude\skills
Expand-Archive $env:USERPROFILE\Downloads\zentao-workflow-v1.6.0.zip -DestinationPath zentao-workflow
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

### 运行时（满足任一即可）

| 运行时 | 版本要求 | 优先级 |
|--------|----------|--------|
| Java | 8+ | 高（优先使用） |
| Python | 3.6+ | 中（默认备选） |

### 技能依赖（v1.5.0 新增）

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| superpowers 插件 | 5.0.6+ | 技术方案设计必需，如未安装会提示自动安装 |

## 功能特性

- **智能触发** - 当提到"禅道"、"需求"、"任务"、"Bug"等关键词时自动激活
- **双运行时支持** - 内置 Java 和 Python 两个版本，自动选择最佳运行时
- **跨平台兼容** - 支持 Windows、macOS、Linux
- **自动环境配置** - 无环境时可自动安装 Python
- **交互式配置** - 引导用户完成禅道服务器配置
- **附件完整下载** - 下载所有附件和内容中嵌入的图片

### v1.6.0 重大更新

- **子任务检测与关联内容下载**
  - 新增子任务检测逻辑，自动识别子任务类型
  - 自动下载关联需求（story）和父任务（parent task）
  - 解决子任务（如 task 61563）描述字段 API 返回为空的问题
  - 确保获取完整需求描述，不再遗漏关键信息

### v1.5.0 重大更新

- **集成 superpowers 技能链** - 技术方案设计效率提升 70%+
  - 使用 `brainstorming` 技能进行需求分析和方案设计
  - 使用 `subagent-driven-development` 技能执行编码任务
  - 使用 `requesting-code-review` 技能进行代码评审
- **合并架构方案和编码方案**
  - 原两个独立阶段 → 合并为"技术实现方案设计"
  - 消除重复探索，一次完成所有设计工作
- **效率大幅提升**
  - 代理数量减少 85%：12-17 个 → 1-2 个
  - 简单需求耗时减少 70%：20+ 分钟 → 5-8 分钟

<details>
<summary>v1.4.x 历史功能</summary>

### v1.4.0 功能
- **方案质量自动评审**（可选）
- **快速/深度模式选择**
- **多项目配置支持**

</details>

## 快速开始

```
你: 帮我下载禅道需求 38817

Claude: [触发 zentao-workflow 技能]
        检测运行环境...
        ✓ Java 1.8.0 已检测到，使用 Java 版本

        首次使用需要配置禅道信息...
        ✓ 配置已完成

        正在下载需求 38817...
        ✓ 下载完成
          - MD 文件: story/38817-需求标题.md
          - 附件: 3 个文件已下载
          - 图片: 2 张图片已下载

        是否开始设计开发技术方案？
```

### 支持的输入格式

| 格式 | 示例 |
|------|------|
| 纯 ID | 38817 |
| URL | https://zentao.example.com/story-view-38817.html |
| 关键词+ID | 开发需求38817、任务12345 |

### 触发关键词

- 禅道、zentao、chandao
- 需求、开发需求、story
- 任务、task
- Bug、缺陷
- 下载禅道、获取需求

## 技术实现方案设计

v1.5.0 使用 `superpowers:brainstorming` 技能，一次完成所有设计工作。

| 指标 | v1.4.x | v1.5.0 | 提升 |
|------|--------|--------|------|
| 设计阶段 | 2 个（架构+编码） | 1 个（技术实现方案） | 减少 50% |
| 代理数量 | 12-17 个 | 1-2 个 | 减少 85%+ |
| 简单需求耗时 | 20+ 分钟 | 5-8 分钟 | 减少 70%+ |

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
├── .chandao/
│   └── config.properties          # 工作区配置（可选）
├── story_39382_技术实现方案.md    # 技术实现方案文档（v1.5.0 新格式）
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

### Q: 如何修改已保存的配置？

编辑 `~/.chandao/config.properties` 文件。

### Q: 下载失败怎么办？

常见原因：
1. 网络无法访问禅道服务器
2. 用户名或密码错误
3. ID 不存在或无权限访问

## 版本历史

| 版本 | 主要更新 |
|------|----------|
| 1.6.0 | 子任务检测与关联内容下载、解决子任务描述缺失问题、自动下载关联需求和父任务 |
| 1.5.0 | 集成 superpowers 技能链、合并架构/编码方案、效率提升 70%+ |
| 1.4.1 | 触发条件优化、Java 源码管理、文档同步 |
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

**版本**: 1.6.0 | **作者**: liuzl | **许可证**: MIT

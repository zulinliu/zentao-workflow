# Zentao Workflow Skill

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/zulinliu/zentao-workflow)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-purple.svg)](https://claude.ai/code)
[![Release](https://img.shields.io/github/release/zulinliu/zentao-workflow.svg)](https://github.com/zulinliu/zentao-workflow/releases)

禅道开发工作流助手 - 自动化禅道需求/任务/Bug 下载与开发技术方案设计。

## 快速安装

### 推荐方式：从 Releases 下载

前往 [Releases 页面](https://github.com/zulinliu/zentao-workflow/releases) 下载最新版本的 `zentao-workflow-vx.x.x.zip`。

```bash
# Linux/macOS
cd ~/.claude/skills
unzip ~/Downloads/zentao-workflow-v1.0.0.zip -d zentao-workflow

# Windows PowerShell
cd $env:USERPROFILE\.claude\skills
Expand-Archive $env:USERPROFILE\Downloads\zentao-workflow-v1.0.0.zip -DestinationPath zentao-workflow
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

- **智能触发** - 当提到"禅道"、"需求"、"任务"、"Bug"等关键词时自动激活
- **双运行时支持** - 内置 Java 和 Python 两个版本，自动选择最佳运行时
- **跨平台兼容** - 支持 Windows、macOS、Linux
- **自动环境配置** - 无环境时可自动安装 Python
- **交互式配置** - 引导用户完成禅道服务器配置
- **附件完整下载** - 下载所有附件和内容中嵌入的图片
- **技术方案生成** - 结合项目代码深度分析，生成详细的开发技术方案

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

## 技术方案包含

1. **需求分析** - 需求背景、功能点拆解、验收标准
2. **技术设计** - 技术选型、架构设计、接口设计
3. **编码实现步骤** - 详细的伪代码和分步骤实现
4. **测试计划** - 单元测试、集成测试、回归测试
5. **风险评估** - 潜在风险和应对措施

## 输出文件结构

```
{workspace}/
├── story_38817_技术方案.md    # 技术方案文档
├── story_38817_设计方案.md    # 设计方案文档（/plan模式后生成）
├── story/                      # 需求 Markdown 文件
│   └── 38817-需求标题.md
├── task/                       # 任务 Markdown 文件
│   └── 12345-任务名称.md
├── bug/                        # Bug Markdown 文件
│   └── 67890-Bug标题.md
└── attachments/                # 附件目录
    ├── story/38817/
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

## 版本管理

本项目采用语义化版本管理：
- **主版本号 (X.0.0)**: 重大架构变更或不兼容更新
- **次版本号 (1.X.0)**: 新增功能，向后兼容
- **修订号 (1.0.X)**: Bug 修复和小改进

查看 [Releases](https://github.com/zulinliu/zentao-workflow/releases) 获取所有版本更新记录。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 作者

- **liuzl** - [GitHub](https://github.com/zulinliu)

---

**版本**: 1.0.0 | **作者**: liuzl | **许可证**: MIT

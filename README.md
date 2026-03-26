# Zentao Workflow Skill

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/zulinliu/zentao-workflow)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-purple.svg)](https://claude.ai/code)

禅道开发工作流助手 - 自动化禅道需求/任务/Bug 下载与开发技术方案设计。

## 功能特性

- **智能触发** - 当提到"禅道"、"需求"、"任务"、"Bug"等关键词时自动激活
- **双运行时支持** - 内置 Java 和 Python 两个版本，自动选择最佳运行时
- **跨平台兼容** - 支持 Windows、macOS、Linux
- **自动环境配置** - 无环境时可自动安装 Python
- **交互式配置** - 引导用户完成禅道服务器配置
- **附件完整下载** - 下载所有附件和内容中嵌入的图片
- **技术方案生成** - 结合项目代码深度分析，生成详细的开发技术方案

## 环境要求

只需满足以下**任一**环境：

| 运行时 | 版本要求 | 优先级 |
|--------|----------|--------|
| Java | 8+ | 高（优先使用） |
| Python | 3.6+ | 中（默认备选） |

## 安装方法

### 方法一：复制到 Claude Code 插件目录

```bash
# Linux/macOS
cp -r zentao-workflow ~/.claude/skills/

# Windows PowerShell
xcopy /E /I zentao-workflow %USERPROFILE%\.claude\skills\zentao-workflow
```

### 方法二：从 GitHub 克隆

```bash
git clone https://github.com/zulinliu/zentao-workflow.git
cp -r zentao-workflow ~/.claude/skills/
```

### 验证安装

重启 Claude Code 后，技能会自动加载。可以通过以下方式验证：

```
你: 帮我下载禅道需求 38817
```

## 使用指南

### 快速开始

```
你: 我想开发禅道需求 38817

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

### 环境选择逻辑

| 检测结果 | 自动选择 |
|----------|---------|
| 仅 Java 可用 | Java 版 |
| 仅 Python 可用 | Python 版 |
| 两者都可用 | Java 版（更稳定） |
| 两者都不可用 | 询问用户，默认安装 Python |

### 支持的输入格式

| 格式 | 示例 |
|------|------|
| 纯 ID | 38817 |
| URL | https://zentao.example.com/story-view-38817.html |
| 关键词+ID | 开发需求38817、任务12345 |

### 技术方案包含

1. **需求分析** - 需求背景、功能点拆解、验收标准
2. **技术设计** - 技术选型、架构设计、接口设计
3. **编码实现步骤** - 详细的伪代码和分步骤实现
4. **测试计划** - 单元测试、集成测试、回归测试
5. **风险评估** - 潜在风险和应对措施

## 触发关键词

- 禅道、zentao、chandao
- 需求、开发需求、story
- 任务、task
- Bug、缺陷
- 下载禅道、获取需求
- 禅道 ID 或 URL

## 技能目录结构

```
zentao-workflow/
├── SKILL.md                      # 技能主文件
├── README.md                     # 本文档
├── LICENSE                       # MIT 许可证
├── CHANGELOG.md                  # 变更日志
├── VERSION                       # 版本号
├── .gitignore                    # Git 忽略配置
├── scripts/                      # 内置工具
│   ├── chandao-fetch.jar         # Java 版工具
│   ├── chandao_fetch/            # Python 版工具
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── client.py
│   │   ├── config.py
│   │   ├── exporter.py
│   │   ├── models.py
│   │   └── service.py
│   ├── chandao_fetch.py          # Python 入口
│   └── requirements.txt          # Python 依赖
├── assets/                       # 模板资源
│   ├── config_template.properties
│   └── tech_plan_template.md     # 技术方案模板
└── references/                   # 参考文档
    ├── java_project_guide.md     # Java 项目分析指南
    └── react_project_guide.md    # React 项目分析指南
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

### Q: 附件和图片会下载到哪里？

```
{workspace}/
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

## 开发

### 构建 Java 版本

```bash
mvn clean package -DskipTests
cp target/chandao-fetch.jar scripts/
```

### 安装 Python 依赖

```bash
pip install -r scripts/requirements.txt
```

## 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 作者

- **liuzl** - [GitHub](https://github.com/zulinliu)

## 致谢

- 感谢 [禅道](https://www.zentao.net/) 项目管理软件
- 感谢 [Claude Code](https://claude.ai/code) 平台

---

**版本**: 1.0.0 | **作者**: liuzl | **许可证**: MIT

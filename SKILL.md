---
name: zentao-workflow
description: |
  禅道开发工作流助手 - 自动化禅道需求/任务/Bug下载与开发方案设计。

  【触发条件】当用户提到以下任一内容时，必须使用此技能：
  - 禅道、zentao、chandao、禅道系统
  - 需求、开发需求、story、需求ID
  - 任务、task、任务ID
  - Bug、缺陷、bug ID
  - 下载禅道、获取需求、同步禅道
  - 开发某需求/任务、开始开发
  - 禅道URL链接（包含 story-view、task-view、bug-view）
  - 纯数字ID后跟"需求"/"任务"/"Bug"（如 "38817需求"）
  - 任何涉及禅道项目管理系统的请求

  【技能功能】
  1. 自动检测 Java/Python 环境，选择最佳运行时
  2. 内置下载工具，无需额外安装
  3. 交互式配置禅道服务器信息
  4. 下载需求/任务/Bug详情及附件到本地
  5. 结合项目代码生成详细开发技术方案

  即使只提到"需求"或"任务"关键词，只要上下文暗示与项目管理相关，也应触发此技能。
---

# 禅道开发工作流助手

## 内置工具

本技能内置两个版本的禅道下载工具，自动选择最佳运行时：

| 工具 | 位置 | 运行时 |
|------|------|--------|
| Java版 | `{SKILL_DIR}/scripts/chandao-fetch.jar` | Java 8+ |
| Python版 | `{SKILL_DIR}/scripts/chandao_fetch/` | Python 3.6+ |

## 执行步骤

### Step 1: 环境检测与运行时选择

**1.1 检测运行环境**

使用 Bash 工具依次检测：

```bash
# 检测 Java
java -version 2>&1 | head -1

# 检测 Python
python3 --version 2>&1 || python --version 2>&1
```

**1.2 选择运行时**

| 检测结果 | 运行时选择 |
|----------|-----------|
| 仅 Java 可用 | 使用 Java 版 |
| 仅 Python 可用 | 使用 Python 版 |
| 两者都可用 | 优先使用 Java 版（更稳定） |
| 两者都不可用 | 询问用户选择安装哪个 |

**1.3 询问用户选择**

如果两个环境都不可用，使用 AskUserQuestion 询问：

```
未检测到 Java 或 Python 运行环境，请选择要安装的环境：

1. Python（推荐） - 轻量级，安装快速
2. Java - 更稳定，但需要下载 JDK

请选择：
```

如果用户不选择，**默认使用 Python** 并自动安装：

```bash
# Windows (使用 winget)
winget install Python.Python.3.12

# macOS (使用 Homebrew)
brew install python3

# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install python3 python3-pip -y
```

安装完成后，安装 Python 依赖：

```bash
pip3 install requests
```

### Step 2: 禅道配置初始化

检查配置文件 `~/.chandao/config.properties` 是否存在。

**如果配置不存在**，使用 AskUserQuestion 工具收集：

| 配置项 | 必填 | 说明 |
|--------|------|------|
| 禅道服务器地址 | 是 | 如 https://zentao.example.com |
| 用户名 | 是 | 登录账号 |
| 密码 | 是 | 登录密码 |
| 存储目录 | 否 | 默认使用当前工作区根目录 |

**保存配置**：使用 Bash 工具创建配置文件

```bash
mkdir -p ~/.chandao
cat > ~/.chandao/config.properties << 'EOF'
zentao.url=<用户提供的地址>
zentao.username=<用户提供的用户名>
zentao.password=<用户提供的密码>
output.dir=<存储目录，默认为当前工作区>
EOF
```

**配置完成后展示**：

```
✓ 禅道配置已完成

  服务器: https://zentao.example.com
  用户名: your_username
  存储目录: /path/to/workspace  ← 禅道内容将保存在此目录
  运行时: Java 1.8.0 / Python 3.10

配置已保存到 ~/.chandao/config.properties
```

### Step 3: 获取禅道内容

**3.1 解析用户输入**

从用户消息中提取禅道 ID 或 URL：

```
支持的输入格式：
- 纯数字ID: 38817
- URL: https://zentao.example.com/story-view-38817.html
- 简短路径: /task-view-12345.html
- 关键词组合: 开发需求38817、任务12345、bug 67890
```

**3.2 如果无法从消息中提取 ID**

使用 AskUserQuestion 询问用户。

**3.3 多内容下载提醒**

如果用户要下载多个内容，**必须主动提醒**：

```
⚠️ 注意：您正在下载多个需求/任务内容。

不建议同时开发多个需求，容易导致理解偏差和代码冲突。
建议逐个完成开发工作。

请确认是否继续下载这些内容？
```

**3.4 执行下载**

根据运行时选择执行命令：

**Java 版本**：
```bash
java -jar {SKILL_DIR}/scripts/chandao-fetch.jar -t {type} -i {id}
```

**Python 版本**：
```bash
python3 {SKILL_DIR}/scripts/chandao_fetch.py -t {type} -i {id}
```

参数说明：
- `{type}`: story / task / bug
- `{id}`: 禅道 ID

**下载完成后展示**：

```
✓ 下载完成

  类型: 需求
  ID: 38817
  标题: 用户登录功能优化
  文件: /path/to/workspace/story/38817-用户登录功能优化.md
  附件: 3个文件已下载到 attachments/story/38817/
```

### Step 4: 开发技术方案设计

**4.1 询问用户是否开始开发**

```
需求内容已下载完成。是否开始设计开发技术方案？

选项：
- 是，开始设计技术方案
- 否，仅下载内容（技能结束）
```

**4.2 进入 Plan 模式**

如果用户确认，使用 EnterPlanMode 工具进入规划模式。

**4.3 深度学习与分析**

在 Plan 模式中：

1. **阅读禅道内容** - 读取下载的 Markdown 文件
2. **查看附件和图片** - **重要**：检查是否有附件和内嵌图片
   - 附件目录: `{output_dir}/attachments/{type}/{id}/`
   - 内嵌图片: Markdown中的 `![](../attachments/...)` 引用
   - 使用 Read 工具查看图片内容（PNG/JPG等）
3. **分析项目代码** - 根据项目类型执行不同的分析策略
4. **技术栈检测** - 检查 pom.xml 或 package.json 判断项目类型

**读取图片说明**：
- 附件中的截图通常包含UI原型、数据流程图、错误截图等关键信息
- 使用 Read 工具直接读取图片路径，Claude 可以理解图片内容
- 示例: `Read tool with path="/path/to/attachments/story/38817/screenshot.png"`

**Java 项目分析** - 参考 `{SKILL_DIR}/references/java_project_guide.md`

**React 项目分析** - 参考 `{SKILL_DIR}/references/react_project_guide.md`

**4.4 编写技术方案**

参考 `{SKILL_DIR}/assets/tech_plan_template.md` 模板，包含：

1. **需求分析** - 需求背景、功能点拆解、验收标准
2. **技术设计** - 技术选型、架构设计、接口设计
3. **编码实现步骤** - 详细的伪代码和分步骤实现
4. **测试计划** - 单元测试、集成测试
5. **风险评估** - 潜在风险和应对措施

**4.5 疑问确认**

如果在方案设计过程中发现存疑点，**必须主动向用户提问**。

### Step 5: 输出技术方案

**5.1 保存技术方案**

将最终版本的技术方案保存到工作区根目录：

```
文件命名: {类型}_{ID}_技术方案.md
示例: story_38817_技术方案.md
```

**5.2 展示方案摘要并询问下一步**

```
技术方案已完成并保存到: story_38817_技术方案.md

【需求分析】
- 功能点: xxx
- 验收标准: xxx

【技术设计】
- 涉及模块: xxx
- 关键改动: xxx

【实现步骤】共 N 步
1. xxx
2. xxx
...

是否按照此技术方案开始编码实现？
```

### Step 6: 开发入口选择

使用 AskUserQuestion 让用户选择：

| 选项 | 说明 |
|------|------|
| 直接开始编码 | 技能结束，Claude 自动开始实现代码 |
| 进入 /plan 模式 | 先查看详细的执行计划再开始 |
| 修改技术方案 | 返回 Step 4 重新设计方案 |
| 暂不开发 | 技能结束，保留已下载的内容和方案 |

### Step 7: 设计方案保存（仅 /plan 模式）

**7.1 当用户选择"进入 /plan 模式"时**

进入 Plan 模式后，会进行详细的实现规划。规划完成后需要与用户迭代确认。

**7.2 迭代确认流程**

```
规划内容已生成，请审阅：

【实现计划】
- 步骤1: xxx
- 步骤2: xxx
...

是否需要调整？如无问题请确认，确认后将保存设计方案并开始编码。
```

**7.3 保存最终设计方案**

**重要**：只有当用户明确确认规划内容后，才保存设计方案。

```bash
# 文件命名规则
{类型}_{ID}_设计方案.md

# 示例
story_38817_设计方案.md
task_12345_设计方案.md
bug_67890_设计方案.md
```

**保存位置**：工作区根目录

**设计方案内容结构**：
```markdown
# {类型}_{ID} 设计方案

> 创建时间: {日期}
> 状态: 已确认

## 一、需求概述
<!-- 简要描述需求背景和目标 -->

## 二、技术方案
<!-- 技术选型、架构设计等 -->

## 三、实现计划
<!-- 详细的实现步骤 -->

### Step 1: {步骤标题}
- 目标: xxx
- 涉及文件: xxx
- 实现要点: xxx

### Step 2: {步骤标题}
...

## 四、风险点
<!-- 需要注意的风险和应对措施 -->

## 五、测试计划
<!-- 验证方案 -->
```

**7.4 确认保存**

```
✓ 设计方案已保存

  文件: /path/to/workspace/story_38817_设计方案.md

现在开始按照设计方案进行编码实现...
```

## 输出标准

### 必须输出

1. **环境检测结果** - 显示使用的运行时（Java/Python）
2. **配置确认信息** - 包含存储目录的完整配置信息
3. **下载结果** - 文件路径、附件数量
4. **技术方案文档** - Markdown 格式，保存在工作区根目录
5. **设计方案文档**（如有） - /plan 模式完成后的最终方案

### 文件结构

```
{workspace}/
├── story_38817_技术方案.md    # 技术方案文档
├── story_38817_设计方案.md    # 设计方案文档（/plan模式后生成）
├── story/                      # 禅道内容目录
│   └── 38817-需求标题.md
└── attachments/                # 附件目录
    └── story/38817/
```

## 注意事项

1. **跨平台兼容** - 支持 Windows/macOS/Linux
2. **运行时优先级** - Java > Python（两者都可用时）
3. **自动安装** - 无环境时默认安装 Python
4. **配置持久化** - 禅道配置保存后，后续使用无需重新输入
5. **主动沟通** - 方案设计中有疑问必须主动询问

## 相关资源

- `{SKILL_DIR}/scripts/chandao-fetch.jar` - Java 版内置工具
- `{SKILL_DIR}/scripts/chandao_fetch/` - Python 版内置工具
- `{SKILL_DIR}/assets/tech_plan_template.md` - 技术方案模板
- `{SKILL_DIR}/references/java_project_guide.md` - Java 项目分析指南
- `{SKILL_DIR}/references/react_project_guide.md` - React 项目分析指南

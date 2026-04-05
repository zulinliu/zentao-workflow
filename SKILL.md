---
name: zentao-workflow
description: |
  禅道开发工作流助手 v1.6.0 - 自动化禅道需求/任务/Bug 下载与技术实现方案设计。

  【v1.6.0 核心更新】
  - 新增子任务检测与关联内容下载逻辑
  - 解决子任务（如 task 61563）描述为空的问题
  - 自动下载关联需求和父任务，确保获取完整需求描述

  【v1.5.0 核心更新】
  - 集成 superpowers:brainstorming 技能，技术方案设计效率提升 70%+
  - 合并架构方案和编码方案为"技术实现方案"，消除重复探索
  - 代理数量减少 85%（12-17个 → 1-2个），简单需求 5-8 分钟完成
  - 聚焦三项核心内容：需求分析、架构设计、实现步骤

  【触发条件】当用户提到以下任一内容时，必须使用此技能：
  - 禅道、zentao、chandao、禅道系统
  - 需求、开发需求、story、需求ID
  - 任务、task、任务ID
  - Bug、缺陷、bug ID
  - 下载禅道、获取需求、同步禅道
  - 开发某需求/任务、开始开发
  - 禅道URL链接（包含 story-view、task-view、bug-view）
  - ID与类型组合：
    - "需求39382"、"任务12345"、"Bug67890"（类型+ID）
    - "39382需求"、"12345任务"、"67890Bug"（ID+类型）
    - "禅道需求39382"、"开发任务12345"（前缀+类型+ID）
  - 任何涉及禅道项目管理系统的请求

  【技能功能】
  1. 自动检测 Java/Python 环境和 superpowers 技能依赖
  2. 内置下载工具，无需额外安装
  3. 交互式配置禅道服务器信息
  4. 下载需求/任务/Bug 详情及附件到本地
  5. 使用 brainstorming 技能生成技术实现方案
  6. 子任务自动检测与关联内容下载（v1.6.0 新增）

  【依赖】需要 superpowers 插件 5.0.6+

  即使只提到"需求"或"任务"关键词，只要上下文暗示与项目管理相关，也应触发此技能。
---

# 禅道开发工作流助手

## 内置工具

本技能内置两个版本的禅道下载工具，自动选择最佳运行时：

| 工具 | 位置 | 运行时 |
|------|------|--------|
| Python 版 | `{SKILL_DIR}/scripts/worklet.py` | Python 3.10+ |

## 执行步骤

### Step 1: 环境检测与运行时选择

**1.1 检测 superpowers 技能（v1.5.0 新增）**

**重要**：v1.5.0 版本依赖 superpowers 插件，必须先检测。

使用 Bash 工具检测：

```bash
# 检测 superpowers 插件
ls ~/.claude/plugins/cache/claude-plugins-official/superpowers/ 2>/dev/null | head -1
```

**检测结果处理**：

| 检测结果 | 处理方式 |
|----------|----------|
| 检测到 5.0.6+ 版本 | 继续执行 |
| 检测到旧版本 | 提示用户更新 |
| 未检测到 | 询问用户是否安装 |

**如果未安装**，使用 AskUserQuestion 询问：

```
AskUserQuestion:
  questions:
    - question: "检测到 superpowers 技能未安装，是否自动安装？"
      header: "技能依赖"
      options:
        - label: "是，自动安装"
          description: "执行 claude plugins add official superpowers"
        - label: "否，稍后手动安装"
          description: "技能继续，但技术方案设计功能将不可用"
```

**自动安装命令**：

```bash
claude plugins add official superpowers
```

**1.2 检测运行环境**

使用 Bash 工具检测 Python：

```bash
# 检测 Python
python3 --version 2>&1 || python --version 2>&1
```

**1.3 选择运行时**

| 检测结果 | 运行时选择 |
|----------|-----------|
| Python 可用 | 使用 Python 版 |
| Python 不可用 | 询问用户选择安装 |

**1.3 询问用户选择**

如果两个环境都不可用，使用 AskUserQuestion 询问：

```
未检测到 Python 运行环境，请选择要安装的环境：

1. Python（推荐） - 轻量级，安装快速

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

**配置文件优先级**（支持多项目开发）：

```
1. 工作区配置: {工作区}/.chandao/config.properties  ← 最高优先
2. 全局配置: ~/.chandao/config.properties           ← 兜底配置
```

**存储目录说明**：
- 存储目录不保存到配置文件，每次运行时动态确定
- 默认使用当前工作区根目录
- 支持多项目并行开发，每个项目独立存储

**检测配置文件**：按优先级检查工作区配置和全局配置是否存在。

**如果配置不存在**，**必须主动使用 AskUserQuestion 工具一次性收集所有配置信息**：

```
AskUserQuestion:
  questions:
    - question: "请输入禅道服务器地址"
      header: "服务器"
      options:
        - label: "跳过配置"
          description: "稍后手动配置"
        - label: "(Other)"
          description: "输入完整地址，如 https://zentao.example.com"

    - question: "请输入禅道登录用户名"
      header: "用户名"
      options:
        - label: "跳过"
          description: "稍后配置"
        - label: "(Other)"
          description: "输入您的登录账号"

    - question: "请输入禅道登录密码"
      header: "密码"
      options:
        - label: "跳过"
          description: "稍后配置"
        - label: "(Other)"
          description: "输入您的登录密码"

    - question: "禅道内容存储目录（可选）"
      header: "存储目录"
      options:
        - label: "使用当前目录"
          description: "默认使用工作区根目录"
        - label: "(Other)"
          description: "输入自定义路径"
```

**配置项说明**：

| 配置项 | 必填 | 说明 |
|--------|------|------|
| 禅道服务器地址 | 是 | 如 https://zentao.example.com |
| 用户名 | 是 | 登录账号 |
| 密码 | 是 | 登录密码或 API Token |
| 存储目录 | 否 | 默认使用当前工作区根目录 |

**保存配置**：使用 Bash 工具创建配置文件

```bash
# 保存到工作区（推荐，支持多项目）
mkdir -p "{工作区}/.chandao"
cat > "{工作区}/.chandao/config.properties" << 'EOF'
zentao.url=<用户提供的地址>
zentao.username=<用户提供的用户名>
zentao.password=<用户提供的密码>
EOF

# 或保存到全局（所有项目共享）
mkdir -p ~/.chandao
cat > ~/.chandao/config.properties << 'EOF'
zentao.url=<用户提供的地址>
zentao.username=<用户提供的用户名>
zentao.password=<用户提供的密码>
EOF
```

**配置完成后展示**：

```
✓ 禅道配置已完成

  配置来源: 工作区配置 (.chandao/config.properties)
  服务器: https://zentao.example.com
  用户名: your_username
  存储目录: /path/to/workspace  ← 禅道内容将保存在此目录
  运行时: Java 1.8.0 / Python 3.10
```

**如果配置已存在**：

1. 读取并展示当前配置（显示配置来源：工作区/全局）
2. **必须**确认存储目录（每次运行时动态确认）：

```
AskUserQuestion:
  questions:
    - question: "禅道内容存储目录"
      header: "存储目录"
      options:
        - label: "使用当前工作区"
          description: "默认：/path/to/current/workspace"
        - label: "(Other)"
          description: "输入自定义存储路径"
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

**Python 版本**：
```bash
# Linux/macOS
python3 "{SKILL_DIR}/scripts/worklet.py" -t {type} -i {id}

# Windows (注意：使用正斜杠或双反斜杠)
python3 "{SKILL_DIR}/scripts/worklet.py" -t {type} -i {id}
```

参数说明：
- `{type}`: story / task / bug
- `{id}`: 禅道 ID
- `-Dfile.encoding=UTF-8`: 确保跨平台中文显示正常
- 路径使用**双引号**包裹，避免空格问题

**3.5 子任务检测与关联内容下载（v1.6.0 新增）**

**问题背景**：禅道的子任务（如 task 61563）的 `desc` 字段 API 返回为空，实际需求描述存储在：
- 关联的需求（story）
- 父任务（parent task）

**检测逻辑**：

下载任务后，检查生成的 Markdown 文件内容：

```bash
# 检查任务描述是否为空
if ! grep -q "^## 任务描述" "{output}/{type}/{id}-*.md" 2>/dev/null; then
  echo "检测到子任务，描述为空，需要下载关联内容"
fi
```

**关联内容下载策略**：

| 场景 | 下载策略 |
|------|----------|
| 任务描述为空 | 1. 读取任务 MD 获取 `story` 字段（关联需求 ID）<br>2. 读取任务 MD 获取 `parent` 字段（父任务 ID）<br>3. 自动下载关联需求和父任务 |
| 任务描述非空 | 无需额外下载 |

**自动下载命令**：

```bash
# 下载关联需求
python3 "{SKILL_DIR}/scripts/worklet.py" -t story -i {storyId}

# 下载父任务
python3 "{SKILL_DIR}/scripts/worklet.py" -t task -i {parentTaskId}
```

**下载完成后展示**：

```
✓ 下载完成

  类型：任务（子任务）
  ID: 61563
  标题：【后端】统计分析 - 出清统计分析
  文件：/path/to/workspace/task/61563-标题.md

  关联内容已自动下载：
  - 需求 39415: /path/to/workspace/story/39415-需求标题.md
  - 父任务 61549: /path/to/workspace/task/61549-父任务标题.md

  附件：3 个文件已下载到 attachments/task/61563/
```

**3.6 需求分析引导**

下载完成后，展示需求的核心描述内容（从关联需求/父任务中提取），帮助用户快速理解：

```
📋 需求摘要

【需求来源】
- 需求 ID: 39415
- 需求标题：统计分析 - 出清统计分析 - 出清电力分析"模块，"长周期运行分析"TAB 页表格完善
- 任务 ID: 61563（子任务）

【核心描述】
"统计分析 - 出清统计分析 - 出清电力分析"模块，"长周期运行分析"TAB 页，分析方法选择：
全网--保供与消纳场景
分别在最大保供出清电力、最大消纳出清电力后增加一列时间，注：时间写法为"2026-01-23 00:15"

【验收标准】
1. 在最大保供出清电力后增加时间列
2. 在最大消纳出清电力后增加时间列
3. 时间格式：yyyy-MM-dd HH:mm
```

### Step 4: 技术实现方案设计

**4.1 询问用户是否开始设计（必须执行）**

**重要**：下载完成后，**必须**使用 AskUserQuestion 询问用户。

```
AskUserQuestion:
  questions:
    - question: "需求内容已下载完成。是否开始技术实现方案设计？"
      header: "下一步"
      options:
        - label: "是，开始设计（推荐）"
          description: "使用 superpowers:brainstorming 生成技术实现方案（5-8分钟）"
        - label: "否，仅下载"
          description: "技能结束，保留已下载的内容"
```

**如果用户选择"否"**：技能结束，展示下载的文件路径。

**如果用户选择"是"**：继续 Step 4.2。

**4.2 调用 superpowers:brainstorming（核心步骤）**

**重要**：使用 Skill 工具调用 brainstorming 技能，传递上下文信息。

```
Skill(skill: "superpowers:brainstorming")
```

**上下文传递**（通过对话内容传递，非参数）：

在调用前，输出以下上下文信息：

```
📊 技术实现方案设计 - 上下文信息

【禅道内容】
- 类型: {story/task/bug}
- ID: {id}
- 标题: {title}
- 内容文件: {workspace}/{type}/{id}-{title}.md
- 附件目录: {workspace}/attachments/{type}/{id}/

【项目信息】
- 工作区路径: {workspace}
- 技术栈: {Java/React/Unknown} (从 pom.xml/package.json 自动检测)

【输出要求】
- 输出文件: {workspace}/{type}_{id}_技术实现方案.md
- 聚焦三项内容：
  1. 需求分析 - 背景、功能点拆解、验收标准
  2. 架构设计 - 技术选型、模块设计、接口设计
  3. 实现步骤 - 详细编码步骤
```

**4.3 brainstorming 工作流**

brainstorming 技能将自动执行：

1. **探索项目上下文** - 读取禅道文件、查看项目结构
2. **提出澄清问题** - 通过 AskUserQuestion 逐一询问
3. **提出 2-3 种技术方案** - 包含权衡分析和推荐
4. **编写技术实现方案** - 保存到工作区
5. **用户确认** - 展示方案摘要，等待用户批准

**4.4 进度提示（必须执行）**

在 brainstorming 执行过程中，定期输出进度提示：

```
📊 技术实现方案设计进度：

[✓] 阶段 1/3: 阅读禅道需求内容
[●] 阶段 2/3: 分析项目代码 ← 进行中...
[ ] 阶段 3/3: 编写技术实现方案
```

**4.5 技术实现方案内容**

输出文件：`{workspace}/{type}_{id}_技术实现方案.md`

**必须包含三项核心内容**：

1. **需求分析**（重点强化）
   - 需求背景
   - 功能点拆解（逐条列出）
   - 验收标准（可验证的具体条件）

2. **架构设计**（重点强化）
   - 技术选型（框架、库、工具）
   - 模块设计（涉及的模块和职责）
   - 接口设计（API 接口、数据结构）

3. **实现步骤**（重点强化）
   - 详细编码步骤（5-10 步）
   - 每步涉及的具体文件
   - 关键代码位置

**已移除的内容**：
- ~~测试计划~~ - 不再输出
- ~~风险评估~~ - 不再输出

### Step 5: 输出技术实现方案

**5.1 确认技术实现方案**

```
✓ 技术实现方案已完成

  文件: story_39382_技术实现方案.md

【需求分析】
- 功能点: xxx
- 验收标准: xxx

【架构设计】
- 涉及模块: xxx
- 关键改动: xxx

【实现步骤】共 N 步
1. 创建 Entity 类
2. 创建 Mapper 接口
3. 创建 Service 层
4. 创建 Controller
5. 编写单元测试
```

**5.2 询问用户下一步**

```
AskUserQuestion:
  questions:
    - question: "技术实现方案已完成。下一步？"
      header: "继续"
      options:
        - label: "开始编码实现（推荐）"
          description: "使用 superpowers:subagent-driven-development 执行"
        - label: "启动代码评审"
          description: "调用 superpowers:requesting-code-review 检查方案"
        - label: "修改方案"
          description: "返回修改技术实现方案"
        - label: "暂不开发"
          description: "技能结束，保留已下载的内容和方案"
```

### Step 6: 开始编码实现

**6.1 询问执行方式**

```
AskUserQuestion:
  questions:
    - question: "请选择编码执行方式："
      header: "执行方式"
      options:
        - label: "子代理驱动（推荐）"
          description: "使用 superpowers:subagent-driven-development，每个任务一个子代理"
        - label: "内联执行"
          description: "使用 superpowers:executing-plans，批量执行"
        - label: "手动执行"
          description: "技能结束，我来手动实现"
```

**6.2 调用执行技能**

根据用户选择调用对应技能：

| 选择 | 调用技能 |
|------|----------|
| 子代理驱动 | `Skill(skill: "superpowers:subagent-driven-development")` |
| 内联执行 | `Skill(skill: "superpowers:executing-plans")` |
| 手动执行 | 技能结束 |

**传递给执行技能的上下文**：

```
【技术实现方案】
- 文件路径: {workspace}/{type}_{id}_技术实现方案.md

【项目信息】
- 工作区路径: {workspace}
```

## 输出标准

### 必须输出

1. **环境检测结果** - 显示使用的运行时（Java/Python）和 superpowers 技能状态
2. **配置确认信息** - 包含配置来源和存储目录
3. **下载结果** - 文件路径、附件数量
4. **技术实现方案文档** - Markdown 格式，保存在工作区根目录

### 文件结构

```
{workspace}/
├── .chandao/
│   └── config.properties          # 工作区配置（可选）
├── story_39382_技术实现方案.md    # 技术实现方案文档（v1.5.0 新格式）
├── story/                         # 禅道内容目录
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

## 注意事项

1. **superpowers 技能依赖** - v1.5.0 需要安装 superpowers 插件 5.0.6+
2. **跨平台兼容** - 支持 Windows/macOS/Linux
3. **配置优先级** - 工作区配置 > 全局配置
4. **主动沟通** - 方案设计中有疑问必须主动询问
5. **效率优化** - v1.5.0 通过集成 brainstorming 技能，代理数量减少 85%+
6. **子任务处理** - v1.6.0 自动检测子任务并下载关联需求和父任务

## 相关资源

- `{SKILL_DIR}/scripts/worklet.py` - Python 版内置工具
- `{SKILL_DIR}/scripts/worklet/` - Python 版内置工具包
- `{SKILL_DIR}/assets/tech_plan_template.md` - 技术方案模板
- `{SKILL_DIR}/references/java_project_guide.md` - Java 项目分析指南
- `{SKILL_DIR}/references/react_project_guide.md` - React 项目分析指南
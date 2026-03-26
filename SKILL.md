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
| Python版 | `{SKILL_DIR}/scripts/chandao_fetch.py` | Python 3.6+ |

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

**重要**：路径格式需要适配操作系统：
- **Windows**: 使用双引号包裹路径，正斜杠 `/` 或双反斜杠 `\\`
- **Linux/macOS**: 直接使用正斜杠 `/`

**Java 版本**：
```bash
# Linux/macOS
java -Dfile.encoding=UTF-8 -Dconsole.encoding=UTF-8 -jar "{SKILL_DIR}/scripts/chandao-fetch.jar" -t {type} -i {id}

# Windows
java -Dfile.encoding=UTF-8 -Dconsole.encoding=UTF-8 -jar "{SKILL_DIR}/scripts/chandao-fetch.jar" -t {type} -i {id}
```

**Python 版本**：
```bash
# Linux/macOS
python3 "{SKILL_DIR}/scripts/chandao_fetch.py" -t {type} -i {id}

# Windows (注意：使用正斜杠或双反斜杠)
python3 "{SKILL_DIR}/scripts/chandao_fetch.py" -t {type} -i {id}
```

参数说明：
- `{type}`: story / task / bug
- `{id}`: 禅道 ID
- `-Dfile.encoding=UTF-8`: 确保跨平台中文显示正常
- 路径使用**双引号**包裹，避免空格问题

**下载完成后展示**：

```
✓ 下载完成

  类型: 需求
  ID: 38817
  标题: 用户登录功能优化
  文件: /path/to/workspace/story/38817-用户登录功能优化.md
  附件: 3个文件已下载到 attachments/story/38817/
```

### Step 4: 架构方案设计

**4.1 询问用户是否开始架构设计（必须执行）**

**重要**：下载完成后，**必须**使用 AskUserQuestion 询问用户，**不能直接进入 Plan 模式**。

```
AskUserQuestion:
  questions:
    - question: "需求内容已下载完成。是否开始架构方案设计？"
      header: "下一步"
      options:
        - label: "是，开始设计"
          description: "进入架构方案设计，分析项目结构并设计技术方案"
        - label: "否，仅下载"
          description: "技能结束，保留已下载的内容"
```

**如果用户选择"否"**：技能结束，展示下载的文件路径。

**如果用户选择"是"**：继续 Step 4.2。

**4.2 选择设计模式（必须执行）**

**重要**：进入 Plan 模式前，**必须**让用户选择设计模式。

```
AskUserQuestion:
  questions:
    - question: "请选择架构方案设计模式："
      header: "设计模式"
      options:
        - label: "快速模式（推荐）"
          description: "2-3分钟完成，启动3个探索代理，适合简单需求"
        - label: "深度模式"
          description: "5-15分钟完成，启动6个探索代理并行分析，适合复杂需求"
```

**模式说明**：

| 模式 | 耗时 | 探索代理数 | 适用场景 |
|------|------|-----------|----------|
| 快速模式 | 2-3分钟 | 3个并行 | 简单需求、熟悉的项目 |
| 深度模式 | 5-15分钟 | 6个并行 | 复杂需求、新项目 |

**4.3 进入 Plan 模式并启动探索代理**

使用 EnterPlanMode 进入规划模式。

**在 Plan 模式中，根据用户选择的模式启动探索代理**：

**快速模式（3个并行代理）**：
```
🚀 启动快速模式架构分析...

正在启动探索代理 [1/3]...
└─ 分析: 需求相关业务代码

正在启动探索代理 [2/3]...
└─ 分析: 相似功能实现模式

正在启动探索代理 [3/3]...
└─ 分析: 数据模型和接口设计
```

**深度模式（6个并行代理）**：
```
🚀 启动深度模式架构分析...

正在启动探索代理 [1/6]...
└─ 分析: 业务逻辑代码（Controller/Service/DAO层）

正在启动探索代理 [2/6]...
└─ 分析: 数据模型设计（Entity/DTO/数据库表结构）

正在启动探索代理 [3/6]...
└─ 分析: API接口设计（REST接口、请求响应格式）

正在启动探索代理 [4/6]...
└─ 分析: 相似功能实现参考（查找类似功能的代码）

正在启动探索代理 [5/6]...
└─ 分析: 前端组件（如有，分析页面结构和交互）

正在启动探索代理 [6/6]...
└─ 分析: 配置和依赖（pom.xml/package.json、配置文件）
```

**4.4 进度提示（必须执行）**

**重要**：在探索过程中，**必须**定期输出进度提示，让用户感知正在进行中。

**进度提示格式**（每完成一个阶段输出一次）：

```
📊 架构方案设计进度：

[✓] 阶段 1/4: 阅读禅道需求内容
[✓] 阶段 2/4: 查看附件和图片
[●] 阶段 3/4: 探索项目代码 ← 进行中...
[ ] 阶段 4/4: 编写架构方案
```

**4.5 深度学习与分析**

在 Plan 模式中：

1. **阅读禅道内容** - 读取下载的 Markdown 文件
2. **查看附件和图片** - **重要**：检查是否有附件和内嵌图片
   - 附件目录: `{output_dir}/attachments/{type}/{id}/`
   - 使用 Read 工具查看图片内容
3. **分析项目代码** - 由探索代理完成
4. **技术栈检测** - 检查 pom.xml 或 package.json

**4.6 编写架构方案**

参考 `{SKILL_DIR}/assets/tech_plan_template.md` 模板，输出包含：

1. **需求分析** - 需求背景、功能点拆解、验收标准
2. **技术设计** - 技术选型、架构设计、接口设计
3. **影响范围** - 涉及的模块和文件

**4.7 疑问确认**

如果在方案设计过程中发现存疑点，**必须主动向用户提问**。

### Step 5: 输出架构方案

**5.1 保存架构方案**

```
文件命名: {类型}_{ID}_架构方案.md
示例: story_38817_架构方案.md
```

**5.2 展示方案摘要**

```
✓ 架构方案已完成

  文件: story_38817_架构方案.md

【需求分析】
- 功能点: xxx
- 验收标准: xxx

【技术设计】
- 涉及模块: xxx
- 关键改动: xxx

【实现步骤】共 N 步
```

**5.3 方案质量评审（可选）**

**重要**：在用户评审前，提供自动评审选项。

```
AskUserQuestion:
  questions:
    - question: "是否启动自动评审来检查方案质量？"
      header: "质量评审"
      options:
        - label: "启动自动评审（推荐）"
          description: "启动3个评审代理，从不同角度检查方案质量"
        - label: "跳过，直接继续"
          description: "跳过自动评审，直接进入下一步"
```

**如果用户选择"启动自动评审"**：

```
🔍 启动架构方案自动评审...

正在启动评审代理 [1/3]...
└─ 评审: 需求覆盖性检查
   • 功能点是否全部覆盖
   • 验收标准是否可验证
   • 边界条件是否考虑

正在启动评审代理 [2/3]...
└─ 评审: 技术可行性检查
   • 技术选型是否合理
   • 是否有技术风险或依赖遗漏
   • 性能和安全是否考虑

正在启动评审代理 [3/3]...
└─ 评审: 架构一致性检查
   • 是否与现有架构一致
   • 是否有破坏性改动
   • 模块划分是否合理
```

**评审结果展示**：

```
📊 评审报告

【需求覆盖性】✓ 通过
- 所有功能点已覆盖
- 验收标准明确可验证

【技术可行性】⚠ 有建议
- 建议补充：xxx 的错误处理机制
- 建议考虑：xxx 的性能优化方案

【架构一致性】✓ 通过
- 与现有架构风格一致
- 无破坏性改动

【综合评分】85/100
【建议】根据评审建议优化方案后继续
```

**如果评审发现问题**，询问用户：
```
AskUserQuestion:
  questions:
    - question: "评审发现 N 个优化建议，如何处理？"
      header: "评审结果"
      options:
        - label: "自动优化方案"
          description: "根据评审建议自动优化架构方案"
        - label: "手动调整"
          description: "我来手动调整方案"
        - label: "忽略建议"
          description: "保持当前方案，继续下一步"
```

**5.4 询问用户下一步**

```
AskUserQuestion:
  questions:
    - question: "架构方案已完成。下一步？"
      header: "继续"
      options:
        - label: "开始编码方案设计"
          description: "进入编码方案设计，生成详细的实现步骤"
        - label: "直接开始编码"
          description: "跳过编码方案，立即开始实现"
        - label: "修改架构方案"
          description: "返回修改架构方案"
        - label: "暂不开发"
          description: "技能结束，保留已下载的内容和方案"
```

### Step 6: 编码方案设计

**6.1 选择设计模式（必须执行）**

如果用户选择"开始编码方案设计"：

```
AskUserQuestion:
  questions:
    - question: "请选择编码方案设计模式："
      header: "设计模式"
      options:
        - label: "快速模式（推荐）"
          description: "2-3分钟完成，启动3个代理，生成核心实现步骤"
        - label: "深度模式"
          description: "5-10分钟完成，启动5个代理，生成详细伪代码和测试计划"
```

**模式说明**：

| 模式 | 耗时 | 探索代理数 | 输出内容 |
|------|------|-----------|----------|
| 快速模式 | 2-3分钟 | 3个并行 | 核心实现步骤、关键代码位置 |
| 深度模式 | 5-10分钟 | 5个并行 | 详细步骤、伪代码、测试计划、风险评估 |

**6.2 进入 Plan 模式并启动探索代理**

```
🚀 启动编码方案设计...

📊 编码方案设计进度：

[✓] 阶段 1/3: 分析架构方案
[●] 阶段 2/3: 设计实现细节 ← 进行中...
[ ] 阶段 3/3: 编写编码方案
```

**快速模式（3个并行代理）**：
```
正在启动探索代理 [1/3]...
└─ 分析: 需要修改的代码文件定位

正在启动探索代理 [2/3]...
└─ 分析: 数据库表和实体类变更

正在启动探索代理 [3/3]...
└─ 分析: API接口和参数定义
```

**深度模式（5个并行代理）**：
```
正在启动探索代理 [1/5]...
└─ 分析: 后端代码实现细节（Controller/Service/DAO）

正在启动探索代理 [2/5]...
└─ 分析: 数据库变更（DDL/DML语句）

正在启动探索代理 [3/5]...
└─ 分析: API接口契约（请求/响应格式）

正在启动探索代理 [4/5]...
└─ 分析: 前端组件变更（如有）

正在启动探索代理 [5/5]...
└─ 分析: 单元测试和集成测试设计
```

**6.3 编码方案内容**

**快速模式**：
- 核心实现步骤（3-5步）
- 关键代码位置
- 简要测试说明

**深度模式**：
- 详细实现步骤（5-10步）
- 伪代码示例
- 完整测试计划
- 风险评估

**6.4 保存编码方案**

```
文件命名: {类型}_{ID}_编码方案.md
示例: story_38817_编码方案.md
```

**6.5 展示方案摘要**

```
✓ 编码方案已完成

  文件: story_38817_编码方案.md

【实现步骤】共 N 步
1. xxx
2. xxx
...

【测试计划】
- 单元测试: xxx
- 集成测试: xxx
```

**6.6 方案质量评审（可选）**

**重要**：在用户评审前，提供自动评审选项。

```
AskUserQuestion:
  questions:
    - question: "是否启动自动评审来检查编码方案质量？"
      header: "质量评审"
      options:
        - label: "启动自动评审（推荐）"
          description: "启动3个评审代理，从不同角度检查编码方案"
        - label: "跳过，直接继续"
          description: "跳过自动评审，直接进入下一步"
```

**如果用户选择"启动自动评审"**：

```
🔍 启动编码方案自动评审...

正在启动评审代理 [1/3]...
└─ 评审: 实现完整性检查
   • 编码步骤是否覆盖架构方案的所有设计点
   • 前后步骤是否有遗漏或断层
   • 数据流是否完整闭环

正在启动评审代理 [2/3]...
└─ 评审: 代码可行性检查
   • 伪代码是否可执行
   • 异常处理是否完整
   • 边界条件是否考虑

正在启动评审代理 [3/3]...
└─ 评审: 测试覆盖性检查
   • 测试用例是否覆盖所有功能点
   • 边界条件和异常场景是否覆盖
   • 测试数据是否充分
```

**评审结果展示**：

```
📊 编码方案评审报告

【实现完整性】✓ 通过
- 所有设计点已覆盖
- 步骤衔接清晰

【代码可行性】⚠ 有建议
- 建议补充：xxx 的空值判断
- 建议增加：xxx 的重试机制

【测试覆盖性】✓ 通过
- 功能测试覆盖完整
- 边界条件已考虑

【综合评分】90/100
【建议】根据评审建议优化后可开始编码
```

**如果评审发现问题**，询问用户：
```
AskUserQuestion:
  questions:
    - question: "评审发现 N 个优化建议，如何处理？"
      header: "评审结果"
      options:
        - label: "自动优化方案"
          description: "根据评审建议自动优化编码方案"
        - label: "手动调整"
          description: "我来手动调整方案"
        - label: "忽略建议"
          description: "保持当前方案，开始编码"
```

**6.7 询问用户下一步**

```
AskUserQuestion:
  questions:
    - question: "编码方案已完成。下一步？"
      header: "继续"
      options:
        - label: "开始编码实现"
          description: "技能结束，Claude 自动开始实现代码"
        - label: "修改编码方案"
          description: "返回修改编码方案"
        - label: "返回修改架构方案"
          description: "返回修改架构方案（会影响编码方案）"
        - label: "暂不开发"
          description: "技能结束，保留已下载的内容和方案"
```

### Step 7: 开始编码实现

使用 AskUserQuestion 让用户选择：

| 选项 | 说明 |
|------|------|
| 是，开始编码 | 技能结束，Claude 自动开始实现代码 |
| 修改编码方案 | 返回修改方案 |
| 暂不开发 | 技能结束，保留已下载的内容和方案 |

## 输出标准

### 必须输出

1. **环境检测结果** - 显示使用的运行时（Java/Python）
2. **配置确认信息** - 包含配置来源和存储目录
3. **下载结果** - 文件路径、附件数量
4. **架构方案文档** - Markdown 格式，保存在工作区根目录
5. **架构方案评审报告**（如有） - 3个角度的评审结果
6. **编码方案文档**（如有） - Markdown 格式，保存在工作区根目录
7. **编码方案评审报告**（如有） - 3个角度的评审结果

### 文件结构

```
{workspace}/
├── .chandao/
│   └── config.properties          # 工作区配置（可选）
├── story_38817_架构方案.md        # 架构方案文档
├── story_38817_架构方案_评审.md   # 架构方案评审报告（如有）
├── story_38817_编码方案.md        # 编码方案文档
├── story_38817_编码方案_评审.md   # 编码方案评审报告（如有）
├── story/                         # 禅道内容目录
│   └── 38817-需求标题.md
└── attachments/                   # 附件目录
    └── story/38817/
```

## 注意事项

1. **跨平台兼容** - 支持 Windows/macOS/Linux
2. **运行时优先级** - Java > Python（两者都可用时）
3. **配置优先级** - 工作区配置 > 全局配置
4. **质量评审可选** - 用户可选择启用或跳过自动评审
5. **主动沟通** - 方案设计中有疑问必须主动询问

## 相关资源

- `{SKILL_DIR}/scripts/chandao-fetch.jar` - Java 版内置工具
- `{SKILL_DIR}/scripts/chandao_fetch/` - Python 版内置工具
- `{SKILL_DIR}/assets/tech_plan_template.md` - 技术方案模板
- `{SKILL_DIR}/references/java_project_guide.md` - Java 项目分析指南
- `{SKILL_DIR}/references/react_project_guide.md` - React 项目分析指南

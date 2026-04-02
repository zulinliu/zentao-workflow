# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## 项目说明

这是一个 Claude Code Skill 项目，用于自动化禅道需求/任务/Bug 下载与技术实现方案设计。

## 版本信息

- **版本**: 1.6.0
- **作者**: liuzl
- **许可证**: MIT

## 开发命令

### Java 版本构建

```bash
# 在 scripts/java-src 目录中执行
cd scripts/java-src
mvn clean package -DskipTests

# 复制 JAR 到 scripts 目录
cp target/chandao-fetch.jar ../
```

### Python 版本测试

```bash
cd scripts
pip install -r requirements.txt
python3 chandao_fetch.py -t bug -i 66445 -o /tmp/test-output
python3 chandao_fetch.py -t story -i 39382 -o /tmp/test-output
python3 chandao_fetch.py -t task -i 61215 -o /tmp/test-output
```

## 架构说明

### 技能执行流程（SKILL.md v1.5.0）

1. **Step 1: 环境检测** - 检测 Java/Python 和 superpowers 技能依赖
2. **Step 2: 配置初始化** - 检查配置文件，引导用户创建
3. **Step 3: 下载内容** - 调用内置工具下载需求/任务/Bug 及附件
4. **Step 4: 技术实现方案设计** - 调用 superpowers:brainstorming 生成方案
5. **Step 5: 输出方案** - 展示方案摘要
6. **Step 6: 开始编码** - 调用 superpowers:subagent-driven-development 或 executing-plans

### v1.5.0 核心变更

| 指标 | v1.4.x | v1.5.0 | 提升 |
|------|--------|--------|------|
| 设计阶段 | 3 个（架构+输出+编码） | 1 个（技术实现方案） | -67% |
| 代理数量 | 12-17 个 | 1-2 个 | -85%+ |
| 简单需求耗时 | 20+ 分钟 | 5-8 分钟 | -70%+ |

### Python 模块架构

```
scripts/chandao_fetch/
├── __main__.py    # CLI 入口
├── config.py      # 配置管理（读取 ~/.chandao/config.properties）
├── client.py      # API 客户端（只读操作，禁止写操作）
├── models.py      # 数据模型（Story/Task/Bug/Attachment）
├── service.py     # 业务逻辑（下载+附件处理）
└── exporter.py    # Markdown 导出（处理图片路径转换）
```

**安全约束**: ChandaoClient 只支持只读操作（登录、查看、下载），禁止创建/更新/删除。

## 关键技术点

### 附件路径处理

- MD 文件位置: `{output}/{type}/{id}-title.md`
- 附件目录: `{output}/attachments/{type}/{id}/`
- **相对路径**: `../attachments/{type}/{id}/filename`

### 内嵌图片下载

- 从内容中提取 `<img src="...">` 标签
- 自动下载图片到附件目录
- 转换为 Markdown 格式: `![](../attachments/...)`

### 配置文件

- 位置: `~/.chandao/config.properties`
- 格式: Java Properties
- 优先级: 命令行 > 配置文件 > 默认值

## 修改 SKILL.md 注意事项

1. **触发条件**在 YAML frontmatter 的 `description` 字段
2. **步骤编号**保持连续（Step 1, Step 2...）
3. **占位符**使用 `{变量名}` 格式
4. **示例**使用通用值，不要包含真实敏感信息

## 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 下载失败 | 网络问题 | 检查禅道服务器是否可达 |
| 登录失败 | 账号密码错误 | 检查配置文件中的凭据 |
| ID 不存在 | 无权限或已删除 | 确认 ID 正确且有访问权限 |
| 附件下载失败 | 权限不足 | 检查输出目录写入权限 |
| superpowers 未安装 | 新环境 | 执行 `claude plugins add official superpowers` |

## 项目管理规范

> 详细规范见 [CONTRIBUTING.md](CONTRIBUTING.md)

### 分支策略

| 分支 | 用途 | 约束 |
|------|------|------|
| `main` | 生产分支 | 仅接受来自 dev 的 PR，合并后自动发版 |
| `dev` | 开发分支 | 日常开发在此进行 |

### 开发流程

```
feature/xxx → dev → (评审通过) → main → (自动发版)
```

### 关键约束

1. **CLAUDE.md 等开发文件** → 只提交到 dev，**禁止合并到 main**
2. **版本号管理** → 遵循语义化版本（SemVer），修改 VERSION 文件
3. **CHANGELOG** → 每次发版必须更新
4. **提交消息** → 使用规范格式：`feat:` / `fix:` / `docs:` / `release:`

### 发版检查清单

- [ ] VERSION 文件已更新
- [ ] CHANGELOG.md 已更新
- [ ] README.md 版本徽章已更新
- [ ] SKILL.md 版本号已更新
- [ ] 代码已评审通过
- [ ] 从 dev 合并到 main（自动触发发版）

## 提交规范

```bash
git commit -m "feat: 功能描述"   # 功能更新
git commit -m "fix: 修复描述"    # 问题修复
git commit -m "docs: 文档描述"   # 文档更新
git commit -m "release: v1.5.0"  # 版本发布
```

## 依赖说明

### 运行时依赖

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Java | 8+ | 优先使用 |
| Python | 3.6+ | 默认备选 |
| superpowers 插件 | 5.0.6+ | v1.5.0 技术方案设计必需 |

### 安装 superpowers

```bash
claude plugins add official superpowers
```

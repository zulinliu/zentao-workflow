# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## 项目说明

这是一个 Claude Code Skill 项目，用于自动化禅道需求/任务/Bug 下载与开发技术方案设计。

## 版本信息

- **版本**: 1.0.0
- **作者**: liuzl
- **许可证**: MIT

## 目录结构

```
zentao-workflow/
├── SKILL.md              # 技能主文件（核心逻辑）
├── README.md             # 用户使用说明
├── LICENSE               # MIT 许可证
├── CHANGELOG.md          # 变更日志
├── VERSION               # 版本号
├── .gitignore
├── scripts/              # 内置工具
│   ├── chandao-fetch.jar     # Java 版本
│   ├── chandao_fetch.py      # Python 入口
│   ├── chandao_fetch/        # Python 模块
│   └── requirements.txt
├── assets/               # 模板资源
│   ├── config_template.properties
│   └── tech_plan_template.md
└── references/           # 参考文档
    ├── java_project_guide.md
    └── react_project_guide.md
```

## 开发命令

### Java 版本构建

```bash
# 在源项目目录执行
cd /home/liuzl/agent/tsintergy-chandao-fetch
mvn clean package -DskipTests

# 复制 JAR 到 skill 目录
cp target/chandao-fetch.jar /path/to/zentao-workflow/scripts/
```

### Python 版本测试

```bash
cd scripts
python3 chandao_fetch.py -t bug -i 66445 -o /tmp/test-output
```

## 关键技术点

### 1. 附件路径处理

- MD 文件位置: `{output}/{type}/{id}-title.md`
- 附件目录: `{output}/attachments/{type}/{id}/`
- **相对路径**: `../attachments/{type}/{id}/filename`

### 2. 内嵌图片下载

- 从内容中提取 `<img src="...">` 标签
- 自动下载图片到附件目录
- 转换为 Markdown 格式: `![](../attachments/...)`

### 3. 配置文件

- 位置: `~/.chandao/config.properties`
- 格式: Java Properties
- 优先级: 命令行 > 配置文件 > 默认值

## 修改 SKILL.md 注意事项

1. **触发条件**在 YAML frontmatter 的 `description` 字段
2. **步骤编号**保持连续（Step 1, Step 2...）
3. **占位符**使用 `{变量名}` 格式
4. **示例**使用通用值，不要包含真实敏感信息

## 提交规范

```bash
# 功能更新
git commit -m "feat: 功能描述"

# 问题修复
git commit -m "fix: 修复描述"

# 文档更新
git commit -m "docs: 文档描述"

# 版本发布
git commit -m "release: v1.0.0"
```

## 测试验证

修改后需要测试：
1. Java 版本下载功能
2. Python 版本下载功能
3. 附件和图片下载
4. 技术方案生成

# 禅道数据抓取工具 (Chandao Fetch)

从禅道系统下载任务、需求、Bug 详情到本地 Markdown 文件，支持图片和附件自动下载。

## 功能特性

- 支持下载需求、任务、Bug 详情
- 自动下载图片和附件
- 输出标准 Markdown 格式
- 支持单个 ID、批量 ID 下载
- 配置自动保存，一次配置永久使用
- 跨平台支持（Windows/macOS/Linux）

## 环境要求

- JDK 8 或更高版本
- 网络可访问禅道服务器

## 安装

### 方式一：直接下载

从 [Releases](https://github.com/zulinliu/tsintergy-chandao-fetch/releases) 页面下载最新版本。

### 方式二：自行编译

```bash
git clone https://github.com/zulinliu/tsintergy-chandao-fetch.git
cd tsintergy-chandao-fetch
mvn clean package
```

编译完成后，在 `target/` 目录下找到 `chandao-fetch.jar`。

## 快速开始

### 第一步：初始化配置

首次使用需要提供禅道地址和账号信息。有两种方式：

**方式一：命令行参数（推荐首次使用）**

```bash
java -jar chandao-fetch.jar \
  --url https://your-zentao-server.com \
  --username your_username \
  --password your_password \
  -t story -i 12345
```

配置将自动保存到 `~/.chandao/config.properties`，后续使用无需再次输入。

**方式二：手动创建配置文件**

在用户目录创建 `~/.chandao/config.properties`：

```properties
zentao.url=https://your-zentao-server.com
zentao.username=your_username
zentao.password=your_password
output.dir=~/chandao
```

### 第二步：下载数据

```bash
# 下载单个需求
java -jar chandao-fetch.jar -t story -i 38817

# 下载多个需求
java -jar chandao-fetch.jar -t story --ids 38817,38818,38819

# 下载任务
java -jar chandao-fetch.jar -t task -i 12345

# 下载 Bug
java -jar chandao-fetch.jar -t bug -i 67890
```

## 命令行参数详解

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--url` | `-u` | 禅道服务器地址 | `--url https://zentao.example.com` |
| `--username` | | 登录用户名 | `--username admin` |
| `--password` | | 登录密码 | `--password 123456` |
| `--output` | `-o` | 输出目录 | `--output ~/my-chandao` |
| `--type` | `-t` | 数据类型 | `-t story` / `-t task` / `-t bug` |
| `--id` | `-i` | 单个 ID | `-i 38817` |
| `--ids` | | 批量 ID，逗号分隔 | `--ids 38817,38818,38819` |
| `--config` | | 指定配置文件路径 | `--config /path/to/config.properties` |
| `--no-attachment` | | 不下载附件 | |
| `--no-image` | | 不下载图片 | |
| `--verbose` | `-v` | 详细输出 | |
| `--help` | `-h` | 显示帮助 | |

## 输出文件结构

```
~/chandao/
├── story/                          # 需求目录
│   ├── 38817-需求标题.md           # 格式：ID-标题.md
│   └── 38818-另一个需求.md
├── task/                           # 任务目录
│   └── 12345-任务名称.md
├── bug/                            # Bug 目录
│   └── 67890-Bug标题.md
└── attachments/                    # 附件目录
    ├── story/
    │   └── 38817/
    │       ├── screenshot.png
    │       └── document.pdf
    ├── task/
    └── bug/
```

## Markdown 文件格式

生成的 Markdown 文件格式如下：

```markdown
# 【需求标题】38817

> 类型: 需求

## 基本信息

| 字段 | 值 |
|------|----|
| 状态 | active |
| 阶段 | wait |
| 优先级 | 1 |
| 创建人 | zhangsan |
| 创建时间 | 2026-03-21 10:00:00 |
| 指派给 | lisi |

## 需求描述

需求详细内容...

## 附件

- [文档.pdf](attachments/38817/document.pdf)

![截图](attachments/38817/screenshot.png)
```

## 配置文件说明

配置文件位于 `~/.chandao/config.properties`：

```properties
# 禅道服务器地址（必填）
zentao.url=https://your-zentao-server.com

# 登录用户名（必填）
zentao.username=your_username

# 登录密码（必填）
zentao.password=your_password

# 输出目录（可选，默认 ~/chandao）
output.dir=~/chandao
```

## 常见问题

### Q: 提示"禅道配置未初始化"？

首次使用需要提供禅道地址、用户名和密码：

```bash
java -jar chandao-fetch.jar \
  --url https://your-zentao-server.com \
  --username your_username \
  --password your_password \
  -t story -i 1
```

### Q: 连接超时怎么办？

1. 检查网络是否能访问禅道服务器
2. 如果是内网地址，确保 VPN 已连接
3. 尝试在浏览器中访问禅道地址确认可用

### Q: 登录失败？

1. 确认用户名和密码正确
2. 检查账号是否被锁定
3. 尝试在浏览器中登录确认账号可用

### Q: 如何修改已保存的配置？

编辑 `~/.chandao/config.properties` 文件，或使用命令行参数覆盖：

```bash
java -jar chandao-fetch.jar --url https://new-server.com --username newuser --password newpass -t story -i 1
```

新配置会自动保存。

## 技术栈

- JDK 8
- OkHttp 4.x（HTTP 客户端）
- Jackson 2.x（JSON 解析）
- JCommander 1.x（命令行解析）
- SLF4J + Logback（日志）

## 开发

```bash
# 编译
mvn clean compile

# 运行测试
mvn test

# 打包
mvn clean package

# 跳过测试打包
mvn clean package -DskipTests
```

## License

MIT
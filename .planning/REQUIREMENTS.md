# Requirements: Worklet v2.0.0

**Defined:** 2026-04-04
**Core Value:** 让开发者从需求到代码一键启动——无论需求来自禅道系统还是本地文档

## v1 Requirements

Requirements for v2.0.0 release. Each maps to roadmap phases.

### Foundation (FOUND)

- [ ] **FOUND-01**: 项目全量重命名 chandao_fetch → worklet，包括包名、类名、文件夹、配置键名
- [x] **FOUND-02**: 删除 Java 版本：chandao-fetch.jar、java-src/ 目录、所有 Java 相关引用
- [x] **FOUND-03**: Python 版本要求提升到 3.10+，更新 CLAUDE.md 和 README
- [ ] **FOUND-04**: 数据模型重构：Worklet/RawContent/Attachment dataclass，BaseSource/BaseReader ABC
- [ ] **FOUND-05**: WorkletConfig 替代 ChandaoConfig，配置目录 .worklet/（项目根优先 → ~/.worklet/）
- [ ] **FOUND-06**: 配置文件写入权限 0600，防止密码泄露
- [x] **FOUND-07**: .worklet/ 自动加入 .gitignore，防止密码误提交
- [x] **FOUND-08**: .gitignore 更新（chandao-data → worklet 相关路径）
- [x] **FOUND-09**: .release-ignore 更新（移除 Java 相关路径和注释）
- [ ] **FOUND-10**: .claude/settings.local.json 清理旧的 Java 复制权限规则
- [x] **FOUND-11**: scripts/requirements.txt 更新（新依赖 + requests>=2.32.0 + 注释重命名）
- [ ] **FOUND-12**: scripts/chandao_fetch.py 入口文件重命名为 worklet.py
- [ ] **FOUND-13**: 清理 __pycache__/ 编译缓存
- [ ] **FOUND-14**: 下载输出目录统一到 .worklet/ 下（story/task/bug/files/attachments）
- [ ] **FOUND-15**: __init__.py 版本号同步更新为 2.0.0
- [x] **FOUND-16**: 新建 pyproject.toml 管理依赖和项目元数据（替代裸 requirements.txt）

### Multi-Source Input (INPUT)

- [ ] **INPUT-01**: BaseSource ABC 定义统一 fetch() 接口，SourceRegistry 自动发现机制
- [x] **INPUT-02**: ZentaoSource 替代现有 client.py + service.py，保持禅道 API 读取能力
- [ ] **INPUT-03**: FileSource 支持读取本地文件，自动识别格式（MD/PDF/DOCX/图片）
- [ ] **INPUT-04**: FolderSource 支持递归扫描文件夹，聚合多文件需求
- [x] **INPUT-05**: MarkdownReader 读取 .md/.txt 文件
- [ ] **INPUT-06**: PdfReader 使用 pypdf 读取 PDF（lazy import，可选依赖）
- [ ] **INPUT-07**: DocxReader 使用 python-docx 读取 Word（lazy import，可选依赖）
- [ ] **INPUT-08**: ImageReader 将图片复制到工作区，生成 Markdown 引用供 Claude 多模态识别
- [ ] **INPUT-09**: InputParser 自动检测输入类型（文件夹 > 文件 > 禅道 ID）

### Client Fixes (CLIENT)

- [ ] **CLIENT-01**: download_attachment/download_image 添加 timeout 参数
- [x] **CLIENT-02**: 大文件流式下载（stream=True + 原子写入 .tmp → rename）
- [ ] **CLIENT-03**: 通用 Exception 替换为具体异常类型（ConnectionError/ValueError 等）
- [ ] **CLIENT-04**: service.py 移除无用 re.findall() 调用
- [ ] **CLIENT-05**: 子任务检测逻辑从 SKILL.md 下沉到 Python 代码层

### Exporter Rewrite (EXPORT)

- [ ] **EXPORT-01**: HTML→Markdown 转换用 markdownify 替代 40+ 正则链
- [ ] **EXPORT-02**: 文件名截断逻辑优化（哈希替代简单截断，避免重名）
- [ ] **EXPORT-03**: Exporter 接受统一 Worklet 模型，不再直接依赖 Story/Task/Bug

### Environment & Config (ENV)

- [x] **ENV-01**: 环境检测优化：先试后检（直接运行工具，失败再检测安装）
- [x] **ENV-02**: 环境检测缓存：成功后写入 .worklet/config.properties 标记，24h TTL
- [x] **ENV-03**: superpowers 安装方式升级为 npx，检测用 capability-based 方式
- [x] **ENV-04**: 移除 Java 环境检测，仅保留 Python

### Trigger & SKILL (SKILL)

- [x] **SKILL-01**: SKILL.md 全面重写：新名称、新流程、新触发词
- [x] **SKILL-02**: description 单行 <250 字符，英文优先 + 命令式语气
- [x] **SKILL-03**: 触发词改为通用开发关键词（开发需求/优化功能/修复bug/重构/开发/优化等）
- [x] **SKILL-04**: 所有路径变量改用 ${CLAUDE_SKILL_DIR}
- [x] **SKILL-05**: 需求入口主动询问用户来源（禅道 API / 本地文件）

### Testing (TEST)

- [x] **TEST-01**: pytest 测试框架搭建（conftest.py、fixtures）
- [x] **TEST-02**: WorkletConfig 单元测试（加载/保存/校验/权限）
- [x] **TEST-03**: ZentaoSource 单元测试（登录/获取/下载，mock API）
- [x] **TEST-04**: Exporter 单元测试（HTML→MD 转换，各种边界情况）
- [x] **TEST-05**: InputParser 单元测试（类型自动检测）
- [x] **TEST-06**: Reader 单元测试（MD/PDF/DOCX/Image 读取）

### Documentation (DOC)

- [x] **DOC-01**: CLAUDE.md 全面更新（新项目名、新架构说明、新开发命令）
- [x] **DOC-02**: CONTRIBUTING.md 更新（移除 Java 构建说明、更新开发流程）
- [ ] **DOC-03**: assets/config_template.properties 重命名键名（zentao → worklet 格式）
- [x] **DOC-04**: assets/tech_plan_template.md 更新为源无关格式（不假设禅道特有字段）
- [x] **DOC-05**: references/ 目录审查（保留通用指南，移除或更新 Java 专属内容）

### Release (REL)

- [ ] **REL-01**: VERSION 更新为 2.0.0，全文档版本号同步
- [ ] **REL-02**: CHANGELOG.md 更新 v2.0.0 完整变更记录
- [ ] **REL-03**: README.md 全面重写（新名称 Worklet、新功能、新安装说明）
- [ ] **REL-04**: release.yml CI/CD 更新（移除 Java 相关、更新目录结构和产物名称）
- [ ] **REL-05**: GitHub 仓库重命名为 worklet

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Extended Sources

- **ESRC-01**: URL 网页读取（WebFetch 集成）
- **ESRC-02**: 剪贴板内容读取
- **ESRC-03**: 其他 PM 工具适配（Jira/GitHub Issues/Linear）

### Performance

- **PERF-01**: 并发附件下载（ThreadPoolExecutor）
- **PERF-02**: 下载进度条显示
- **PERF-03**: 断点续传支持

### Advanced

- **ADV-01**: Spec-driven 三文件方案格式（requirements.md + design.md + tasks.md）
- **ADV-02**: 智能内容缓存（已下载内容跳过重复获取）
- **ADV-03**: 项目级批量下载

## Out of Scope

| Feature | Reason |
|---------|--------|
| v1.x 旧配置兼容（.chandao/） | 大版本升级，不做向后兼容 |
| Java 版本维护 | v2.0 彻底移除 |
| 禅道写操作（创建/更新/删除） | 安全约束，只读 |
| 实时同步/Webhook | 超出 Skill 工具定位 |
| GUI 界面 | CLI Skill 定位 |
| 内置 OCR（pytesseract/EasyOCR） | Claude 多模态视觉足够，OCR 库 2GB+ 太重 |
| 旧版 .doc 格式支持 | python-docx 仅支持 .docx，.doc 格式稀少 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| FOUND-01 | Phase 1 | Pending |
| FOUND-02 | Phase 1 | Complete |
| FOUND-03 | Phase 1 | Complete |
| FOUND-04 | Phase 1 | Pending |
| FOUND-05 | Phase 1 | Pending |
| FOUND-06 | Phase 1 | Pending |
| FOUND-07 | Phase 1 | Complete |
| FOUND-08 | Phase 1 | Complete |
| FOUND-09 | Phase 1 | Complete |
| FOUND-10 | Phase 1 | Pending |
| FOUND-11 | Phase 1 | Complete |
| FOUND-12 | Phase 1 | Pending |
| FOUND-13 | Phase 1 | Pending |
| FOUND-14 | Phase 1 | Pending |
| FOUND-15 | Phase 1 | Pending |
| FOUND-16 | Phase 1 | Complete |
| DOC-03 | Phase 1 | Pending |
| INPUT-01 | Phase 2 | Pending |
| INPUT-02 | Phase 2 | Complete |
| INPUT-05 | Phase 2 | Complete |
| CLIENT-01 | Phase 2 | Pending |
| CLIENT-02 | Phase 2 | Complete |
| CLIENT-03 | Phase 2 | Pending |
| CLIENT-04 | Phase 2 | Pending |
| CLIENT-05 | Phase 2 | Pending |
| EXPORT-01 | Phase 2 | Pending |
| EXPORT-02 | Phase 2 | Pending |
| EXPORT-03 | Phase 2 | Pending |
| INPUT-03 | Phase 3 | Pending |
| INPUT-04 | Phase 3 | Pending |
| INPUT-06 | Phase 3 | Pending |
| INPUT-07 | Phase 3 | Pending |
| INPUT-08 | Phase 3 | Pending |
| TEST-01 | Phase 3 | Complete |
| TEST-02 | Phase 3 | Complete |
| TEST-03 | Phase 3 | Complete |
| TEST-04 | Phase 3 | Complete |
| TEST-05 | Phase 3 | Complete |
| TEST-06 | Phase 3 | Complete |
| INPUT-09 | Phase 4 | Pending |
| ENV-01 | Phase 4 | Complete |
| ENV-02 | Phase 4 | Complete |
| ENV-03 | Phase 4 | Complete |
| ENV-04 | Phase 4 | Complete |
| SKILL-01 | Phase 5 | Complete |
| SKILL-02 | Phase 5 | Complete |
| SKILL-03 | Phase 5 | Complete |
| SKILL-04 | Phase 5 | Complete |
| SKILL-05 | Phase 5 | Complete |
| DOC-01 | Phase 5 | Complete |
| DOC-02 | Phase 5 | Complete |
| DOC-04 | Phase 5 | Complete |
| DOC-05 | Phase 5 | Complete |
| REL-01 | Phase 5 | Pending |
| REL-02 | Phase 5 | Pending |
| REL-03 | Phase 5 | Pending |
| REL-04 | Phase 5 | Pending |
| REL-05 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 58 total
- Mapped to phases: 58
- Unmapped: 0

---
*Requirements defined: 2026-04-04*
*Last updated: 2026-04-04 after roadmap creation*

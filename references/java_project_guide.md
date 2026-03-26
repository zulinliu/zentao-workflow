# Java 项目分析指南

本文档指导如何分析 Java 项目以便设计开发技术方案。

## 分析流程

### Step 1: 快速了解项目

```bash
# 检查项目类型
ls -la                    # 查看根目录结构
cat pom.xml | head -50    # 查看 Maven 配置
find . -name "*.java" | head -20  # 查看代码结构
```

### Step 2: 技术栈识别

从 pom.xml 识别核心依赖：

| 依赖关键字 | 技术栈 |
|-----------|-------|
| spring-boot-starter | Spring Boot |
| mybatis-spring-boot-starter | MyBatis |
| spring-boot-starter-data-jpa | JPA/Hibernate |
| knife4j/springfox-swagger | API 文档 |
| lombok | 代码简化 |
| mapstruct | 对象映射 |
| hutool | 工具库 |
| easyexcel | Excel 处理 |
| jjwt | JWT 认证 |
| shiro-spring | Shiro 权限 |
| spring-boot-starter-security | Spring Security |

## 项目结构识别

### 标准 Maven 项目

```
project/
├── pom.xml                    # Maven 配置
├── src/
│   ├── main/
│   │   ├── java/             # 源代码
│   │   └── resources/        # 资源文件
│   └── test/
│       ├── java/             # 测试代码
│       └── resources/        # 测试资源
└── target/                    # 构建输出
```

### 多模块项目

```
project/
├── pom.xml                    # 父 POM
├── module-common/             # 公共模块
│   └── pom.xml
├── module-api/                # API 模块
│   └── pom.xml
├── module-service/            # 业务模块
│   └── pom.xml
└── module-web/                # Web 模块
    └── pom.xml
```

### 分层架构识别

```
com.company.project/
├── controller/        # API 层 - 处理 HTTP 请求
├── service/           # 业务逻辑层
│   └── impl/          # Service 实现
├── mapper/            # MyBatis Mapper (或 repository/ JPA)
├── entity/            # 数据库实体 (或 model/domain/)
├── dto/               # 数据传输对象
│   ├── request/       # 请求 DTO
│   └── response/      # 响应 DTO
├── config/            # 配置类
├── util/              # 工具类
├── exception/         # 自定义异常
├── aspect/            # AOP 切面
└── enums/             # 枚举类
```

## 关键分析点

### 1. pom.xml 分析重点

```xml
<!-- 项目坐标 -->
<groupId>com.company</groupId>      # 包命名规范
<artifactId>project-name</artifactId>
<version>1.0.0</version>

<!-- 核心依赖 -->
<dependencies>
    <!-- 识别使用的技术栈 -->
    - Spring Boot 版本?
    - ORM 框架 (MyBatis/JPA)?
    - 数据库驱动 (MySQL/PostgreSQL/Oracle)?
    - 缓存 (Redis)?
    - 消息队列 (RabbitMQ/Kafka)?
</dependencies>

<!-- 构建配置 -->
<build>
    <plugins>
        - maven-compiler-plugin: Java 版本
        - maven-shade-plugin/assembly-plugin: 打包方式
    </plugins>
</build>
```

### 2. 配置文件分析

**application.yml 分析重点**

```yaml
# 重点关注以下配置
server:
  port: 8080                    # 服务端口
  servlet:
    context-path: /api          # 上下文路径

spring:
  datasource:                   # 数据库配置
    url: jdbc:mysql://...
    driver-class-name: ...
  jpa:                          # JPA 配置
    hibernate:
      ddl-auto: ...
  mybatis:                      # MyBatis 配置
    mapper-locations: ...
  redis:                        # Redis 配置
    host: ...
  mvc:                          # MVC 配置
    pathmatch:
      matching-strategy: ant_path_matcher  # Swagger 兼容

# 自定义配置 (业务相关)
app:
  xxx: ...
```

### 3. 代码风格识别

| 特征 | 说明 |
|-----|------|
| @Data, @Builder, @Slf4j | 使用 Lombok |
| 构造器注入 (@RequiredArgsConstructor) | 推荐的依赖注入方式 |
| @Transactional | 事务管理方式 |
| 全局异常处理器 (@ControllerAdvice) | 统一异常处理 |
| Result/Response<T> 统一响应 | API 响应规范 |
| BaseXxx 基类 | 代码复用模式 |

### 4. 数据库设计分析

```bash
# 查找数据库相关文件
find . -name "*.sql"           # SQL 脚本
find . -name "*Mapper.xml"     # MyBatis Mapper XML
find . -path "*/entity/*"      # 实体类
```

实体类分析重点：
- @TableName / @Table 注解 → 表名
- 字段类型 → 数据库字段
- @OneToMany / @ManyToOne → 关联关系

## 新功能开发分析清单

当需要开发新功能时，按以下清单分析：

### Step 1: 理解需求

- [ ] 阅读禅道 MD 文件
- [ ] 查看附件中的截图、原型图
- [ ] 理解业务背景和目标

### Step 2: 分析现有代码

- [ ] 找到相关的 Controller (类似功能的 API)
- [ ] 找到相关的 Service (业务逻辑参考)
- [ ] 找到相关的 Entity/Mapper (数据模型参考)
- [ ] 查看是否有可复用的工具类

### Step 3: 确定需要创建的文件

- [ ] Controller 类（API 入口）
- [ ] Service 接口和实现类
- [ ] Mapper/Repository 接口
- [ ] Entity 实体类
- [ ] DTO 类（请求/响应）
- [ ] Mapper XML（MyBatis 项目）

### Step 4: 确定需要修改的文件

- [ ] 现有 Service 类（扩展功能）
- [ ] 配置文件（新增配置项）
- [ ] 全局异常处理器（新增异常类型）
- [ ] 枚举类（新增类型）

### Step 5: 数据库变更

- [ ] 新增表？
- [ ] 修改现有表结构？
- [ ] 新增索引？
- [ ] 数据迁移？

## 技术方案模板 - Java 部分

```markdown
## 技术设计

### API 设计
- 接口路径: POST /api/v1/xxx
- 请求参数: XxxRequest
- 响应结构: Result<XxxResponse>

### 数据模型

#### 新增表: t_xxx
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | BIGINT | 主键 |
| name | VARCHAR(100) | 名称 |
| created_time | DATETIME | 创建时间 |

### 实现方案

#### 1. Controller 层
```java
@RestController
@RequestMapping("/api/v1/xxx")
@RequiredArgsConstructor
public class XxxController {

    private final XxxService xxxService;

    @PostMapping
    public Result<XxxResponse> create(@Valid @RequestBody XxxRequest request) {
        return Result.success(xxxService.create(request));
    }
}
```

#### 2. Service 层
```java
@Service
@RequiredArgsConstructor
public class XxxServiceImpl implements XxxService {

    private final XxxMapper xxxMapper;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public XxxResponse create(XxxRequest request) {
        // 1. 参数校验
        // 2. 业务逻辑
        // 3. 数据持久化
        // 4. 返回结果
    }
}
```

#### 3. Mapper 层 (MyBatis)
```java
@Mapper
public interface XxxMapper {
    int insert(XxxEntity entity);
    XxxEntity selectById(Long id);
}
```

#### 4. 实体类
```java
@Data
@TableName("t_xxx")
public class XxxEntity {
    @TableId(type = IdType.AUTO)
    private Long id;
    private String name;
    private LocalDateTime createdTime;
}
```
```

## 常见问题

### 如何判断使用 MyBatis 还是 JPA？

| 特征 | 技术 |
|-----|------|
| XML mapper 文件 | MyBatis |
| @Mapper 注解 | MyBatis |
| Repository 继承 JpaRepository | JPA |
| @Entity + @Column 注解 | JPA |
| BaseMapper<T> | MyBatis-Plus |

### 如何识别项目是 Spring Boot？

- pom.xml 有 `spring-boot-starter-parent` 或 `spring-boot-dependencies`
- 主类有 `@SpringBootApplication`
- 配置文件是 application.yml/properties
- 有内嵌 Tomcat/Jetty

### 如何找到某个功能的入口？

```bash
# 方法1: 搜索 URL 路径
grep -r "/api/xxx" --include="*.java"

# 方法2: 搜索 Controller
find . -name "*Controller.java"

# 方法3: 搜索 Service 名称
grep -r "XxxService" --include="*.java"
```

## 分析工具推荐

```bash
# 代码结构分析
tree -L 4 -d                    # 目录结构
find . -name "*.java" | wc -l   # 代码文件数

# 依赖分析
mvn dependency:tree             # 依赖树

# 代码搜索
grep -r "关键词" --include="*.java"
```

# React 项目分析指南

本文档指导如何分析 React 项目以便设计开发技术方案。

## 分析流程

### Step 1: 快速了解项目

```bash
# 检查项目类型
ls -la                       # 查看根目录结构
cat package.json             # 查看依赖配置
find src -name "*.tsx" | head -20  # 查看代码结构
```

### Step 2: 技术栈识别

从 package.json 识别核心依赖：

| 依赖关键字 | 技术栈 |
|-----------|-------|
| react / react-dom | React 核心 |
| next / next.js | Next.js 框架 |
| react-router-dom | React Router |
| @tanstack/react-query | React Query |
| axios | HTTP 客户端 |
| antd / ant-design | Ant Design UI |
| @mui/material | Material UI |
| tailwindcss | Tailwind CSS |
| zustand | Zustand 状态管理 |
| @reduxjs/toolkit | Redux Toolkit |
| mobx | MobX 状态管理 |
| formik | Formik 表单 |
| react-hook-form | React Hook Form |
| ahooks | 阿里 Hooks 库 |
| dayjs / moment | 日期处理 |
| echarts / @ant-design/charts | 图表库 |
| ahooks | 阿里业务 Hooks |

## 项目结构识别

### 标准 Create React App 项目

```
project/
├── package.json              # 依赖配置
├── public/
│   └── index.html           # HTML 模板
├── src/
│   ├── index.tsx            # 入口文件
│   ├── App.tsx              # 根组件
│   ├── components/          # 通用组件
│   │   ├── common/          # 基础组件
│   │   └── business/        # 业务组件
│   ├── pages/               # 页面组件
│   ├── hooks/               # 自定义 Hooks
│   ├── services/            # API 服务
│   ├── stores/              # 状态管理
│   ├── utils/               # 工具函数
│   ├── types/               # TypeScript 类型
│   └── styles/              # 样式文件
├── tsconfig.json            # TypeScript 配置
└── vite.config.ts / craco.config.js  # 构建配置
```

### Next.js 项目

```
project/
├── package.json
├── next.config.js           # Next.js 配置
├── app/                     # App Router (Next.js 13+)
│   ├── layout.tsx
│   ├── page.tsx
│   └── (auth)/              # 路由组
├── pages/                   # Pages Router
│   ├── _app.tsx
│   ├── index.tsx
│   └── api/                 # API 路由
├── components/
├── lib/                     # 工具库
└── public/
```

### 企业级项目（Ant Design Pro）

```
project/
├── src/
│   ├── pages/               # 页面
│   │   └── User/
│   │       ├── index.tsx    # 列表页
│   │       ├── detail.tsx   # 详情页
│   │       └── components/  # 页面组件
│   ├── components/          # 全局组件
│   ├── services/            # API
│   ├── models/              # 数据模型
│   ├── stores/              # 状态
│   └── access/              # 权限
```

## 关键分析点

### 1. package.json 分析重点

```json
{
  "scripts": {
    "dev": "vite",           // 开发服务器
    "build": "tsc && vite build",  // 构建
    "lint": "eslint src"     // 代码检查
  },
  "dependencies": {
    // 核心依赖
    "react": "^18.x",
    "react-dom": "^18.x",
    "react-router-dom": "^6.x",    // 路由
    "axios": "^1.x",               // HTTP
    "zustand": "^4.x",             // 状态管理
    "antd": "^5.x",                // UI 组件库
    "@ant-design/pro-components": "^2.x",  // Pro 组件
    "ahooks": "^3.x",              // Hooks
    "dayjs": "^1.x"                // 日期
  },
  "devDependencies": {
    "typescript": "^5.x",
    "vite": "^5.x",
    "@types/react": "^18.x"
  }
}
```

### 2. 路由结构分析

**React Router v6**

```tsx
// router/index.tsx
import { createBrowserRouter } from 'react-router-dom';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'users', element: <UserList /> },
      { path: 'users/:id', element: <UserDetail /> },
    ],
  },
]);
```

**查找路由文件**：
```bash
grep -r "createBrowserRouter\|Routes\|Route" --include="*.tsx" src/
```

### 3. 状态管理分析

**Zustand（轻量级推荐）**

```tsx
// stores/userStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UserState {
  user: User | null;
  token: string | null;
  setUser: (user: User) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      setUser: (user) => set({ user }),
      logout: () => set({ user: null, token: null }),
    }),
    { name: 'user-storage' }
  )
);
```

**Redux Toolkit**

```tsx
// stores/index.ts
import { configureStore } from '@reduxjs/toolkit';

export const store = configureStore({
  reducer: {
    user: userReducer,
    // ...
  },
});
```

### 4. API 调用方式分析

**Axios 封装**

```tsx
// services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});

// 请求拦截器
api.interceptors.request.use((config) => {
  const token = useUserStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 响应拦截器
api.interceptors.response.use(
  (res) => res.data,
  (error) => {
    if (error.response?.status === 401) {
      // 跳转登录
    }
    return Promise.reject(error);
  }
);

export default api;
```

**React Query 集成**

```tsx
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { xxxApi } from '../services/xxxApi';

export const useUserList = (params: ListParams) => {
  return useQuery({
    queryKey: ['users', params],
    queryFn: () => xxxApi.getList(params),
  });
};

export const useCreateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: xxxApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};
```

### 5. 组件风格分析

**函数组件 + Hooks（现代风格）**

```tsx
import { useState, useEffect, useCallback } from 'react';
import { Table, Button, Modal, Form, Input } from 'antd';
import { useUserList, useCreateUser } from '../hooks/useUsers';

const UserListPage: React.FC = () => {
  const [params, setParams] = useState({ page: 1, pageSize: 10 });
  const { data, isLoading } = useUserList(params);
  const createMutation = useCreateUser();

  const handleCreate = useCallback(async (values: CreateUserDTO) => {
    await createMutation.mutateAsync(values);
    message.success('创建成功');
  }, []);

  return (
    <div className="page-container">
      <Table
        dataSource={data?.list}
        loading={isLoading}
        rowKey="id"
        columns={columns}
      />
    </div>
  );
};
```

## 新功能开发分析清单

### Step 1: 理解需求

- [ ] 阅读禅道 MD 文件
- [ ] 查看附件中的 UI 原型图、流程图
- [ ] 理解业务背景和目标

### Step 2: 分析现有代码

- [ ] 找到相关的页面组件 (类似功能)
- [ ] 找到相关的 API 服务
- [ ] 查看是否有可复用的组件
- [ ] 理解状态管理方式

### Step 3: 确定需要创建的文件

- [ ] 页面组件（pages/XxxPage.tsx）
- [ ] 业务组件（components/XxxComponent.tsx）
- [ ] API 服务（services/xxxApi.ts）
- [ ] 类型定义（types/xxx.ts）
- [ ] 自定义 Hook（hooks/useXxx.ts）
- [ ] 状态 Store（stores/xxxStore.ts）

### Step 4: 确定需要修改的文件

- [ ] 路由配置（添加新路由）
- [ ] 菜单配置（添加菜单项）
- [ ] 布局组件（如有布局变化）
- [ ] 权限配置（如有权限控制）

## 技术方案模板 - React 部分

```markdown
## 技术设计

### 页面设计
- 路由路径: /xxx
- 页面组件: XxxPage
- 布局: 使用现有 Layout 组件

### 实现方案

#### 1. 类型定义
```typescript
// types/xxx.ts
export interface XxxItem {
  id: number;
  name: string;
  status: 'active' | 'inactive';
  createdAt: string;
}

export interface XxxListParams {
  page: number;
  pageSize: number;
  keyword?: string;
}
```

#### 2. API 服务
```typescript
// services/xxxApi.ts
import api from './api';

export const xxxApi = {
  getList: (params: XxxListParams) =>
    api.get<PageResult<XxxItem>>('/xxx', { params }),

  getById: (id: number) =>
    api.get<XxxItem>(`/xxx/${id}`),

  create: (data: CreateXxxDto) =>
    api.post<XxxItem>('/xxx', data),

  update: (id: number, data: UpdateXxxDto) =>
    api.put<XxxItem>(`/xxx/${id}`, data),

  delete: (id: number) =>
    api.delete(`/xxx/${id}`),
};
```

#### 3. 自定义 Hook
```typescript
// hooks/useXxx.ts
import { useQuery, useMutation } from '@tanstack/react-query';
import { xxxApi } from '../services/xxxApi';

export const useXxxList = (params: XxxListParams) => {
  return useQuery({
    queryKey: ['xxx', params],
    queryFn: () => xxxApi.getList(params),
  });
};
```

#### 4. 页面组件
```tsx
// pages/XxxPage.tsx
import { useState } from 'react';
import { Table, Button, Space } from 'antd';
import { useXxxList } from '../hooks/useXxx';

const XxxPage: React.FC = () => {
  const [params, setParams] = useState<XxxListParams>({
    page: 1,
    pageSize: 10,
  });

  const { data, isLoading } = useXxxList(params);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Xxx 管理</h1>
        <Button type="primary">新增</Button>
      </div>
      <Table
        dataSource={data?.list}
        loading={isLoading}
        rowKey="id"
        columns={columns}
        pagination={{
          current: params.page,
          pageSize: params.pageSize,
          total: data?.total,
          onChange: (page, pageSize) => setParams({ ...params, page, pageSize }),
        }}
      />
    </div>
  );
};

export default XxxPage;
```

#### 5. 路由配置
```tsx
// router/routes.ts
import XxxPage from '../pages/XxxPage';

export const routes = [
  // ...
  {
    path: '/xxx',
    element: <XxxPage />,
    meta: { title: 'Xxx 管理', icon: 'TableOutlined' },
  },
];
```
```

## 常见问题

### 如何判断项目使用什么 UI 组件库？

| 依赖 | UI 库 |
|-----|-------|
| antd | Ant Design |
| @mui/material | Material UI |
| @chakra-ui/react | Chakra UI |
| arco-design | Arco Design |
| 无明显依赖 | 可能是 Tailwind 或原生 CSS |

### 如何判断项目是否使用 TypeScript？

- 存在 tsconfig.json
- 文件后缀为 .tsx 或 .ts
- package.json 有 typescript 依赖

### 如何处理受保护的页面？

```tsx
// components/ProtectedRoute.tsx
import { Navigate, useLocation } from 'react-router-dom';
import { useUserStore } from '../stores/userStore';

export const ProtectedRoute: React.FC<PropsWithChildren> = ({ children }) => {
  const { user } = useUserStore();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

// 使用
<Route path="/dashboard" element={
  <ProtectedRoute>
    <Dashboard />
  </ProtectedRoute>
} />
```

### 如何查找某个功能的入口？

```bash
# 方法1: 搜索 URL 路径
grep -r "/api/xxx" --include="*.ts" src/

# 方法2: 搜索页面名称
grep -r "Xxx管理\|Xxx列表" --include="*.tsx" src/

# 方法3: 搜索路由配置
find src -name "*route*" -o -name "*router*"
```

## 分析工具推荐

```bash
# 代码结构分析
tree -L 4 -d src/           # 目录结构
find src -name "*.tsx" | wc -l  # 组件数量

# 依赖分析
npm list --depth=0          # 直接依赖

# 代码搜索
grep -r "关键词" --include="*.tsx" src/
grep -r "关键词" --include="*.ts" src/
```

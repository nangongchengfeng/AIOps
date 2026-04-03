# AIOps 前端

基于 Vue 3 + Vite + TypeScript 的 AIOps 智能运维平台前端。

## 技术栈

- Vue 3 (Composition API + `<script setup>`)
- Vite 5
- TypeScript
- Vue Router 4
- Pinia
- ECharts 5
- lucide-vue-next (图标库)
- Axios

## 设计理念

采用 **有机形态设计** 风格：
- 多值不对称圆角
- 缓慢形变的 blob 装饰元素
- 粉紫青绿柔和渐变
- 平稳流畅的动效

## 快速开始

### 安装依赖

```bash
cd frontend
npm install
```

### 开发模式

```bash
npm run dev
```

前端将在 `http://localhost:3000` 启动。

### 构建生产版本

```bash
npm run build
```

### 预览构建结果

```bash
npm run preview
```

## 项目结构

```
frontend/
├── src/
│   ├── api/           # API 接口
│   │   └── index.ts
│   ├── components/    # 通用组件
│   │   ├── AppLayout.vue
│   │   ├── Badge.vue
│   │   ├── GlobalBlobs.vue
│   │   ├── OrgButton.vue
│   │   ├── OrgCard.vue
│   │   ├── Sidebar.vue
│   │   └── TopBar.vue
│   ├── router/        # 路由配置
│   │   └── index.ts
│   ├── styles/        # 样式文件
│   │   ├── index.css
│   │   ├── theme.css
│   │   └── variables.css
│   ├── types/         # TypeScript 类型
│   │   └── index.ts
│   ├── views/         # 页面组件
│   │   ├── AlertDetail.vue
│   │   ├── Alerts.vue
│   │   ├── Analyses.vue
│   │   └── Dashboard.vue
│   ├── App.vue
│   └── main.ts
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 页面说明

### 1. 仪表盘 (`/dashboard`)
- KPI 数据卡片（总告警数、活跃告警、AI 分析、今日解决）
- 告警趋势图表
- 最新分析记录列表

### 2. 告警管理 (`/alerts`)
- 告警列表（支持状态过滤、分页）
- 查看告警详情
- 状态和严重程度标识

### 3. 告警详情 (`/alerts/:id`)
- 告警基本信息
- 标签和注解
- AI 分析入口
- 分析历史记录
- 分析结果详情弹窗

### 4. AI 分析 (`/analyses`)
- 最新分析记录列表
- 分析结果展示
- 置信度可视化

## API 代理

开发模式下，Vite 会自动代理 `/api` 请求到 `http://localhost:8000`（后端服务）。

可以在 `.env` 文件中配置后端地址：

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 字体

项目使用 Google Fonts：
- Sora（标题、数字）
- DM Sans（正文）
- JetBrains Mono（代码）

请确保网络可以访问 Google Fonts。

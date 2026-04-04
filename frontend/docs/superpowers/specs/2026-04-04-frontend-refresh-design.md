---
title: 前端主题重构设计规范
date: 2026-04-04
type: design
---

# 前端主题重构设计文档

## 概述

本次重构将 AIOps 前端主题从当前的"粉紫有机形态"更新为"清新办公风"，采用浅蓝色+灰白渐变配色，极简规整的设计语言，同时保持现有目录结构不变。

## 设计原则

| 维度 | 选择 |
|------|------|
| **主题风格** | 清新办公风（浅蓝色+灰白渐变） |
| **侧边栏** | 半透明毛玻璃效果 |
| **布局** | 保持当前结构（Sidebar + 主内容区） |
| **组件风格** | 极简规整（统一圆角） |
| **重构范围** | 主要更新主题和样式，保持现有目录 |

## 颜色系统

### CSS 变量定义

```css
:root {
  /* 背景层 */
  --bg-base:        #f8fafc;      /* 整体底色 */
  --bg-surface:     #ffffff;      /* 卡片表面 */
  --bg-elevated:    #ffffff;      /* 悬浮层 */

  /* 主色调 — 清新蓝白 */
  --color-primary:       #5b9bd5;  /* 主色 */
  --color-primary-light: #8ecae6;  /* 浅蓝 */
  --color-primary-dark:  #2e77c2;  /* 深蓝 */

  /* 辅助色 */
  --color-teal:     #67c8c5;
  --color-soft:     #a8d5e8;

  /* 状态色（清新版） */
  --color-success:  #51cf66;
  --color-warning:  #f59f00;
  --color-error:    #ff6b6b;
  --color-info:     #5b9bd5;

  /* 文字 */
  --text-primary:   #1e293b;
  --text-secondary: #64748b;
  --text-muted:     #94a3b8;

  /* 渐变预设 */
  --gradient-primary: linear-gradient(135deg, #5b9bd5 0%, #8ecae6 100%);
  --gradient-surface: linear-gradient(160deg, #ffffff 0%, #f8fafc 100%);
  --gradient-sidebar: linear-gradient(180deg, rgba(255,255,255,0.85) 0%, rgba(248,250,252,0.8) 100%);

  /* 阴影（清新蓝调） */
  --shadow-sm:   0 2px 12px rgba(91, 155, 213, 0.08);
  --shadow-md:   0 6px 24px rgba(91, 155, 213, 0.12);
  --shadow-lg:   0 12px 40px rgba(91, 155, 213, 0.15);

  /* 圆角（统一规整） */
  --radius-sm:  8px;
  --radius-md:  12px;
  --radius-lg:  16px;
  --radius-xl:  20px;
  --radius-pill: 50px;

  /* 动效时间 */
  --duration-hover:    0.3s;
  --duration-active:   0.15s;
  --duration-enter:    0.4s;
  --easing-smooth:     cubic-bezier(0.4, 0, 0.2, 1);

  /* 字体栈 */
  --font-display: 'Sora', 'PingFang SC', sans-serif;
  --font-body:    'DM Sans', 'PingFang SC', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;

  /* 字号 */
  --text-xs: 11px;
  --text-sm: 13px;
  --text-base: 15px;
  --text-lg: 18px;
  --text-xl: 22px;
  --text-2xl: 28px;
  --text-3xl: 36px;
}
```

## 组件设计规范

### 卡片 (OrgCard)

- **圆角**: `16px` 统一
- **背景**: `var(--gradient-surface)`
- **阴影**: `var(--shadow-md)`
- **边框**: `1px solid rgba(91, 155, 213, 0.1)`
- **Hover 效果**: 上移 `2px`，阴影增强
- **移除**: 有机形态变化、blob 装饰

### 按钮 (OrgButton)

- **主按钮**:
  - 背景: `var(--gradient-primary)`
  - 圆角: `12px`
  - 文字: 白色
  - 阴影: `0 4px 12px rgba(91, 155, 213, 0.3)`

- **次要按钮**:
  - 背景: 透明
  - 边框: `1.5px solid var(--color-primary-light)`
  - 圆角: `10px`
  - 文字: `var(--color-primary)`

### 输入框

- **圆角**: `10px`
- **背景**: `rgba(91, 155, 213, 0.05)`
- **边框**: `1.5px solid rgba(91, 155, 213, 0.18)`
- **Focus**: 边框变为 `var(--color-primary)`，添加蓝色光晕

### 侧边栏 (Sidebar)

- **背景**: `var(--gradient-sidebar)`
- **毛玻璃效果**: `backdrop-filter: blur(20px)`
- **边框**: `1px solid rgba(91, 155, 213, 0.15)`
- **圆角**: `0 24px 20px 0`
- **导航项**:
  - 未选中: `var(--text-secondary)`
  - Hover: 浅蓝背景 `rgba(91, 155, 213, 0.08)`
  - 选中: 蓝色背景渐变 + 左侧蓝色边框

### 全局装饰 (GlobalBlobs)

- **颜色**: 更新为浅蓝色调
- **Blob 1**: 右上 - `rgba(91, 155, 213, 0.15)`
- **Blob 2**: 左下 - `rgba(103, 200, 197, 0.12)`
- **Blob 3**: 中间 - `rgba(142, 202, 230, 0.1)`

## 页面架构

保持现有结构不变：

```
App.vue
├── GlobalBlobs (更新为浅蓝色调)
└── AppLayout
    ├── Sidebar (半透明毛玻璃，浅色系)
    └── MainArea
        └── PageContent (RouterView)
```

## 文件更新清单

### 必须更新

1. `src/styles/variables.css` - 全新颜色系统
2. `src/components/Sidebar.vue` - 毛玻璃效果，浅色主题
3. `src/components/OrgCard.vue` - 统一圆角，移除有机形态
4. `src/components/GlobalBlobs.vue` - 浅蓝色调 blob
5. `src/views/Dashboard.vue` - 图表颜色更新

### 可能需要更新

6. `src/styles/theme.css` - 全局样式适配
7. `src/components/OrgButton.vue` - 按钮样式更新
8. `src/components/Badge.vue` - 徽章颜色更新
9. `src/views/Alerts.vue` - 页面样式适配
10. `src/views/AlertDetail.vue` - 页面样式适配
11. `src/views/Analyses.vue` - 页面样式适配

## 图表配色

ECharts 图表使用新配色：

- **主线条**: `#5b9bd5` → `#8ecae6` 渐变
- **填充区域**: 浅蓝半透明 `rgba(91, 155, 213, 0.2)`
- **数据点**: `#5b9bd5`
- **坐标轴**: 浅灰 `rgba(91, 155, 213, 0.2)`

## 不更改的内容

- 目录结构（保持现有）
- 路由配置
- API 模块结构
- TypeScript 类型定义
- 业务逻辑代码

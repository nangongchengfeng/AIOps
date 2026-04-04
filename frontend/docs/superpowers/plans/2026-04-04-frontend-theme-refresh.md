# 前端主题重构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将前端主题从粉紫有机形态更新为清新办公风（浅蓝色+灰白渐变，极简规整）

**Architecture:** 保持现有目录结构，逐步更新样式文件和组件，每个任务都是独立可验证的

**Tech Stack:** Vue 3 + TypeScript + SCSS + ECharts

---

## 文件结构映射

| 文件 | 操作 | 职责 |
|------|------|------|
| `src/styles/variables.css` | 修改 | 全局 CSS 变量（颜色、圆角、阴影） |
| `src/components/Sidebar.vue` | 修改 | 侧边栏毛玻璃效果和浅色主题 |
| `src/components/OrgCard.vue` | 修改 | 卡片统一圆角，移除有机形态 |
| `src/components/GlobalBlobs.vue` | 修改 | 全局装饰 blob 改为浅蓝色调 |
| `src/views/Dashboard.vue` | 修改 | 仪表盘图表配色更新 |
| `src/components/Badge.vue` | 修改 | 徽章颜色适配新主题 |
| `src/views/Alerts.vue` | 修改 | 告警页面样式适配 |
| `src/views/AlertDetail.vue` | 修改 | 告警详情页面样式适配 |
| `src/views/Analyses.vue` | 修改 | 分析页面样式适配 |

---

### Task 1: 更新全局 CSS 变量

**Files:**
- Modify: `src/styles/variables.css`

**Goal:** 替换所有颜色变量为清新办公风配色

- [ ] **Step 1: 读取现有 variables.css 文件**

```bash
# 已读取，内容见设计文档
```

- [ ] **Step 2: 替换为新的颜色系统**

将整个 `:root` 块替换为：

```css
:root {
  /* 背景层 */
  --bg-base:        #f8fafc;
  --bg-surface:     #ffffff;
  --bg-elevated:    #ffffff;

  /* 主色调 — 清新蓝白 */
  --color-primary:       #5b9bd5;
  --color-primary-light: #8ecae6;
  --color-primary-dark:  #2e77c2;

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

- [ ] **Step 3: 验证文件保存成功**

确认文件已写入，无语法错误

- [ ] **Step 4: 提交**

```bash
cd frontend
git add src/styles/variables.css
git commit -m "style: 更新全局 CSS 变量为清新办公风配色"
```

---

### Task 2: 更新侧边栏为半透明毛玻璃效果

**Files:**
- Modify: `src/components/Sidebar.vue`

**Goal:** 将深色侧边栏改为浅色半透明毛玻璃效果

- [ ] **Step 1: 修改侧边栏背景**

将 `.sidebar` 的 `background` 替换为：

```css
background: var(--gradient-sidebar);
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px);
border-right: 1px solid rgba(91, 155, 213, 0.15);
```

- [ ] **Step 2: 修改侧边栏圆角**

将 `.sidebar` 的 `border-radius` 改为：

```css
border-radius: 0 24px 20px 0;
```

- [ ] **Step 3: 更新 Logo 文字颜色**

将 `.logo-text` 的 `color` 改为：

```css
color: var(--text-primary);
```

- [ ] **Step 4: 更新导航项样式**

将 `.nav-item` 的样式替换为：

```css
.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  border-radius: var(--radius-md);
  transition: all var(--duration-hover) var(--easing-smooth);
  position: relative;
}

.nav-item:hover {
  color: var(--text-primary);
  background: rgba(91, 155, 213, 0.08);
}

.nav-item.active {
  color: var(--color-primary);
  background: linear-gradient(90deg, rgba(91, 155, 213, 0.15), rgba(91, 155, 213, 0.05));
  border-left: 3px solid var(--color-primary);
}
```

- [ ] **Step 5: 更新 Logo 图标背景**

将 `.logo-icon` 的 `background` 保持为 `var(--gradient-primary)`

- [ ] **Step 6: 更新侧边栏装饰 blob**

将 `.sidebar-decoration` 的 `background` 改为：

```css
background: var(--gradient-primary);
opacity: 0.08;
```

- [ ] **Step 7: 提交**

```bash
cd frontend
git add src/components/Sidebar.vue
git commit -m "style: 更新侧边栏为半透明毛玻璃效果"
```

---

### Task 3: 更新卡片组件为统一规整风格

**Files:**
- Modify: `src/components/OrgCard.vue`

**Goal:** 移除有机形态，使用统一圆角

- [ ] **Step 1: 修改卡片基础样式**

将 `.org-card` 样式替换为：

```css
.org-card {
  background: var(--gradient-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: 24px 28px;
  border: 1px solid rgba(91, 155, 213, 0.1);
  transition: transform var(--duration-hover) var(--easing-smooth),
    box-shadow var(--duration-hover) var(--easing-smooth);
  position: relative;
  overflow: hidden;
}
```

- [ ] **Step 2: 移除有机形态变化**

删除以下代码块：

```css
.org-card:nth-child(2n) {
  border-radius: 28px 38px 22px 32px;
}

.org-card:nth-child(3n) {
  border-radius: 36px 22px 38px 18px;
}
```

- [ ] **Step 3: 移除 blob 装饰**

删除整个 `.org-card:not(.no-decoration)::before` 代码块

- [ ] **Step 4: 调整 Hover 效果**

将 `.org-card:hover` 改为：

```css
.org-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

- [ ] **Step 5: 提交**

```bash
cd frontend
git add src/components/OrgCard.vue
git commit -m "style: 卡片组件统一规整风格，移除有机形态"
```

---

### Task 4: 更新全局装饰 Blob 为浅蓝色调

**Files:**
- Modify: `src/components/GlobalBlobs.vue`

**Goal:** 将 blob 颜色从粉紫改为浅蓝

- [ ] **Step 1: 更新 blob-1 颜色**

将 `.blob-1` 的 `background` 改为：

```css
background: radial-gradient(circle, rgba(91, 155, 213, 0.15), transparent 70%);
```

- [ ] **Step 2: 更新 blob-2 颜色**

将 `.blob-2` 的 `background` 改为：

```css
background: radial-gradient(circle, rgba(103, 200, 197, 0.12), transparent 70%);
```

- [ ] **Step 3: 更新 blob-3 颜色**

将 `.blob-3` 的 `background` 改为：

```css
background: radial-gradient(circle, rgba(142, 202, 230, 0.1), transparent 70%);
```

- [ ] **Step 4: 调整模糊度（可选，更柔和）**

将 `.blob` 的 `filter: blur(60px)` 保持不变

- [ ] **Step 5: 提交**

```bash
cd frontend
git add src/components/GlobalBlobs.vue
git commit -m "style: 全局装饰 blob 改为浅蓝色调"
```

---

### Task 5: 更新仪表盘图表配色

**Files:**
- Modify: `src/views/Dashboard.vue`

**Goal:** 更新 ECharts 图表颜色为新主题配色

- [ ] **Step 1: 更新 KPI 卡片图标颜色**

将四个 `.kpi-icon` 的内联样式 `background` 分别改为：

```css
/* 总告警数 - 蓝色 */
background: linear-gradient(135deg, #5b9bd5, #8ecae6);

/* 活跃告警 - 橙色 */
background: linear-gradient(135deg, #f59f00, #ffc078);

/* AI 分析 - 青色 */
background: linear-gradient(135deg, #67c8c5, #a8d5e8);

/* 今日解决 - 绿色 */
background: linear-gradient(135deg, #51cf66, #8ce99a);
```

- [ ] **Step 2: 更新图表配色**

在 `initChart()` 函数中，更新 `option` 对象的颜色：

更新 `tooltip.backgroundColor` 为 `'rgba(255, 255, 255, 0.95)'`

更新 `tooltip.borderColor` 为 `'rgba(91, 155, 213, 0.2)'`

更新 `tooltip.textStyle.color` 为 `'#1e293b'`

更新 `xAxis.axisLine.lineStyle.color` 为 `'rgba(91, 155, 213, 0.2)'`

更新 `xAxis.axisLabel.color` 为 `'#64748b'`

更新 `yAxis.splitLine.lineStyle.color` 为 `'rgba(91, 155, 213, 0.1)'`

更新 `yAxis.axisLabel.color` 为 `'#64748b'`

- [ ] **Step 3: 更新 series 线条渐变**

将 `series[0].lineStyle.color` 改为：

```javascript
color: {
  type: 'linear',
  x: 0, y: 0, x2: 1, y2: 0,
  colorStops: [
    { offset: 0, color: '#5b9bd5' },
    { offset: 1, color: '#8ecae6' }
  ]
}
```

将 `series[0].itemStyle.color` 改为 `'#5b9bd5'`

将 `series[0].areaStyle.color` 改为：

```javascript
color: {
  type: 'linear',
  x: 0, y: 0, x2: 0, y2: 1,
  colorStops: [
    { offset: 0, color: 'rgba(91, 155, 213, 0.25)' },
    { offset: 1, color: 'rgba(91, 155, 213, 0.05)' }
  ]
}
```

- [ ] **Step 4: 更新加载动画颜色**

将 `.spinner` 的 `border-color` 改为 `'rgba(91, 155, 213, 0.2)'`

将 `.spinner` 的 `border-top-color` 改为 `'var(--color-primary)'`

- [ ] **Step 5: 更新列表 hover 背景**

将 `.analysis-item:hover` 的 `background` 改为 `'rgba(91, 155, 213, 0.05)'`

将 `.analysis-item` 的 `border-bottom` 改为 `'1px solid rgba(91, 155, 213, 0.08)'`

- [ ] **Step 6: 提交**

```bash
cd frontend
git add src/views/Dashboard.vue
git commit -m "style: 仪表盘图表和配色更新为新主题"
```

---

### Task 6: 更新徽章组件颜色

**Files:**
- Modify: `src/components/Badge.vue`

**Goal:** 适配新主题颜色

- [ ] **Step 1: 读取 Badge.vue 并更新颜色**

确保徽章使用新的 CSS 变量：`--color-success`, `--color-warning`, `--color-error`, `--color-info`

- [ ] **Step 2: 提交**

```bash
cd frontend
git add src/components/Badge.vue
git commit -m "style: 徽章组件颜色适配新主题"
```

---

### Task 7: 更新其他页面样式适配

**Files:**
- Modify: `src/views/Alerts.vue`
- Modify: `src/views/AlertDetail.vue`
- Modify: `src/views/Analyses.vue`

**Goal:** 更新所有视图页面中的硬编码颜色为 CSS 变量

- [ ] **Step 1: 更新 Alerts.vue**

搜索所有硬编码颜色（如 `#9b7fe8`、`rgba(155, 127, 232, ...)`）替换为新主题颜色

- [ ] **Step 2: 更新 AlertDetail.vue**

同样替换硬编码颜色

- [ ] **Step 3: 更新 Analyses.vue**

同样替换硬编码颜色

- [ ] **Step 4: 提交**

```bash
cd frontend
git add src/views/Alerts.vue src/views/AlertDetail.vue src/views/Analyses.vue
git commit -m "style: 所有视图页面样式适配新主题"
```

---

### Task 8: 启动开发服务器验证

**Files:** 无修改

**Goal:** 验证所有更改正常工作

- [ ] **Step 1: 安装依赖（如果需要）**

```bash
cd frontend
npm install
```

- [ ] **Step 2: 启动开发服务器**

```bash
npm run dev
```

- [ ] **Step 3: 手动验证**

在浏览器中打开，检查：
- 全局配色是否正确
- 侧边栏毛玻璃效果
- 卡片样式
- 图表颜色
- 各页面导航正常

---

## 总结

本计划包含 8 个任务，按顺序执行：
1. 更新全局 CSS 变量
2. 更新侧边栏为半透明毛玻璃
3. 更新卡片组件为统一规整风格
4. 更新全局装饰 blob
5. 更新仪表盘图表配色
6. 更新徽章组件
7. 更新其他页面样式
8. 验证

每个任务都独立可提交，完成后可单独验证。

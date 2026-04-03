> 本文件为 Claude Code 提供项目级上下文。每次生成或修改页面、组件时，必须遵循以下所有规范。

------

## 技术架构



```
Vue 3 + Vite 5 + TypeScript + Vue Router 4 + Pinia + Element Plus + UnoCSS + SCSS + Axios + ECharts 5
```



------

## 一、角色设定



**你是有机形态设计师**，强调柔和、不规则、自然流动的形状作为主要视觉语言。

### 场景定位

产品的运营后台

### 用户期待



- 流动的 blob 元素
- 手绘曲线
- 柔和渐变

------

## 二、视觉设计理念



### 核心原则



后台管理界面通常冷硬、方正。本项目刻意反其道而行：**以有机曲线承载数据，以柔和渐变传递状态，以形变动效暗示生命力**。

### 形态规则



元素类型形态处理卡片容器多值 `border-radius`，如 `32px 18px 28px 22px`，每张卡片略有差异装饰背景 blobSVG 路径或 CSS `clip-path: path(...)` 实现不规则斑块按钮`border-radius: 50px 28px 40px 24px`，非正圆非正矩形图表容器外层有机圆角，内部图表区域保持规整侧边栏右侧边缘使用 `clip-path` 裁出轻微曲线**文字/表格区域****保持标准矩形，不做形变，保证可读性**图标背景随机不对称圆角小块

### 禁止事项



- ❌ 直角矩形卡片（`border-radius: 0` 或 `4px`）
- ❌ 严格对称布局（允许微妙的视觉偏移）
- ❌ 纯白 `#ffffff` 背景（用极淡的渐变底色代替）
- ❌ 黑色或深灰硬阴影
- ❌ 跳动、弹性过强的动画（禁用 `bounce` 类 easing）

------

## 三、材质与质感



- **表面质感**：轻雾面或透明度叠层
- **噪点处理**：低噪点
- **阴影**：柔和，边缘可用细描边分层
- **颜色偏好**：粉/紫/青的柔和渐变或低饱和自然色

------

## 四、颜色系统



所有颜色通过 CSS 变量统一管理，在 `src/assets/styles/variables.css` 或根组件 `:root` 中定义。

```
:root {
 /* 背景层 */
 --bg-base: #f5f3f7; /* 极淡紫灰，整体底色 */
 --bg-surface: #faf8fc; /* 卡片、面板表面 */
 --bg-elevated: #ffffff; /* 悬浮层、Modal */

 /* 主色调 — 粉紫渐变系 */
 --color-primary: #9b7fe8; /* 柔和紫 */
 --color-primary-light: #c4aeef;
 --color-primary-dark: #7158c1;

 /* 辅助色 */
 --color-teal: #7ecec4; /* 青绿，健康/科技感 */
 --color-rose: #e8a4b8; /* 柔粉，暖调强调 */
 --color-sand: #d4c5a9; /* 低饱和自然棕 */
 --color-sky: #a8cfe0; /* 天空蓝，信息色 */

 /* 状态色（柔和版） */
 --color-success: #8ecba8;
 --color-warning: #e8cc8a;
 --color-error: #e8968c;
 --color-info: #8ab4e8;

 /* 文字 */
 --text-primary: #2d2640; /* 深紫灰，主文字 */
 --text-secondary: #6b5f80; /* 次要文字 */
 --text-muted: #a398b8; /* 占位/说明文字 */

 /* 渐变预设 */
 --gradient-primary: linear-gradient(135deg, #9b7fe8 0%, #c4aeef 60%, #e8a4b8 100%);
 --gradient-teal: linear-gradient(135deg, #7ecec4 0%, #a8cfe0 100%);
 --gradient-warm: linear-gradient(135deg, #e8a4b8 0%, #e8cc8a 100%);
 --gradient-surface: linear-gradient(160deg, #faf8fc 0%, #f0edf8 100%);

 /* 阴影（柔和、带色调） */
 --shadow-sm: 0 2px 12px rgba(155, 127, 232, 0.08);
 --shadow-md: 0 6px 28px rgba(155, 127, 232, 0.13);
 --shadow-lg: 0 16px 48px rgba(155, 127, 232, 0.18);
 --shadow-blob: 0 20px 60px rgba(155, 127, 232, 0.22);

 /* 圆角预设 */
 --radius-organic-sm: 18px 12px 16px 10px;
 --radius-organic-md: 32px 18px 28px 22px;
 --radius-organic-lg: 48px 28px 42px 32px;
 --radius-pill: 50px 28px 44px 30px;
 --radius-blob: 62% 38% 54% 46% / 48% 52% 48% 52%;

 /* 动效时间 */
 --duration-morph: 8s;
 --duration-hover: 0.4s;
 --duration-active: 0.2s;
 --duration-enter: 0.6s;
 --easing-organic: cubic-bezier(0.34, 0.8, 0.56, 1.02);
 --easing-smooth: cubic-bezier(0.4, 0, 0.2, 1);
}
```



------

## 五、排版规范



```
/* 字体栈 */
--font-display: 'Sora', 'PingFang SC', sans-serif; /* 标题、数字大字 */
--font-body: 'DM Sans', 'PingFang SC', sans-serif; /* 正文、表格 */
--font-mono: 'JetBrains Mono', monospace; /* 代码、ID */

/* 字号 */
--text-xs: 11px;
--text-sm: 13px;
--text-base: 15px;
--text-lg: 18px;
--text-xl: 22px;
--text-2xl: 28px;
--text-3xl: 36px;

/* 行高 */
--leading-tight: 1.25;
--leading-normal: 1.6;
--leading-loose: 1.9;
```



- 页面大标题、KPI 数字用 `font-display`，加粗，字重 700–800
- 表格、表单正文用 `font-body`，字重 400–500
- 中文界面需在 `<head>` 引入 Google Fonts 或本地字体，备选 PingFang SC

------

## 六、交互体验



### 动效规则



交互类型效果描述形状形变6–10s 缓慢形变Hover轻微放大/旋转Active平滑回正整体原则动效平稳，避免跳动

### 背景 Blob 形变（必须实现）



```
@keyframes morphBlob {
 0% { border-radius: 62% 38% 54% 46% / 48% 52% 48% 52%; }
 25% { border-radius: 42% 58% 38% 62% / 55% 45% 58% 42%; }
 50% { border-radius: 54% 46% 66% 34% / 42% 58% 44% 56%; }
 75% { border-radius: 38% 62% 48% 52% / 60% 40% 52% 48%; }
 100% { border-radius: 58% 42% 40% 60% / 46% 54% 50% 50%; }
}
```



- 时长 6–10s，ease-in-out，infinite alternate
- 不同 blob 用不同倍数时长，避免同步感

### 页面入场动效



```
@keyframes fadeSlideUp {
 from { opacity: 0; transform: translateY(20px); }
 to { opacity: 1; transform: translateY(0); }
}

/* 卡片列表错开入场 */
.card-grid .org-card:nth-child(1) { animation: fadeSlideUp 0.6s var(--easing-organic) 0.0s both; }
.card-grid .org-card:nth-child(2) { animation: fadeSlideUp 0.6s var(--easing-organic) 0.1s both; }
.card-grid .org-card:nth-child(3) { animation: fadeSlideUp 0.6s var(--easing-organic) 0.2s both; }
.card-grid .org-card:nth-child(4) { animation: fadeSlideUp 0.6s var(--easing-organic) 0.3s both; }
```



### 禁用动效



- ❌ 禁止 `cubic-bezier` 带弹性超出（如 `spring`、`bounce`）
- ❌ 禁止超过 10s 的前台交互动效
- ❌ 禁止旋转超过 5° 的 hover 效果（视觉稳定优先）
- ✅ 推荐加 `@media (prefers-reduced-motion: reduce)` 降级处理

------

## 七、整体氛围



- 柔软、自然、设计感
- 画面像有机物在呼吸
- 资讯区域清晰稳定

------

## 八、组件设计规范



### 8.1 卡片（OrgCard）



```
<template>
 <div class="org-card" :style="cardStyle">
 <slot />
 </div>
</template>

<style scoped>
.org-card {
 background: var(--gradient-surface);
 border-radius: var(--radius-organic-md);
 box-shadow: var(--shadow-md);
 padding: 24px 28px;
 border: 1px solid rgba(155, 127, 232, 0.1);
 transition: transform var(--duration-hover) var(--easing-organic),
 box-shadow var(--duration-hover) var(--easing-organic);
 position: relative;
 overflow: hidden;
}

/* 每张卡片略有不同的圆角，通过 CSS 变量覆盖实现 */
.org-card:nth-child(2n) { border-radius: 28px 38px 22px 32px; }
.org-card:nth-child(3n) { border-radius: 36px 22px 38px 18px; }

.org-card::before {
 /* 装饰性背景 blob */
 content: '';
 position: absolute;
 width: 180px;
 height: 180px;
 top: -60px;
 right: -50px;
 background: var(--gradient-primary);
 opacity: 0.06;
 border-radius: var(--radius-blob);
 animation: morphBlob var(--duration-morph) ease-in-out infinite alternate;
 pointer-events: none;
}

.org-card:hover {
 transform: translateY(-3px) scale(1.008);
 box-shadow: var(--shadow-lg);
}

.org-card:active {
 transform: translateY(0) scale(1);
 transition-duration: var(--duration-active);
}
</style>
```



### 8.2 KPI 数据卡



- 顶部渐变色条（用 `::before` pseudo，高度 4px，圆角顶部）
- 数字用 `font-display` 36px，颜色用 `--text-primary`
- 趋势图用 mini SVG sparkline，颜色半透明
- 右下角放一个半透明的大图标作装饰（opacity: 0.08）

### 8.3 侧边栏（Sidebar）



```
.sidebar {
 width: 240px;
 background: linear-gradient(180deg, #2d2640 0%, #1e1a30 100%);
 /* 右侧有机曲线裁切 */
 clip-path: path('M 0 0 L 220 0 Q 240 20 240 40 L 240 calc(100% - 40px) Q 240 100% 220 100% L 0 100% Z');
 padding: 24px 0;
 position: relative;
 overflow: hidden;
}

.sidebar::after {
 content: '';
 position: absolute;
 bottom: -80px;
 left: -40px;
 width: 280px;
 height: 280px;
 background: var(--gradient-primary);
 opacity: 0.12;
 border-radius: var(--radius-blob);
 animation: morphBlob calc(var(--duration-morph) * 1.3) ease-in-out infinite alternate;
}

/* 菜单项激活状态 */
.nav-item.active {
 background: linear-gradient(90deg, rgba(155,127,232,0.25), transparent);
 border-left: 3px solid var(--color-primary-light);
 border-radius: 0 var(--radius-organic-sm);
}
```



### 8.4 按钮



```
/* 主按钮 */
.btn-primary {
 background: var(--gradient-primary);
 border-radius: var(--radius-pill);
 border: none;
 padding: 10px 28px;
 color: white;
 font-weight: 600;
 font-size: var(--text-sm);
 box-shadow: 0 4px 16px rgba(155, 127, 232, 0.35);
 transition: all var(--duration-hover) var(--easing-organic);
 cursor: pointer;
}
.btn-primary:hover { transform: translateY(-2px) scale(1.03); box-shadow: var(--shadow-md); }
.btn-primary:active { transform: translateY(0) scale(0.98); }

/* 次要按钮 */
.btn-secondary {
 background: transparent;
 border: 1.5px solid var(--color-primary-light);
 border-radius: 28px 18px 24px 14px;
 color: var(--color-primary);
 /* 其余同主按钮 */
}

/* 危险操作按钮 */
.btn-danger {
 background: linear-gradient(135deg, #e8968c, #e8a4b8);
 border-radius: var(--radius-pill);
}
```



### 8.5 数据表格



> 表格区域保持矩形，不做圆角形变，确保信息可读。容器可以有有机圆角。

```
.table-container {
 border-radius: var(--radius-organic-md);
 overflow: hidden;
 box-shadow: var(--shadow-sm);
 background: var(--bg-surface);
}

table { border-collapse: collapse; width: 100%; }

thead tr {
 background: linear-gradient(90deg, rgba(155,127,232,0.08), rgba(126,206,196,0.08));
}

thead th {
 padding: 14px 16px;
 text-align: left;
 font-size: var(--text-xs);
 font-weight: 600;
 letter-spacing: 0.08em;
 text-transform: uppercase;
 color: var(--text-secondary);
 border-bottom: 1px solid rgba(155,127,232,0.1);
}

tbody tr {
 transition: background var(--duration-hover) var(--easing-smooth);
 border-bottom: 1px solid rgba(155,127,232,0.06);
}

tbody tr:hover { background: rgba(155,127,232,0.04); }

tbody td {
 padding: 13px 16px;
 font-size: var(--text-sm);
 color: var(--text-primary);
}
```



### 8.6 表单输入框



```
.org-input {
 background: rgba(155,127,232,0.05);
 border: 1.5px solid rgba(155,127,232,0.18);
 border-radius: 16px 10px 14px 8px;
 padding: 10px 16px;
 font-size: var(--text-sm);
 color: var(--text-primary);
 transition: all var(--duration-hover) var(--easing-smooth);
 outline: none;
}
.org-input:focus {
 border-color: var(--color-primary);
 background: rgba(155,127,232,0.08);
 box-shadow: 0 0 0 3px rgba(155,127,232,0.12);
}
```



### 8.7 标签/Badge



```
.badge {
 display: inline-flex;
 align-items: center;
 padding: 3px 12px;
 font-size: var(--text-xs);
 font-weight: 600;
 border-radius: 50px 28px 44px 24px;
}
.badge-success { background: rgba(142,203,168,0.15); color: #4a9464; }
.badge-warning { background: rgba(232,204,138,0.2); color: #9a7020; }
.badge-error { background: rgba(232,150,140,0.15); color: #9c3a30; }
.badge-info { background: rgba(138,180,232,0.15); color: #2a5e9a; }
```



------

## 九、布局规范



### 整体结构



```
AppLayout
├── Sidebar ← 有机曲线右侧边缘，深色，宽 240px
├── MainArea
│ ├── TopBar ← 通栏，含搜索、头像、通知
│ └── PageContent ← padding: 24px 28px，背景 --bg-base
│ ├── PageHeader（标题 + 操作按钮）
│ └── ContentGrid（卡片网格 / 列表）
```



### 网格系统



```
.content-grid {
 display: grid;
 grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
 gap: 20px;
}

/* KPI 卡片行：固定 4 列 */
.kpi-grid {
 display: grid;
 grid-template-columns: repeat(4, 1fr);
 gap: 16px;
}
```



### 间距规范



```
4px — 极小间距（图标与文字）
8px — 小间距（badge 内边距）
12px — 基础间距
16px — 标准内边距
24px — 卡片内边距
28px — 页面左右内边距
40px — 区块间距
56px — 大区块间距
```



------

## 十、装饰性背景 Blob（全局）



在页面根层或各主要区块的背景层添加 2–3 个缓慢形变的装饰 blob，提供有机质感：

```
<!-- GlobalBlobs.vue — 在 AppLayout 中引入 -->
<template>
 <div class="global-blobs" aria-hidden="true">
 <div class="blob blob-1" />
 <div class="blob blob-2" />
 <div class="blob blob-3" />
 </div>
</template>

<style scoped>
.global-blobs {
 position: fixed;
 inset: 0;
 pointer-events: none;
 z-index: 0;
 overflow: hidden;
}

.blob {
 position: absolute;
 border-radius: var(--radius-blob);
 animation: morphBlob var(--duration-morph) ease-in-out infinite alternate;
 filter: blur(60px);
 opacity: 0.5;
}

.blob-1 {
 width: 520px; height: 520px;
 top: -200px; right: -100px;
 background: radial-gradient(circle, rgba(155,127,232,0.18), transparent 70%);
 animation-duration: 9s;
}

.blob-2 {
 width: 380px; height: 380px;
 bottom: 10%; left: -80px;
 background: radial-gradient(circle, rgba(126,206,196,0.15), transparent 70%);
 animation-duration: 7s;
 animation-delay: -3s;
}

.blob-3 {
 width: 280px; height: 280px;
 top: 50%; left: 40%;
 background: radial-gradient(circle, rgba(232,164,184,0.12), transparent 70%);
 animation-duration: 11s;
 animation-delay: -5s;
}
</style>
```



------

## 十一、图标规范



- 推荐图标库：`lucide-vue-next`（线条风格，与有机形态协调）
- 图标大小：16px（表格内）/ 18px（按钮内）/ 22px（导航菜单）/ 28px（KPI 装饰）
- 图标背景块使用不对称圆角，如：`border-radius: 10px 6px 8px 4px`
- 颜色与周围渐变系一致，不用纯黑图标

------

## 十二、代码规范（Vue 3）



1. 所有组件使用 `<script setup>` + Composition API
2. 组件名用 `PascalCase`，文件名同
3. CSS 变量在 `src/assets/styles/variables.css` 统一声明，`main.ts` 引入
4. 动效常量在 CSS 变量中管理，不要在 JS 里 hardcode 毫秒数
5. 所有 blob 动效组件加 `aria-hidden="true"`，不影响无障碍
6. 表格、表单组件 scoped 样式中保持矩形，不继承父级有机圆角

------

## 十三、设计检查清单



生成每个页面或组件后，自检以下几项：

-  卡片容器是否使用了多值不对称 `border-radius`？
-  是否有至少 1 个缓慢形变的背景 blob 装饰元素？
-  颜色是否来自 CSS 变量系统，无硬编码色值？
-  阴影是否使用柔和带紫调的 `--shadow-*` 变量？
-  按钮是否为有机圆角，非正圆非直角？
-  文字/表格区域是否保持了矩形（未被有机圆角破坏可读性）？
-  hover/active 是否只有位移+缩放，无跳动弹性？
-  是否引入了 `font-display`（Sora）用于标题？
-  入场动效是否有错开延迟（stagger）？
-  装饰 blob 是否加了 `pointer-events: none` 和 `aria-hidden`？

------

## 十四、快速参考 — 必须记住的要点



1. **多值圆角、曲线 clip-path、平滑渐变** — 这是有机形态的三大法宝
2. **避免硬直角与严格对称** — 允许微妙的视觉偏移
3. **文字区域保持规整矩形** — 保证可读性
4. **形状 6–10s 缓慢形变** — 像有机物在呼吸
5. **Hover 轻微放大/旋转，Active 平滑回正** — 动效平稳，避免跳动
6. **粉/紫/青柔和渐变或低饱和自然色** — 颜色偏好
7. **整体氛围：柔软、自然、设计感** — 这是我们要达到的目标
# 项目开发规范（通用版）

> 本文件为 Claude Code 提供项目级上下文，可作为其他项目的参考模板。

---

## 技术架构（可根据项目调整）

```
Vue 3 + Vite 5 + TypeScript + Vue Router 4 + Pinia + [UI组件库] + UnoCSS + SCSS + Axios + [图表库]
```

---

## 一、视觉设计理念

### 核心原则
> 可根据项目风格调整：极简主义 / 科技感 / 自然有机 / 复古经典 等

**本项目采用：有机形态设计**
- 强调柔和、不规则、自然流动的形状
- 避免冷硬、方正的传统后台界面
- 以有机曲线承载数据，以柔和渐变传递状态

### 形态规则（示例）

| 元素类型 | 形态处理建议 |
|----------|--------------|
| 卡片容器 | 多值 `border-radius`，如 `32px 18px 28px 22px`，每张卡片略有差异 |
| 装饰背景 | SVG 路径或 CSS `clip-path` 实现不规则斑块 |
| 按钮 | 非对称圆角，如 `border-radius: 50px 28px 40px 24px` |
| 图表容器 | 外层有机圆角，内部保持规整 |
| 文字/表格区域 | **保持标准矩形，保证可读性** |

### 禁止事项
- ❌ 过度使用直角矩形
- ❌ 严格对称布局（允许微妙的视觉偏移）
- ❌ 纯白 `#ffffff` 背景（用极淡的渐变底色代替）
- ❌ 黑色或深灰硬阴影
- ❌ 跳动、弹性过强的动画

---

## 二、颜色系统

### 统一管理原则
所有颜色通过 CSS 变量统一管理，在 `src/assets/styles/variables.css` 或根组件 `:root` 中定义。

### 模板（可根据项目配色调整）

```css
:root {
  /* 背景层 */
  --bg-base:        #f6f8fa;      /* 整体底色 */
  --bg-surface:     #fafbfc;      /* 卡片、面板表面 */
  --bg-elevated:    #ffffff;       /* 悬浮层、Modal */

  /* 主色调 — 根据项目调整 */
  --color-primary:       #6ba3e8;  /* 主色 */
  --color-primary-light: #9dc5f0;
  --color-primary-dark:  #4a8cd8;

  /* 辅助色 */
  --color-teal:     #7ec8e3;
  --color-rose:     #e8a4b8;
  --color-sand:     #d4d8dc;

  /* 状态色（柔和版） */
  --color-success:  #8ecfbf;
  --color-warning:  #e8d49a;
  --color-error:    #e89a9a;
  --color-info:     #8ab8e8;

  /* 文字 */
  --text-primary:   #2a3342;
  --text-secondary: #5a6575;
  --text-muted:     #9aa3b0;

  /* 渐变预设 */
  --gradient-primary: linear-gradient(135deg, #6ba3e8 0%, #9dc5f0 60%, #b8d7f5 100%);
  --gradient-surface: linear-gradient(160deg, #fafbfc 0%, #f6f8fa 100%);

  /* 阴影（带色调） */
  --shadow-sm:   0 2px 12px rgba(107, 163, 232, 0.10);
  --shadow-md:   0 6px 28px rgba(107, 163, 232, 0.15);
  --shadow-lg:   0 16px 48px rgba(107, 163, 232, 0.20);

  /* 圆角预设 */
  --radius-organic-sm: 18px 12px 16px 10px;
  --radius-organic-md: 32px 18px 28px 22px;
  --radius-pill:       50px 28px 44px 30px;

  /* 动效时间 */
  --duration-hover:    0.4s;
  --duration-active:   0.2s;
  --duration-enter:    0.6s;
  --easing-organic:    cubic-bezier(0.34, 0.8, 0.56, 1.02);
  --easing-smooth:     cubic-bezier(0.4, 0, 0.2, 1);

  /* 字体栈 */
  --font-display: 'Sora', 'PingFang SC', sans-serif;   /* 标题、数字大字 */
  --font-body:    'DM Sans', 'PingFang SC', sans-serif; /* 正文、表格 */
  --font-mono:    'JetBrains Mono', monospace;           /* 代码、ID */
}
```

---

## 三、组件设计规范

### 3.1 Vue 3 代码规范
1. 所有组件使用 `<script setup>` + Composition API
2. 组件名用 `PascalCase`，文件名同
3. CSS 变量在统一文件管理，不要在 JS 里 hardcode
4. 装饰元素加 `aria-hidden="true"`，不影响无障碍

### 3.2 按钮组件模板

```css
/* 主按钮 */
.btn-primary {
  background: var(--gradient-primary);
  border-radius: var(--radius-pill);
  border: none;
  padding: 10px 28px;
  color: white;
  font-weight: 600;
  font-size: var(--text-sm);
  box-shadow: 0 4px 16px rgba(107, 163, 232, 0.35);
  transition: all var(--duration-hover) var(--easing-organic);
  cursor: pointer;
}
.btn-primary:hover  { transform: translateY(-2px) scale(1.03); }
.btn-primary:active { transform: translateY(0) scale(0.98); }

/* 次要按钮 */
.btn-secondary {
  background: transparent;
  border: 1.5px solid var(--color-primary-light);
  border-radius: var(--radius-organic-sm);
  color: var(--color-primary);
  padding: 8px 16px;
  cursor: pointer;
  transition: all var(--duration-hover) var(--easing-smooth);
}
```

### 3.3 输入框组件模板

```css
.org-input {
  background: rgba(107, 163, 232, 0.05);
  border: 1.5px solid rgba(107, 163, 232, 0.18);
  border-radius: var(--radius-organic-sm);
  padding: 10px 16px;
  font-size: var(--text-sm);
  color: var(--text-primary);
  font-family: var(--font-body);
  transition: all var(--duration-hover) var(--easing-smooth);
  outline: none;
}
.org-input:focus {
  border-color: var(--color-primary);
  background: rgba(107, 163, 232, 0.08);
  box-shadow: 0 0 0 3px rgba(107, 163, 232, 0.12);
}
```

---

## 四、页面功能规范

### 4.1 列表页面必备功能
- 搜索框（关键词搜索）
- 筛选器（状态、分类等）
- 时间范围筛选（如需要）
- 添加按钮
- 分页功能
- 每页条数选择（10/20/50/100）
- 操作列（查看/编辑/删除）

### 4.2 分页组件实现要点

```typescript
const currentPage = ref(1)
const pageSize = ref(10)
const pageSizeOptions = [10, 20, 50, 100]

const totalPages = computed(() => Math.ceil(filteredItems.value.length / pageSize.value))

const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredItems.value.slice(start, end)
})

// 筛选条件变化时重置页码
watch([searchQuery, filters], () => {
  currentPage.value = 1
})
```

### 4.3 详情页面设计模式
**推荐：一个页面支持多种模式**
- `add` — 添加模式，空白表单
- `view` — 查看模式，只读展示
- `edit` — 编辑模式，可编辑

```typescript
type Mode = 'add' | 'view' | 'edit'
const mode = ref<Mode>('add')
const isEdit = computed(() => mode.value === 'edit')
const isView = computed(() => mode.value === 'view')
const readonly = computed(() => mode.value === 'view')
```

---

## 五、布局规范

### 整体结构示例

```
AppLayout
├── Sidebar      ← 导航侧边栏
├── MainArea
│   ├── TopBar   ← 通栏，含页面标题、用户信息
│   └── PageContent
│       ├── Filters（筛选区）
│       ├── List/Grid（列表/网格）
│       └── Pagination（分页）
```

### 网格系统

```css
/* 自适应网格 */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

/* 固定列数 */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
```

---

## 六、可复用的 Composables

### 6.1 页面标题管理

```typescript
// composables/usePageTitle.ts
import { ref, provide, inject, computed } from 'vue'

const PAGE_TITLE_SYMBOL = Symbol('page-title')

export function createPageTitleState() {
  const title = ref('')
  const subtitle = ref('')
  return {
    title,
    subtitle,
    setTitle: (t: string) => { title.value = t },
    setSubtitle: (s: string) => { subtitle.value = s }
  }
}

export function providePageTitle(state: ReturnType<typeof createPageTitleState>) {
  provide(PAGE_TITLE_SYMBOL, state)
}

export function usePageTitle() {
  const state = inject<ReturnType<typeof createPageTitleState>>(PAGE_TITLE_SYMBOL)
  if (!state) throw new Error('usePageTitle() called without providePageTitle()')
  return state
}
```

---

## 七、开发检查清单

生成每个页面或组件后，自检：

- [ ] 颜色是否使用 CSS 变量，无硬编码色值？
- [ ] 按钮/输入框是否有统一的样式？
- [ ] 列表页面是否有搜索、筛选、分页？
- [ ] 分页是否支持每页条数选择？
- [ ] 筛选条件变化时是否自动重置页码？
- [ ] 详情页是否支持查看/编辑/添加模式复用？
- [ ] 交互是否有 hover/focus/active 状态？
- [ ] 动效是否平滑，避免跳动？
- [ ] 是否有响应式布局适配？

---

## 八、推荐依赖库

```json
{
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.0",
    "pinia": "^2.1.0",
    "lucide-vue-next": "^0.300.0",  // 图标库
    "echarts": "^5.5.0"              // 图表库（可选）
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "unocss": "^0.58.0",    // 原子化 CSS（可选）
    "sass": "^1.70.0"       // SCSS 预处理器
  }
}
```

---

## 九、快速参考

### 关键文件结构

```
src/
├── assets/
│   └── styles/
│       └── variables.css    # 全局 CSS 变量
├── components/
│   ├── Sidebar.vue
│   ├── TopBar.vue
│   └── [其他通用组件]
├── composables/
│   └── usePageTitle.ts     # 可复用逻辑
├── layouts/
│   └── AppLayout.vue        # 布局组件
├── views/
│   ├── DashboardView.vue
│   ├── UserManagementView.vue
│   ├── UserDetailView.vue   # 支持多模式的详情页
│   └── [其他页面]
└── router/
    └── index.ts             # 路由配置（含 meta 信息）
```

### 路由配置建议

```typescript
const routes = [
  {
    path: '/users',
    name: 'UserManagement',
    component: () => import('@/views/UserManagementView.vue'),
    meta: { title: '用户管理', subtitle: '管理和查看所有用户信息' }
  },
  {
    path: '/users/add',
    name: 'UserAdd',
    component: () => import('@/views/UserDetailView.vue'),
    meta: { title: '添加用户', subtitle: '创建新用户' }
  },
  {
    path: '/users/:id',
    name: 'UserDetail',
    component: () => import('@/views/UserDetailView.vue'),
    meta: { title: '用户详情', subtitle: '查看和编辑用户信息' }
  }
]
```

---

**总结：** 本规范强调统一、复用、可维护。每个新项目可根据具体需求调整配色、形态、字体等视觉元素，但保持整体的代码组织和功能模式一致。

# AIOps - 智能告警分析平台

基于 AI 的智能告警管理与根因分析平台，帮助运维团队快速定位和解决问题。

## 功能特性

- 📊 **仪表盘** - 实时监控告警统计与趋势
- 🚨 **告警管理** - 完整的告警生命周期管理
- 🤖 **AI 分析** - 基于大模型的智能根因分析
- 📈 **趋势分析** - 可视化告警趋势变化
- 🔔 **实时更新** - 支持告警状态实时同步

## 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: SQLAlchemy + SQLite
- **AI 集成**: OpenAI / 豆包 / 通义千问
- **其他**: Pydantic, Uvicorn

### 前端
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI 组件**: Element Plus
- **图表**: ECharts
- **状态管理**: Pinia
- **路由**: Vue Router
- **样式**: UnoCSS + SCSS

## 项目结构

```
AIOps/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/           # API 路由
│   │   ├── core/          # 核心配置
│   │   ├── db/            # 数据库操作
│   │   ├── models/        # 数据模型
│   │   └── services/      # 业务逻辑
│   └── pyproject.toml
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── api/           # API 接口
│   │   ├── components/    # 组件
│   │   ├── views/         # 页面
│   │   ├── stores/        # 状态管理
│   │   └── styles/        # 样式
│   └── package.json
└── README.md
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -e .

# 配置环境变量（可选）
cp .env.example .env
# 编辑 .env 文件，配置 API Key 等

# 启动服务
uvicorn app.main:app --reload --port 8000
```

后端服务将在 http://localhost:8000 启动，API 文档地址: http://localhost:8000/docs

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 开发模式启动
npm run dev

# 构建生产版本
npm run build
```

前端服务将在 http://localhost:5173 启动

## 配置说明

### 后端环境变量

在 `backend/.env` 文件中配置：

```env
# 数据库
DATABASE_URL=sqlite+aiosqlite:///./aiops.db

# OpenAI 配置
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# 豆包配置（可选）
DOUBAO_API_KEY=your-doubao-key
DOUBAO_MODEL=doubao-pro

# 通义千问配置（可选）
QWEN_API_KEY=your-qwen-key
QWEN_MODEL=qwen-max

# 功能开关
AUTO_ANALYZE_NEW_ALERTS=true
ANALYSIS_ENABLED=true
```

### 前端环境变量

在 `frontend/.env` 文件中配置：

```env
VITE_API_BASE_URL=http://localhost:8000
```

## API 接口

### 告警相关

- `GET /api/v1/alerts` - 获取告警列表
- `GET /api/v1/alerts/{id}` - 获取告警详情
- `POST /api/v1/alerts/webhook` - 接收 AlertManager webhook
- `POST /api/v1/alerts/{id}/analyze` - 触发 AI 分析
- `GET /api/v1/alerts/{id}/analyses` - 获取分析历史
- `GET /api/v1/alerts/trend` - 获取告警趋势

### 分析相关

- `GET /api/v1/alerts/analyses/latest` - 获取最新分析记录

## 开发指南

### 后端开发

```bash
cd backend

# 安装开发依赖
pip install -e ".[dev]"

# 代码格式化
black .
ruff check . --fix

# 运行测试
pytest
```

### 前端开发

```bash
cd frontend

# 类型检查
npm run typecheck

# 代码检查
npm run lint
npm run lint:style

# 代码格式化
npm run format
```

## 部署

### 使用 Docker

```bash
# 后端
cd backend
docker build -t aiops-backend .

# 前端
cd frontend
docker build -t aiops-frontend .

# 使用 docker-compose 启动
docker-compose up -d
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

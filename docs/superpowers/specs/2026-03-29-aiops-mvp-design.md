---
name: AIOps MVP 告警根因分析设计
description: 基于 LLM 的告警根因分析系统 MVP 架构设计
type: design
---

# AIOps MVP - 告警根因分析系统

## Context

构建一个基于 LLM 的 AIOps 系统 MVP，核心功能是接收 AlertManager 告警，自动查询 Prometheus 指标，调用商用 LLM API 进行根因分析并给出解决方案建议。

**为什么做这个：**
- AI + 运维是 2024-2026 热门赛道
- 告警根因分析是运维痛点，能显著缩短 MTTR
- 面试时能讲架构、讲痛点、讲数据

## 设计原则

- MVP 优先：先跑通核心流程
- 简单直接：避免过度设计
- 可扩展：为后续功能预留空间

---

## 1. 架构概览

采用轻量级模块化架构（方案 A）：

```
┌─────────────────────────────────────────────────────────────┐
│                         FastAPI API 层                       │
│  - /api/v1/alerts/webhook   (AlertManager webhook)         │
│  - /api/v1/alerts/analyze   (手动触发分析)                  │
│  - /api/v1/alerts/{id}      (查询分析结果)                  │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                      业务逻辑层                               │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  AlertProcessor  │  │  AlertAnalyzer   │                │
│  │  (告警去重处理)   │  │  (根因分析核心)   │                │
│  └──────────────────┘  └──────────────────┘                │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ PrometheusClient │  │   LLMService     │                │
│  │  (查询指标)       │  │  (LangChain)     │                │
│  └──────────────────┘  └──────────────────┘                │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    SQLite 数据层                              │
│  - alerts: 告警记录表                                         │
│  - analyses: 分析结果表                                       │
│  - feedback: 用户反馈表 (预留)                                │
└──────────────────────────────────────────────────────────────┘
```

**部署方式：** 独立部署，非 K8s Operator

**接口类型：** 纯 API，无 Web UI

---

## 2. 目录结构

```
aiops/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 入口
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── alerts.py        # 告警相关 API
│   │   │   └── health.py        # 健康检查
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # 配置管理 (Pydantic Settings)
│   │   │   └── database.py      # 数据库连接
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py       # Pydantic schemas
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── alert_processor.py   # 告警去重与状态管理
│   │   │   ├── alert_analyzer.py    # 根因分析服务
│   │   │   ├── prometheus_client.py # Prometheus 查询客户端
│   │   │   └── llm_service.py       # LLM 集成 (LangChain)
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── models.py          # SQLAlchemy models
│   │       └── crud.py            # 数据库 CRUD 操作
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   └── test_services.py
│   ├── pyproject.toml          # 项目配置 (uv)
│   ├── .env.example            # 环境变量示例
│   └── README.md
└── docs/
    └── superpowers/specs/
        └── 2026-03-29-aiops-mvp-design.md
```

---

## 3. 数据模型

### 3.1 alerts 表 - 告警记录

| 字段 | 类型 | 说明 | 约束 |
|------|------|------|------|
| id | Integer | 主键 | PK, autoincrement |
| fingerprint | String | AlertManager 告警指纹 | unique, not null |
| alert_id | String | 告警 ID | indexed |
| group_key | String | 告警分组 key | |
| status | String | firing/resolved | not null |
| alert_name | String | 告警名称 | not null, indexed |
| severity | String | 严重程度 | indexed |
| summary | String | 告警摘要 | |
| description | Text | 告警描述 | |
| labels | JSON | 标签 | JSON |
| annotations | JSON | 注解 | JSON |
| starts_at | DateTime | 告警开始时间 | not null |
| ends_at | DateTime | 告警结束时间 | nullable |
| update_count | Integer | 更新次数 | default 0 |
| last_received_at | DateTime | 最后接收时间 | not null |
| created_at | DateTime | 创建时间 | default now |

### 3.2 analyses 表 - 分析结果

| 字段 | 类型 | 说明 | 约束 |
|------|------|------|------|
| id | Integer | 主键 | PK, autoincrement |
| alert_id | Integer | 关联 alerts.id | FK, indexed |
| version | Integer | 分析版本 | default 1 |
| is_latest | Boolean | 是否为最新分析 | default true |
| root_cause | Text | 根因分析 | |
| possible_solutions | JSON | 建议解决方案 | JSON array |
| reasoning | Text | 推理过程 | |
| confidence_score | Float | 置信度 0-1 | |
| model_used | String | 使用的模型 | |
| status | String | pending/completed/failed | not null |
| error_message | Text | 错误信息 | nullable |
| started_at | DateTime | 分析开始时间 | |
| completed_at | DateTime | 分析完成时间 | nullable |
| created_at | DateTime | 创建时间 | default now |

### 3.3 feedback 表 - 用户反馈（MVP 预留）

| 字段 | 类型 | 说明 | 约束 |
|------|------|------|------|
| id | Integer | 主键 | PK, autoincrement |
| analysis_id | Integer | 关联 analyses.id | FK, indexed |
| rating | Integer | 评分 1-5 | |
| comment | Text | 评论 | |
| correct_root_cause | Boolean | 根因是否正确 | |
| created_at | DateTime | 创建时间 | default now |

---

## 4. API 设计

### 4.1 AlertManager Webhook

```
POST /api/v1/alerts/webhook
Content-Type: application/json
```

**Request Body:** AlertManager webhook 标准格式
```json
{
  "receiver": "aiops-webhook",
  "status": "firing",
  "alerts": [...],
  "groupLabels": {},
  "commonLabels": {},
  "commonAnnotations": {},
  "externalURL": "",
  "version": "4",
  "groupKey": ""
}
```

**Response:**
```json
{
  "status": "ok",
  "processed": 2,
  "created": 1,
  "updated": 1
}
```

### 4.2 告警查询

```
GET /api/v1/alerts?status=firing&limit=20&offset=0
```

**Response:**
```json
{
  "items": [...],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

```
GET /api/v1/alerts/{id}
GET /api/v1/alerts/fingerprint/{fingerprint}
```

### 4.3 分析相关

```
POST /api/v1/alerts/{alert_id}/analyze
# 手动触发分析
```

```
GET /api/v1/alerts/{alert_id}/analyses
# 获取某告警的所有分析历史
```

```
GET /api/v1/analyses/latest?limit=10
# 获取最新分析结果
```

### 4.4 健康检查

```
GET /health
GET /ready
```

---

## 5. 核心服务设计

### 5.1 AlertProcessor（告警处理器）

**职责：**
- 接收并解析 AlertManager webhook 数据
- 根据 fingerprint 去重
- 处理 firing/resolved 状态变化
- 决定是否触发分析

**核心方法：**
```python
process_alerts(webhook_data: dict) -> ProcessResult
should_trigger_analysis(alert: Alert, old_alert: Alert | None) -> bool
```

**触发分析规则：**
- 新告警且 status = firing → 触发
- 已有告警，status 从 resolved → firing → 触发
- 重复 firing 告警 → 不触发（只更新时间）
- resolved 告警 → 不触发分析

### 5.2 AlertAnalyzerService（根因分析核心）

**职责：**
- 协调分析流程
- 调用 PrometheusClient 查询指标
- 调用 LLMService 进行分析
- 保存分析结果

**核心方法：**
```python
analyze_alert(alert_id: int) -> Analysis
```

**流程：**
```
1. 从 DB 读取 alert
2. 创建 analysis 记录 (status=pending)
3. PrometheusClient 查询相关指标
4. 构建 Prompt
5. LLMService 调用 API
6. 解析返回结果
7. 更新 analysis 记录 (status=completed/failed)
```

### 5.3 PrometheusClient

**职责：**
- 连接 Prometheus
- 根据告警标签智能查询相关指标
- 提取时间序列数据

**核心方法：**
```python
query(query_str: str, time: datetime | None = None) -> dict
query_range(query_str: str, start: datetime, end: datetime, step: str) -> dict
get_related_metrics(alert_labels: dict, lookback_minutes: int = 30) -> dict
```

**智能查询策略：**
- 根据 alert 的 job/instance/pod 等标签
- 查询该实例相关的黄金指标（CPU, 内存, 磁盘, 网络, 错误率）
- 告警发生前 30 分钟的数据

### 5.4 LLMService

**职责：**
- LangChain 封装
- 支持多模型（OpenAI/豆包/通义千问）
- Prompt 模板管理
- 结构化输出解析

**核心方法：**
```python
analyze_root_cause(alert_data: dict, metrics_data: dict) -> AnalysisResult
```

**Prompt 模板：**
```
你是一个经验丰富的 SRE 专家。请分析以下告警并给出根因分析和解决方案建议。

【告警信息】
名称: {alert_name}
严重程度: {severity}
摘要: {summary}
描述: {description}
标签: {labels}
开始时间: {starts_at}

【相关指标数据】
{metrics_summary}

请以 JSON 格式返回结果，格式如下：
{{
  "root_cause": "详细的根因分析，说明可能是什么导致了这个告警",
  "possible_solutions": [
    "建议的解决方案 1",
    "建议的解决方案 2"
  ],
  "reasoning": "你的推理过程，说明是如何得出这个结论的",
  "confidence_score": 0.8
}}

要求：
- confidence_score 是 0-1 之间的数字，表示你对分析结果的置信度
- root_cause 要具体，不要太笼统
- possible_solutions 要可操作
```

---

## 6. 技术栈与依赖

### 环境管理
- **uv**: Python 版本和依赖管理（替代 pip/venv）

### 核心依赖 (pyproject.toml)
```toml
[project]
name = "aiops-mvp"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "sqlalchemy>=2.0.25",
    "pydantic>=2.6.0",
    "pydantic-settings>=2.1.0",
    "langchain>=0.1.10",
    "langchain-openai>=0.0.8",
    "python-multipart>=0.0.6",
    "python-json-logger>=2.0.7",
    "prometheus-api-client>=0.5.0",
    "alembic>=1.13.0",  # 数据库迁移（可选，MVP 可先不用）
]
```

### 开发依赖
```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.27.0",
    "black>=24.0",
    "ruff>=0.2.0",
    "mypy>=1.8.0",
]
```

---

## 7. 数据流程

### 完整流程图

```
┌──────────────┐
│ AlertManager │
└──────┬───────┘
       │
       │ 1. Webhook POST
       ▼
┌─────────────────────────────────┐
│ POST /api/v1/alerts/webhook     │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ AlertProcessor.process_alerts() │
├─────────────────────────────────┤
│ 2. 解析 webhook 数据            │
│ 3. 遍历 alerts 列表             │
│ 4. 按 fingerprint 查询 DB       │
└──────┬──────────────────────────┘
       │
       ├─ 不存在 ───────────────┐
       │                         │
       │ 存在                     │
       ▼                         ▼
┌──────────────────┐    ┌──────────────────┐
│ 创建新 alert     │    │ 更新现有 alert   │
│ status: firing   │    │ update_count++   │
└────────┬─────────┘    └────────┬─────────┘
         │                         │
         ▼                         ▼
  ┌─────────────────────────────────────────┐
  │ should_trigger_analysis()?              │
  ├─────────────────────────────────────────┤
  │ 新 firing?          → YES               │
  │ resolved→firing?    → YES               │
  │ 重复 firing?        → NO                │
  │ resolved?           → NO                │
  └─────────────┬───────────────────────────┘
                │ YES
                ▼
    ┌───────────────────────────┐
    │ AlertAnalyzerService      │
    ├───────────────────────────┤
    │ 5. 创建 analysis (pending)│
    └─────────────┬─────────────┘
                  │
      ┌───────────┴───────────┐
      │                       │
      ▼                       ▼
┌──────────────┐    ┌─────────────────┐
│ Prometheus   │    │ 构建 Prompt     │
│ Client 查询  │    │ 告警 + 指标     │
│ 相关指标     │    └────────┬────────┘
└──────┬───────┘             │
       │                     │
       └──────────┬──────────┘
                  ▼
         ┌─────────────────┐
         │ LLMService      │
         │ 调用 API 分析   │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ 解析 JSON 结果  │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ 更新 analysis   │
         │ status=completed│
         └─────────────────┘
```

---

## 8. 配置管理

### 环境变量 (.env.example)
```env
# App
APP_NAME=aiops-mvp
APP_ENV=development
DEBUG=true

# Database
DATABASE_URL=sqlite+aiosqlite:///./aiops.db

# Prometheus
PROMETHEUS_URL=http://localhost:9090

# LLM
LLM_PROVIDER=openai  # openai/doubao/qwen
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# Doubao (optional)
# DOUBAO_API_KEY=xxx
# DOUBAO_MODEL=ep-xxx

# Qwen (optional)
# QWEN_API_KEY=xxx
# QWEN_MODEL=qwen-max

# Analysis
ANALYSIS_ENABLED=true
ANALYSIS_TIMEOUT_SECONDS=60
AUTO_ANALYZE_NEW_ALERTS=true
```

---

## 9. 部署说明

### 本地开发
```bash
# 使用 uv 创建环境
uv venv
uv pip install -e .[dev]

# 运行
uv run uvicorn app.main:app --reload
```

### 生产部署
```bash
# 独立运行
uv run uvicorn app.main:app --host 0.0.0.0 --port 5000

# 或使用 systemd/docker
```

### AlertManager 配置
```yaml
receivers:
  - name: 'aiops-webhook'
    webhook_configs:
      - url: 'http://aiops-service:5000/api/v1/alerts/webhook'
        send_resolved: true

route:
  routes:
    - match:
        severity: critical|warning
      receiver: 'aiops-webhook'
      continue: true
```

---

## 10. 后续扩展方向

MVP 完成后，可以考虑：
- 日志异常检测（对接 ELK/Loki）
- 自动生成 Runbook
- 用户反馈与模型微调
- Web UI 控制台
- 多集群支持
- K8s Operator 部署模式

---

## 验证清单

- [x] 目录结构清晰，符合 Python 项目标准
- [x] 数据模型支持告警去重和状态管理
- [x] API 设计符合 RESTful 规范
- [x] 核心服务职责明确
- [x] 使用 uv 管理环境
- [x] 支持商用 LLM API
- [x] 独立部署，纯 API

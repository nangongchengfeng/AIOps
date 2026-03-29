# AIOps MVP - 告警根因分析系统 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个基于 LLM 的告警根因分析系统 MVP，接收 AlertManager webhook，查询 Prometheus 指标，调用商用 LLM API 进行根因分析。

**Architecture:** 轻量级模块化架构，FastAPI + SQLAlchemy + LangChain + SQLite，独立部署，纯 API 服务。

**Tech Stack:** Python 3.10+, FastAPI, SQLAlchemy, Pydantic, LangChain, uv, SQLite

---

## 文件结构总览

```
aiops/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── alerts.py
│   │   │   └── health.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── alert_processor.py
│   │   │   ├── alert_analyzer.py
│   │   │   ├── prometheus_client.py
│   │   │   └── llm_service.py
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── models.py
│   │       └── crud.py
│   ├── tests/
│   │   └── __init__.py
│   ├── pyproject.toml
│   ├── .env.example
│   └── README.md
└── docs/...
```

---

## Task 1: 项目初始化

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/.env.example`
- Create: `backend/README.md`

- [ ] **Step 1.1: 创建 pyproject.toml**

```toml
[project]
name = "aiops-mvp"
version = "0.1.0"
description = "AIOps MVP - Alert Root Cause Analysis"
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
    "aiosqlite>=0.19.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.27.0",
    "black>=24.0",
    "ruff>=0.2.0",
    "mypy>=1.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

- [ ] **Step 1.2: 创建 .env.example**

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
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# Analysis
ANALYSIS_ENABLED=true
ANALYSIS_TIMEOUT_SECONDS=60
AUTO_ANALYZE_NEW_ALERTS=true
```

- [ ] **Step 1.3: 创建 README.md**

```markdown
# AIOps MVP - 告警根因分析系统

基于 LLM 的告警根因分析系统 MVP。

## 功能

- 接收 AlertManager webhook
- 告警去重和状态管理
- 自动查询 Prometheus 相关指标
- 调用 LLM 进行根因分析
- 提供 REST API 查询分析结果

## 快速开始

### 环境要求

- Python 3.10+
- uv

### 安装

​```bash
cd backend
uv venv
uv pip install -e .[dev]
```

### 配置

复制 `.env.example` 为 `.env` 并填入配置：

```bash
cp .env.example .env
# 编辑 .env
```

### 运行

```bash
uv run uvicorn app.main:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档。
```

---

## Task 2: 核心配置和数据库

**Files:**
- Create: `backend/app/__init__.py`
- Create: `backend/app/core/__init__.py`
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/database.py`

- [ ] **Step 2.1: 创建 app/__init__.py**

​```python
__version__ = "0.1.0"
```

- [ ] **Step 2.2: 创建 app/core/__init__.py**

```python
"""Core configuration and utilities."""
```

- [ ] **Step 2.3: 创建 app/core/config.py**

```python
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    app_name: str = "aiops-mvp"
    app_env: str = "development"
    debug: bool = True

    database_url: str = "sqlite+aiosqlite:///./aiops.db"

    prometheus_url: str = "http://localhost:9090"

    llm_provider: Literal["openai", "doubao", "qwen"] = "openai"
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o"

    doubao_api_key: str = ""
    doubao_model: str = ""

    qwen_api_key: str = ""
    qwen_model: str = ""

    analysis_enabled: bool = True
    analysis_timeout_seconds: int = 60
    auto_analyze_new_alerts: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
```

- [ ] **Step 2.4: 创建 app/core/database.py**

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

---

## Task 3: 数据库模型 (SQLAlchemy)

**Files:**
- Create: `backend/app/db/__init__.py`
- Create: `backend/app/db/models.py`

- [ ] **Step 3.1: 创建 app/db/__init__.py**

```python
"""Database models and CRUD operations."""
```

- [ ] **Step 3.2: 创建 app/db/models.py**

```python
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fingerprint = Column(String, unique=True, nullable=False, index=True)
    alert_id = Column(String, index=True)
    group_key = Column(String)
    status = Column(String, nullable=False, index=True)
    alert_name = Column(String, nullable=False, index=True)
    severity = Column(String, index=True)
    summary = Column(String)
    description = Column(Text)
    labels = Column(JSON)
    annotations = Column(JSON)
    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=True)
    update_count = Column(Integer, default=0)
    last_received_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    analyses = relationship("Analysis", back_populates="alert", cascade="all, delete-orphan")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=False, index=True)
    version = Column(Integer, default=1)
    is_latest = Column(Boolean, default=True)
    root_cause = Column(Text)
    possible_solutions = Column(JSON)
    reasoning = Column(Text)
    confidence_score = Column(Float)
    model_used = Column(String)
    status = Column(String, nullable=False)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    alert = relationship("Alert", back_populates="analyses")
```

---

## Task 4: Pydantic Schemas

**Files:**
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/schemas.py`

- [ ] **Step 4.1: 创建 app/models/__init__.py**

```python
"""Pydantic models for API request/response validation."""
```

- [ ] **Step 4.2: 创建 app/models/schemas.py**

```python
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime


class AlertManagerAlert(BaseModel):
    status: str
    labels: Dict[str, str]
    annotations: Dict[str, str]
    startsAt: str
    endsAt: Optional[str] = None
    generatorURL: Optional[str] = None
    fingerprint: str


class AlertManagerWebhook(BaseModel):
    receiver: str
    status: str
    alerts: List[AlertManagerAlert]
    groupLabels: Dict[str, str]
    commonLabels: Dict[str, str]
    commonAnnotations: Dict[str, str]
    externalURL: str
    version: str
    groupKey: str


class WebhookResponse(BaseModel):
    status: str
    processed: int
    created: int
    updated: int


class AlertBase(BaseModel):
    fingerprint: str
    alert_id: Optional[str] = None
    group_key: Optional[str] = None
    status: str
    alert_name: str
    severity: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[Dict[str, Any]] = None
    annotations: Optional[Dict[str, Any]] = None
    starts_at: datetime
    ends_at: Optional[datetime] = None


class AlertCreate(AlertBase):
    last_received_at: datetime


class AlertUpdate(BaseModel):
    status: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[Dict[str, Any]] = None
    annotations: Optional[Dict[str, Any]] = None
    ends_at: Optional[datetime] = None
    last_received_at: datetime


class Alert(AlertBase):
    id: int
    update_count: int
    last_received_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertListResponse(BaseModel):
    items: List[Alert]
    total: int
    limit: int
    offset: int


class AnalysisBase(BaseModel):
    alert_id: int
    version: int = 1
    is_latest: bool = True
    status: str


class AnalysisCreate(AnalysisBase):
    started_at: datetime


class AnalysisResult(BaseModel):
    root_cause: str
    possible_solutions: List[str]
    reasoning: str
    confidence_score: float


class AnalysisUpdate(BaseModel):
    root_cause: Optional[str] = None
    possible_solutions: Optional[List[str]] = None
    reasoning: Optional[str] = None
    confidence_score: Optional[float] = None
    model_used: Optional[str] = None
    status: Optional[str] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None


class Analysis(AnalysisBase):
    id: int
    root_cause: Optional[str] = None
    possible_solutions: Optional[List[str]] = None
    reasoning: Optional[str] = None
    confidence_score: Optional[float] = None
    model_used: Optional[str] = None
    error_message: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    status: str
    version: str


class ReadyResponse(BaseModel):
    status: str
    database: bool
    prometheus: Optional[bool] = None
```

---

## Task 5: CRUD 操作

**Files:**
- Create: `backend/app/db/crud.py`

- [ ] **Step 5.1: 创建 app/db/crud.py**

```python
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.db.models import Alert, Analysis
from app.models.schemas import AlertCreate, AlertUpdate, AnalysisCreate, AnalysisUpdate


class AlertCRUD:
    @staticmethod
    async def get_by_fingerprint(db: AsyncSession, fingerprint: str) -> Optional[Alert]:
        result = await db.execute(select(Alert).where(Alert.fingerprint == fingerprint))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(db: AsyncSession, alert_id: int) -> Optional[Alert]:
        result = await db.execute(select(Alert).where(Alert.id == alert_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_list(
        db: AsyncSession,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[List[Alert], int]:
        query = select(Alert)
        if status:
            query = query.where(Alert.status == status)
        query = query.order_by(desc(Alert.created_at))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_query)).scalar() or 0

        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        items = list(result.scalars().all())
        return items, total

    @staticmethod
    async def create(db: AsyncSession, obj_in: AlertCreate) -> Alert:
        db_obj = Alert(
            fingerprint=obj_in.fingerprint,
            alert_id=obj_in.alert_id,
            group_key=obj_in.group_key,
            status=obj_in.status,
            alert_name=obj_in.alert_name,
            severity=obj_in.severity,
            summary=obj_in.summary,
            description=obj_in.description,
            labels=obj_in.labels,
            annotations=obj_in.annotations,
            starts_at=obj_in.starts_at,
            ends_at=obj_in.ends_at,
            update_count=0,
            last_received_at=obj_in.last_received_at,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def update(db: AsyncSession, db_obj: Alert, obj_in: AlertUpdate) -> Alert:
        update_data = obj_in.model_dump(exclude_unset=True)
        update_data["update_count"] = db_obj.update_count + 1

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj


class AnalysisCRUD:
    @staticmethod
    async def get_by_id(db: AsyncSession, analysis_id: int) -> Optional[Analysis]:
        result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_alert_id(
        db: AsyncSession,
        alert_id: int,
        only_latest: bool = False,
    ) -> List[Analysis]:
        query = select(Analysis).where(Analysis.alert_id == alert_id)
        if only_latest:
            query = query.where(Analysis.is_latest == True)
        query = query.order_by(desc(Analysis.version))
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_latest(db: AsyncSession, limit: int = 10) -> List[Analysis]:
        query = (
            select(Analysis)
            .where(Analysis.is_latest == True)
            .order_by(desc(Analysis.created_at))
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def create(db: AsyncSession, obj_in: AnalysisCreate) -> Analysis:
        await db.execute(
            Analysis.__table__.update()
            .where(and_(Analysis.alert_id == obj_in.alert_id, Analysis.is_latest == True))
            .values(is_latest=False)
        )

        db_obj = Analysis(
            alert_id=obj_in.alert_id,
            version=obj_in.version,
            is_latest=obj_in.is_latest,
            status=obj_in.status,
            started_at=obj_in.started_at,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def update(db: AsyncSession, db_obj: Analysis, obj_in: AnalysisUpdate) -> Analysis:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


from sqlalchemy import func
```

---

## Task 6: Prometheus Client 服务

**Files:**
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/prometheus_client.py`

- [ ] **Step 6.1: 创建 app/services/__init__.py**

```python
"""Business logic services."""
```

- [ ] **Step 6.2: 创建 app/services/prometheus_client.py**

```python
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from prometheus_api_client import PrometheusConnect

from app.core.config import settings

logger = logging.getLogger(__name__)


class PrometheusClient:
    def __init__(self, url: Optional[str] = None):
        self.url = url or settings.prometheus_url
        self._client: Optional[PrometheusConnect] = None

    @property
    def client(self) -> PrometheusConnect:
        if self._client is None:
            self._client = PrometheusConnect(url=self.url, disable_ssl=True)
        return self._client

    async def check_connection(self) -> bool:
        try:
            self.client.all_metrics()
            return True
        except Exception as e:
            logger.warning(f"Failed to connect to Prometheus: {e}")
            return False

    def query(self, query: str, time: Optional[datetime] = None) -> Dict[str, Any]:
        try:
            params = {}
            if time:
                params["time"] = time.timestamp()
            result = self.client.custom_query(query, params=params)
            return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"Prometheus query failed: {query}, error: {e}")
            return {"success": False, "error": str(e), "data": []}

    def query_range(
        self,
        query: str,
        start: datetime,
        end: datetime,
        step: str = "1m",
    ) -> Dict[str, Any]:
        try:
            result = self.client.custom_query_range(
                query,
                start_time=start,
                end_time=end,
                step=step,
            )
            return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"Prometheus query_range failed: {query}, error: {e}")
            return {"success": False, "error": str(e), "data": []}

    def get_related_metrics(
        self,
        alert_labels: Dict[str, str],
        lookback_minutes: int = 30,
    ) -> Dict[str, Any]:
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=lookback_minutes)

        instance = alert_labels.get("instance", "")
        job = alert_labels.get("job", "")
        pod = alert_labels.get("pod", "")
        namespace = alert_labels.get("namespace", "")

        metrics = {}
        queries = []

        if instance:
            queries.append(
                (
                    "cpu_usage",
                    f'rate(container_cpu_usage_seconds_total{{instance="{instance}"}}[5m])',
                )
            )
            queries.append(
                (
                    "memory_usage",
                    f'container_memory_usage_bytes{{instance="{instance}"}}',
                )
            )

        if job:
            queries.append(
                (
                    "job_up",
                    f'up{{job="{job}"}}',
                )
            )
            queries.append(
                (
                    "job_errors",
                    f'rate(http_requests_total{{job="{job}",status=~"5.."}}[5m])',
                )
            )

        if pod and namespace:
            queries.append(
                (
                    "pod_cpu",
                    f'rate(container_cpu_usage_seconds_total{{pod="{pod}",namespace="{namespace}"}}[5m])',
                )
            )
            queries.append(
                (
                    "pod_memory",
                    f'container_memory_usage_bytes{{pod="{pod}",namespace="{namespace}"}}',
                )
            )

        for name, query_str in queries:
            result = self.query_range(query_str, start_time, end_time)
            if result["success"] and result["data"]:
                metrics[name] = result["data"]

        return {
            "lookback_minutes": lookback_minutes,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "metrics": metrics,
        }


prometheus_client = PrometheusClient()
```

---

## Task 7: LLM Service

**Files:**
- Create: `backend/app/services/llm_service.py`

- [ ] **Step 7.1: 创建 app/services/llm_service.py**

```python
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from app.core.config import settings
from app.models.schemas import AnalysisResult

logger = logging.getLogger(__name__)


PROMPT_TEMPLATE = """你是一个经验丰富的 SRE 专家。请分析以下告警并给出根因分析和解决方案建议。

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
"""


class LLMService:
    def __init__(self):
        self._llm: Optional[ChatOpenAI] = None

    @property
    def llm(self) -> ChatOpenAI:
        if self._llm is None:
            if settings.llm_provider == "openai":
                self._llm = ChatOpenAI(
                    model=settings.openai_model,
                    api_key=settings.openai_api_key,
                    base_url=settings.openai_base_url,
                    temperature=0.3,
                )
            else:
                raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
        return self._llm

    def _format_metrics_summary(self, metrics_data: Dict[str, Any]) -> str:
        if not metrics_data or not metrics_data.get("metrics"):
            return "暂无相关指标数据"

        summary_lines = []
        for name, data in metrics_data["metrics"].items():
            if data:
                summary_lines.append(f"- {name}: 有 {len(data)} 个时间序列")
                for series in data[:3]:
                    metric_labels = series.get("metric", {})
                    values = series.get("values", [])
                    if values:
                        last_val = values[-1][1]
                        summary_lines.append(f"  * {metric_labels}: {last_val}")

        return "\n".join(summary_lines) if summary_lines else "暂无相关指标数据"

    def analyze_root_cause(
        self,
        alert_data: Dict[str, Any],
        metrics_data: Dict[str, Any],
    ) -> AnalysisResult:
        metrics_summary = self._format_metrics_summary(metrics_data)

        prompt = PROMPT_TEMPLATE.format(
            alert_name=alert_data.get("alert_name", ""),
            severity=alert_data.get("severity", ""),
            summary=alert_data.get("summary", ""),
            description=alert_data.get("description", ""),
            labels=json.dumps(alert_data.get("labels", {}), ensure_ascii=False),
            starts_at=alert_data.get("starts_at", ""),
            metrics_summary=metrics_summary,
        )

        logger.info(f"Invoking LLM for alert: {alert_data.get('alert_name')}")

        messages = [
            ("system", "你是一个专业的 SRE 专家，擅长告警根因分析。请严格按照 JSON 格式输出。"),
            ("user", prompt),
        ]

        try:
            response = self.llm.invoke(messages)
            content = response.content.strip()

            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            result_json = json.loads(content)

            return AnalysisResult(
                root_cause=result_json.get("root_cause", ""),
                possible_solutions=result_json.get("possible_solutions", []),
                reasoning=result_json.get("reasoning", ""),
                confidence_score=result_json.get("confidence_score", 0.5),
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {content}, error: {e}")
            return AnalysisResult(
                root_cause="LLM 返回结果解析失败",
                possible_solutions=["请检查 LLM 配置"],
                reasoning="JSON 解析失败",
                confidence_score=0.0,
            )
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            raise


llm_service = LLMService()
```

---

## Task 8: Alert Processor（告警处理器）

**Files:**
- Create: `backend/app/services/alert_processor.py`

- [ ] **Step 8.1: 创建 app/services/alert_processor.py**

```python
import logging
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas import (
    AlertManagerWebhook,
    AlertManagerAlert,
    AlertCreate,
    AlertUpdate,
)
from app.db.crud import AlertCRUD
from app.db.models import Alert

logger = logging.getLogger(__name__)


@dataclass
class ProcessResult:
    processed: int = 0
    created: int = 0
    updated: int = 0
    to_analyze: List[int] = None

    def __post_init__(self):
        if self.to_analyze is None:
            self.to_analyze = []


class AlertProcessor:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.alert_crud = AlertCRUD()

    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        if not dt_str:
            return None
        try:
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except ValueError:
            logger.warning(f"Failed to parse datetime: {dt_str}")
            return None

    def _convert_alert(
        self,
        am_alert: AlertManagerAlert,
        group_key: str,
    ) -> AlertCreate:
        labels = am_alert.labels or {}
        annotations = am_alert.annotations or {}

        return AlertCreate(
            fingerprint=am_alert.fingerprint,
            alert_id=labels.get("alertname"),
            group_key=group_key,
            status=am_alert.status,
            alert_name=labels.get("alertname", "unknown"),
            severity=labels.get("severity", "unknown"),
            summary=annotations.get("summary", ""),
            description=annotations.get("description", ""),
            labels=labels,
            annotations=annotations,
            starts_at=self._parse_datetime(am_alert.startsAt) or datetime.now(),
            ends_at=self._parse_datetime(am_alert.endsAt),
            last_received_at=datetime.now(),
        )

    def should_trigger_analysis(
        self,
        alert: Alert,
        old_alert: Optional[Alert],
    ) -> bool:
        if old_alert is None:
            return alert.status == "firing"

        if old_alert.status == "resolved" and alert.status == "firing":
            return True

        return False

    async def process_webhook(
        self,
        webhook: AlertManagerWebhook,
    ) -> ProcessResult:
        result = ProcessResult()

        for am_alert in webhook.alerts:
            result.processed += 1

            alert_in = self._convert_alert(am_alert, webhook.groupKey)

            existing_alert = await self.alert_crud.get_by_fingerprint(
                self.db,
                alert_in.fingerprint,
            )

            if existing_alert is None:
                alert = await self.alert_crud.create(self.db, alert_in)
                result.created += 1
                logger.info(f"Created new alert: {alert.fingerprint}")

                if self.should_trigger_analysis(alert, None):
                    result.to_analyze.append(alert.id)
            else:
                update_in = AlertUpdate(
                    status=alert_in.status,
                    summary=alert_in.summary,
                    description=alert_in.description,
                    labels=alert_in.labels,
                    annotations=alert_in.annotations,
                    ends_at=alert_in.ends_at,
                    last_received_at=alert_in.last_received_at,
                )
                old_status = existing_alert.status
                alert = await self.alert_crud.update(self.db, existing_alert, update_in)
                result.updated += 1
                logger.info(f"Updated alert: {alert.fingerprint}, status: {old_status} -> {alert.status}")

                if self.should_trigger_analysis(alert, existing_alert):
                    result.to_analyze.append(alert.id)

        return result


def get_alert_processor(db: AsyncSession) -> AlertProcessor:
    return AlertProcessor(db)
```

---

## Task 9: Alert Analyzer（根因分析核心）

**Files:**
- Create: `backend/app/services/alert_analyzer.py`

- [ ] **Step 9.1: 创建 app/services/alert_analyzer.py**

```python
import logging
from typing import Dict, Any
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.crud import AlertCRUD, AnalysisCRUD
from app.db.models import Alert, Analysis
from app.models.schemas import AnalysisCreate, AnalysisUpdate, AnalysisResult
from app.services.prometheus_client import prometheus_client
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)


class AlertAnalyzer:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.alert_crud = AlertCRUD()
        self.analysis_crud = AnalysisCRUD()

    async def analyze_alert(self, alert_id: int) -> Analysis:
        alert = await self.alert_crud.get_by_id(self.db, alert_id)
        if not alert:
            raise ValueError(f"Alert {alert_id} not found")

        existing_analyses = await self.analysis_crud.get_by_alert_id(
            self.db,
            alert_id,
            only_latest=True,
        )
        next_version = 1
        if existing_analyses:
            next_version = existing_analyses[0].version + 1

        analysis_in = AnalysisCreate(
            alert_id=alert_id,
            version=next_version,
            is_latest=True,
            status="pending",
            started_at=datetime.now(),
        )
        analysis = await self.analysis_crud.create(self.db, analysis_in)
        logger.info(f"Created analysis {analysis.id} for alert {alert_id}")

        if not settings.analysis_enabled:
            update_in = AnalysisUpdate(
                status="completed",
                root_cause="分析功能已禁用",
                possible_solutions=["启用 ANALYSIS_ENABLED 配置"],
                reasoning="配置禁用",
                confidence_score=0.0,
                model_used="disabled",
                completed_at=datetime.now(),
            )
            return await self.analysis_crud.update(self.db, analysis, update_in)

        try:
            alert_data = {
                "alert_name": alert.alert_name,
                "severity": alert.severity,
                "summary": alert.summary,
                "description": alert.description,
                "labels": alert.labels or {},
                "starts_at": alert.starts_at.isoformat() if alert.starts_at else "",
            }

            metrics_data = {}
            try:
                if alert.labels:
                    metrics_data = prometheus_client.get_related_metrics(alert.labels)
            except Exception as e:
                logger.warning(f"Failed to fetch metrics: {e}")
                metrics_data = {"error": str(e)}

            llm_result: AnalysisResult = llm_service.analyze_root_cause(
                alert_data,
                metrics_data,
            )

            update_in = AnalysisUpdate(
                root_cause=llm_result.root_cause,
                possible_solutions=llm_result.possible_solutions,
                reasoning=llm_result.reasoning,
                confidence_score=llm_result.confidence_score,
                model_used=settings.openai_model,
                status="completed",
                completed_at=datetime.now(),
            )
            analysis = await self.analysis_crud.update(self.db, analysis, update_in)
            logger.info(f"Completed analysis {analysis.id} for alert {alert_id}")

        except Exception as e:
            logger.error(f"Analysis failed for alert {alert_id}: {e}")
            update_in = AnalysisUpdate(
                status="failed",
                error_message=str(e),
                completed_at=datetime.now(),
            )
            analysis = await self.analysis_crud.update(self.db, analysis, update_in)

        return analysis


def get_alert_analyzer(db: AsyncSession) -> AlertAnalyzer:
    return AlertAnalyzer(db)
```

---

## Task 10: API 路由

**Files:**
- Create: `backend/app/api/__init__.py`
- Create: `backend/app/api/health.py`
- Create: `backend/app/api/alerts.py`

- [ ] **Step 10.1: 创建 app/api/__init__.py**

```python
"""API routes."""
```

- [ ] **Step 10.2: 创建 app/api/health.py**

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.models.schemas import HealthResponse, ReadyResponse
from app.services.prometheus_client import prometheus_client

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        version="0.1.0",
    )


@router.get("/ready", response_model=ReadyResponse)
async def ready(db: AsyncSession = Depends(get_db)):
    db_ok = True
    try:
        from sqlalchemy import text
        await db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False

    prom_ok = None
    try:
        prom_ok = await prometheus_client.check_connection()
    except Exception:
        prom_ok = False

    return ReadyResponse(
        status="ok" if (db_ok and (prom_ok is not False)) else "error",
        database=db_ok,
        prometheus=prom_ok,
    )
```

- [ ] **Step 10.3: 创建 app/api/alerts.py**

```python
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.models.schemas import (
    AlertManagerWebhook,
    WebhookResponse,
    Alert,
    AlertListResponse,
    Analysis,
)
from app.services.alert_processor import get_alert_processor
from app.services.alert_analyzer import get_alert_analyzer
from app.db.crud import AlertCRUD, AnalysisCRUD

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alerts", tags=["alerts"])


async def _background_analyze(alert_id: int, db: AsyncSession):
    try:
        analyzer = get_alert_analyzer(db)
        await analyzer.analyze_alert(alert_id)
    except Exception as e:
        logger.error(f"Background analysis failed for alert {alert_id}: {e}")


@router.post("/webhook", response_model=WebhookResponse)
async def receive_webhook(
    webhook: AlertManagerWebhook,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    processor = get_alert_processor(db)
    result = await processor.process_webhook(webhook)

    if settings.auto_analyze_new_alerts and result.to_analyze:
        for alert_id in result.to_analyze:
            background_tasks.add_task(_background_analyze, alert_id, db)

    return WebhookResponse(
        status="ok",
        processed=result.processed,
        created=result.created,
        updated=result.updated,
    )


@router.get("", response_model=AlertListResponse)
async def list_alerts(
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    crud = AlertCRUD()
    items, total = await crud.get_list(db, status=status, limit=limit, offset=offset)
    return AlertListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{alert_id}", response_model=Alert)
async def get_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    crud = AlertCRUD()
    alert = await crud.get_by_id(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.get("/fingerprint/{fingerprint}", response_model=Alert)
async def get_alert_by_fingerprint(fingerprint: str, db: AsyncSession = Depends(get_db)):
    crud = AlertCRUD()
    alert = await crud.get_by_fingerprint(db, fingerprint)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/{alert_id}/analyze", response_model=Analysis)
async def analyze_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    analyzer = get_alert_analyzer(db)
    try:
        return await analyzer.analyze_alert(alert_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{alert_id}/analyses", response_model=list[Analysis])
async def get_alert_analyses(alert_id: int, db: AsyncSession = Depends(get_db)):
    crud = AnalysisCRUD()
    return await crud.get_by_alert_id(db, alert_id)


@router.get("/analyses/latest", response_model=list[Analysis])
async def get_latest_analyses(limit: int = 10, db: AsyncSession = Depends(get_db)):
    crud = AnalysisCRUD()
    return await crud.get_latest(db, limit=limit)
```

---

## Task 11: FastAPI 主入口

**Files:**
- Create: `backend/app/main.py`

- [ ] **Step 11.1: 创建 app/main.py**

```python
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_tables
from app.api import health, alerts

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    await create_tables()
    logger.info("Database tables created")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

---

## Task 12: 测试和运行

**Files:**
- Create: `backend/tests/__init__.py`
- Run: uv 安装依赖和启动服务

- [ ] **Step 12.1: 创建 tests/__init__.py**

```python
"""Tests for AIOps MVP."""
```

- [ ] **Step 12.2: 初始化项目并安装依赖**

```bash
cd backend
uv venv
uv pip install -e .[dev]
```

- [ ] **Step 12.3: 复制并配置 .env**

```bash
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY 等配置
```

- [ ] **Step 12.4: 启动服务**

```bash
uv run uvicorn app.main:app --reload
```

- [ ] **Step 12.5: 验证服务**

访问 http://localhost:8000/docs 查看 Swagger UI

---

## 自检查清单

- [x] Spec 覆盖完整：所有设计文档中的功能都有对应的实现任务
- [x] 无占位符：所有步骤都有完整代码
- [x] 类型一致：方法签名和类型在所有任务中保持一致
- [x] 文件路径正确：所有文件都在 backend/ 目录下的正确位置

"""
Schema 层

提供所有 Pydantic 模型定义，用于请求验证和响应序列化。
"""
from app.schemas.common_schema import (
    HealthResponse,
    ReadyResponse,
    AlertTrendItem,
    AlertTrendResponse,
)
from app.schemas.alert_schema import (
    AlertManagerAlert,
    AlertManagerWebhook,
    WebhookResponse,
    AlertBase,
    AlertCreate,
    AlertUpdate,
    Alert,
    AlertListResponse,
)
from app.schemas.analysis_schema import (
    AnalysisBase,
    AnalysisCreate,
    AnalysisResult,
    AnalysisUpdate,
    Analysis,
)

__all__ = [
    # Common
    "HealthResponse",
    "ReadyResponse",
    "AlertTrendItem",
    "AlertTrendResponse",
    # Alert
    "AlertManagerAlert",
    "AlertManagerWebhook",
    "WebhookResponse",
    "AlertBase",
    "AlertCreate",
    "AlertUpdate",
    "Alert",
    "AlertListResponse",
    # Analysis
    "AnalysisBase",
    "AnalysisCreate",
    "AnalysisResult",
    "AnalysisUpdate",
    "Analysis",
]

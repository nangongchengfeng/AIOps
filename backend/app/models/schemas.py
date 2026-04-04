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


class AlertTrendItem(BaseModel):
    """告警趋势数据项"""
    date: str
    count: int


class AlertTrendResponse(BaseModel):
    """告警趋势响应"""
    items: List[AlertTrendItem]
    total: int

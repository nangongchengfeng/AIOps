"""
告警相关 Schema 模块

定义告警接收、创建、更新等相关的 Pydantic 模型。
"""
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime


class AlertManagerAlert(BaseModel):
    """
    AlertManager 告警格式

    Attributes:
        status: 状态
        labels: 标签
        annotations: 注释
        startsAt: 开始时间
        endsAt: 结束时间
        generatorURL: 生成器 URL
        fingerprint: 指纹
    """
    status: str
    labels: Dict[str, str]
    annotations: Dict[str, str]
    startsAt: str
    endsAt: Optional[str] = None
    generatorURL: Optional[str] = None
    fingerprint: str


class AlertManagerWebhook(BaseModel):
    """
    AlertManager Webhook 格式

    Attributes:
        receiver: 接收者
        status: 状态
        alerts: 告警列表
        groupLabels: 组标签
        commonLabels: 公共标签
        commonAnnotations: 公共注释
        externalURL: 外部 URL
        version: 版本
        groupKey: 组键
    """
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
    """
    Webhook 响应

    Attributes:
        status: 状态
        processed: 处理数量
        created: 创建数量
        updated: 更新数量
    """
    status: str
    processed: int
    created: int
    updated: int


class AlertBase(BaseModel):
    """
    告警基础模型

    Attributes:
        fingerprint: 指纹
        alert_id: 告警 ID
        group_key: 组键
        status: 状态
        alert_name: 告警名称
        severity: 严重程度
        summary: 摘要
        description: 描述
        labels: 标签
        annotations: 注释
        starts_at: 开始时间
        ends_at: 结束时间
    """
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
    """
    告警创建模型

    Attributes:
        last_received_at: 最后接收时间
    """
    last_received_at: datetime


class AlertUpdate(BaseModel):
    """
    告警更新模型

    Attributes:
        status: 状态
        summary: 摘要
        description: 描述
        labels: 标签
        annotations: 注释
        ends_at: 结束时间
        last_received_at: 最后接收时间
    """
    status: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[Dict[str, Any]] = None
    annotations: Optional[Dict[str, Any]] = None
    ends_at: Optional[datetime] = None
    last_received_at: datetime


class Alert(AlertBase):
    """
    告警响应模型

    Attributes:
        id: 主键 ID
        update_count: 更新次数
        last_received_at: 最后接收时间
        created_at: 创建时间
    """
    id: int
    update_count: int
    last_received_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertListResponse(BaseModel):
    """
    告警列表响应

    Attributes:
        items: 告警列表
        total: 总数
        limit: 每页数量
        offset: 偏移量
    """
    items: List[Alert]
    total: int
    limit: int
    offset: int

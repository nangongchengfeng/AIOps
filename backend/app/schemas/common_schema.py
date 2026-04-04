"""
通用 Schema 模块

定义健康检查、趋势统计等通用的 Pydantic 模型。
"""
from pydantic import BaseModel
from typing import List, Optional


class HealthResponse(BaseModel):
    """
    健康检查响应

    Attributes:
        status: 状态
        version: 版本号
    """
    status: str
    version: str


class ReadyResponse(BaseModel):
    """
    就绪检查响应

    Attributes:
        status: 状态
        database: 数据库连接状态
        prometheus: Prometheus 连接状态
    """
    status: str
    database: bool
    prometheus: Optional[bool] = None


class AlertTrendItem(BaseModel):
    """
    告警趋势数据项

    Attributes:
        date: 日期
        count: 告警数量
    """
    date: str
    count: int


class AlertTrendResponse(BaseModel):
    """
    告警趋势响应

    Attributes:
        items: 趋势数据列表
        total: 总数
    """
    items: List[AlertTrendItem]
    total: int

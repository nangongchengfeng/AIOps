"""
分析相关 Schema 模块

定义分析创建、更新、结果等相关的 Pydantic 模型。
"""
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class AnalysisBase(BaseModel):
    """
    分析基础模型

    Attributes:
        alert_id: 告警 ID
        version: 版本号
        is_latest: 是否最新
        status: 状态
    """
    alert_id: int
    version: int = 1
    is_latest: bool = True
    status: str


class AnalysisCreate(AnalysisBase):
    """
    分析创建模型

    Attributes:
        started_at: 开始时间
    """
    started_at: datetime


class AnalysisResult(BaseModel):
    """
    分析结果模型

    Attributes:
        root_cause: 根因分析
        possible_solutions: 可能的解决方案
        reasoning: 推理过程
        confidence_score: 置信度分数
    """
    root_cause: str
    possible_solutions: List[str]
    reasoning: str
    confidence_score: float


class AnalysisUpdate(BaseModel):
    """
    分析更新模型

    Attributes:
        root_cause: 根因分析
        possible_solutions: 可能的解决方案
        reasoning: 推理过程
        confidence_score: 置信度分数
        model_used: 使用的模型
        status: 状态
        error_message: 错误消息
        completed_at: 完成时间
    """
    root_cause: Optional[str] = None
    possible_solutions: Optional[List[str]] = None
    reasoning: Optional[str] = None
    confidence_score: Optional[float] = None
    model_used: Optional[str] = None
    status: Optional[str] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None


class Analysis(AnalysisBase):
    """
    分析响应模型

    Attributes:
        id: 主键 ID
        root_cause: 根因分析
        possible_solutions: 可能的解决方案
        reasoning: 推理过程
        confidence_score: 置信度分数
        model_used: 使用的模型
        error_message: 错误消息
        started_at: 开始时间
        completed_at: 完成时间
        created_at: 创建时间
    """
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

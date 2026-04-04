"""
数据库模型模块

定义所有 SQLAlchemy ORM 模型。
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Alert(Base):
    """
    告警模型

    存储从 AlertManager 接收的告警信息。

    Attributes:
        id: 主键 ID
        fingerprint: 告警指纹（唯一标识）
        alert_id: 告警 ID
        group_key: 组键
        status: 状态（firing/resolved）
        alert_name: 告警名称
        severity: 严重程度
        summary: 摘要
        description: 描述
        labels: 标签（JSON）
        annotations: 注释（JSON）
        starts_at: 开始时间
        ends_at: 结束时间
        update_count: 更新次数
        last_received_at: 最后接收时间
        created_at: 创建时间
    """
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
    """
    分析记录模型

    存储告警的根因分析结果。

    Attributes:
        id: 主键 ID
        alert_id: 关联的告警 ID
        version: 分析版本号
        is_latest: 是否为最新版本
        root_cause: 根因分析
        possible_solutions: 可能的解决方案（JSON 列表）
        reasoning: 推理过程
        confidence_score: 置信度分数
        model_used: 使用的模型
        status: 状态（pending/completed/failed）
        error_message: 错误消息
        started_at: 开始时间
        completed_at: 完成时间
        created_at: 创建时间
    """
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

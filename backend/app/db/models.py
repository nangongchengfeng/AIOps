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

"""
Repository 层

提供数据访问抽象，封装所有数据库操作。
"""
from app.repository.alert_repository import AlertRepository
from app.repository.analysis_repository import AnalysisRepository

__all__ = [
    "AlertRepository",
    "AnalysisRepository",
]

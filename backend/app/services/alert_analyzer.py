"""
告警分析器模块

负责调用 LLM 进行告警根因分析，支持异步后台执行。
"""
import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.repository import AlertRepository, AnalysisRepository
from app.db.models import Analysis
from app.schemas import AnalysisCreate, AnalysisUpdate, AnalysisResult
from app.services.prometheus_client import prometheus_client
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)


class AlertAnalyzer:
    """
    告警分析器

    负责创建分析记录、调用 LLM 进行根因分析、保存分析结果。
    """

    def __init__(self, db: AsyncSession):
        """
        初始化告警分析器

        Args:
            db: 数据库会话
        """
        self.db = db
        self.alert_repository = AlertRepository()
        self.analysis_repository = AnalysisRepository()

    async def create_pending_analysis(self, alert_id: int) -> Analysis:
        """
        创建 pending 状态的分析记录，立即返回

        Args:
            alert_id: 告警 ID

        Returns:
            pending 状态的分析记录

        Raises:
            ValueError: 当告警不存在时
        """
        alert = await self.alert_repository.get_by_id(self.db, alert_id)
        if not alert:
            raise ValueError(f"Alert {alert_id} not found")

        existing_analyses = await self.analysis_repository.get_by_alert_id(
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
        analysis = await self.analysis_repository.create(self.db, analysis_in)
        logger.info(f"Created pending analysis {analysis.id} for alert {alert_id}")
        return analysis

    async def process_analysis_background(self, analysis_id: int):
        """
        后台执行实际的分析逻辑

        Args:
            analysis_id: 分析记录 ID
        """
        try:
            analysis = await self.analysis_repository.get_by_id(self.db, analysis_id)
            if not analysis:
                logger.error(f"Analysis {analysis_id} not found")
                return

            alert = await self.alert_repository.get_by_id(self.db, analysis.alert_id)
            if not alert:
                logger.error(f"Alert {analysis.alert_id} not found")
                return

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
                await self.analysis_repository.update(self.db, analysis, update_in)
                return

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

            llm_result: AnalysisResult = await llm_service.analyze_root_cause(
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
            await self.analysis_repository.update(self.db, analysis, update_in)
            logger.info(f"Completed analysis {analysis_id} for alert {analysis.alert_id}")

        except Exception as e:
            logger.error(f"Background analysis failed for analysis {analysis_id}: {e}")
            try:
                analysis = await self.analysis_repository.get_by_id(self.db, analysis_id)
                if analysis:
                    update_in = AnalysisUpdate(
                        status="failed",
                        error_message=str(e),
                        completed_at=datetime.now(),
                    )
                    await self.analysis_repository.update(self.db, analysis, update_in)
            except Exception as update_error:
                logger.error(f"Failed to update failed analysis: {update_error}")

    async def analyze_alert(self, alert_id: int) -> Analysis:
        """
        同步分析（保留向后兼容）

        Args:
            alert_id: 告警 ID

        Returns:
            分析记录

        Raises:
            ValueError: 当告警不存在时
        """
        alert = await self.alert_repository.get_by_id(self.db, alert_id)
        if not alert:
            raise ValueError(f"Alert {alert_id} not found")

        existing_analyses = await self.analysis_repository.get_by_alert_id(
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
        analysis = await self.analysis_repository.create(self.db, analysis_in)
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
            return await self.analysis_repository.update(self.db, analysis, update_in)

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

            llm_result: AnalysisResult = await llm_service.analyze_root_cause(
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
            analysis = await self.analysis_repository.update(self.db, analysis, update_in)
            logger.info(f"Completed analysis {analysis.id} for alert {alert_id}")

        except Exception as e:
            logger.error(f"Analysis failed for alert {alert_id}: {e}")
            update_in = AnalysisUpdate(
                status="failed",
                error_message=str(e),
                completed_at=datetime.now(),
            )
            analysis = await self.analysis_repository.update(self.db, analysis, update_in)

        return analysis


def get_alert_analyzer(db: AsyncSession) -> AlertAnalyzer:
    """
    获取告警分析器实例

    Args:
        db: 数据库会话

    Returns:
        告警分析器实例
    """
    return AlertAnalyzer(db)

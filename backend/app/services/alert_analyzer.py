import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.crud import AlertCRUD, AnalysisCRUD
from app.db.models import Analysis
from app.models.schemas import AnalysisCreate, AnalysisUpdate, AnalysisResult
from app.services.prometheus_client import prometheus_client
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)


class AlertAnalyzer:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.alert_crud = AlertCRUD()
        self.analysis_crud = AnalysisCRUD()

    async def create_pending_analysis(self, alert_id: int) -> Analysis:
        """创建 pending 状态的分析记录，立即返回"""
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
        logger.info(f"Created pending analysis {analysis.id} for alert {alert_id}")
        return analysis

    async def process_analysis_background(self, analysis_id: int):
        """后台执行实际的分析逻辑"""
        try:
            # 重新获取 db session，因为后台任务可能在不同的上下文中
            analysis = await self.analysis_crud.get_by_id(self.db, analysis_id)
            if not analysis:
                logger.error(f"Analysis {analysis_id} not found")
                return

            alert = await self.alert_crud.get_by_id(self.db, analysis.alert_id)
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
                await self.analysis_crud.update(self.db, analysis, update_in)
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
            await self.analysis_crud.update(self.db, analysis, update_in)
            logger.info(f"Completed analysis {analysis_id} for alert {analysis.alert_id}")

        except Exception as e:
            logger.error(f"Background analysis failed for analysis {analysis_id}: {e}")
            try:
                analysis = await self.analysis_crud.get_by_id(self.db, analysis_id)
                if analysis:
                    update_in = AnalysisUpdate(
                        status="failed",
                        error_message=str(e),
                        completed_at=datetime.now(),
                    )
                    await self.analysis_crud.update(self.db, analysis, update_in)
            except Exception as update_error:
                logger.error(f"Failed to update failed analysis: {update_error}")

    async def analyze_alert(self, alert_id: int) -> Analysis:
        """同步分析（保留向后兼容）"""
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

"""
告警处理器模块

处理 AlertManager Webhook，负责告警的接收、去重和状态管理。
"""
import logging
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import (
    AlertManagerWebhook,
    AlertManagerAlert,
    AlertCreate,
    AlertUpdate,
)
from app.repository import AlertRepository
from app.db.models import Alert

logger = logging.getLogger(__name__)


@dataclass
class ProcessResult:
    """
    Webhook 处理结果

    Attributes:
        processed: 处理的告警数量
        created: 新创建的告警数量
        updated: 更新的告警数量
        to_analyze: 需要分析的告警 ID 列表
    """
    processed: int = 0
    created: int = 0
    updated: int = 0
    to_analyze: List[int] = None

    def __post_init__(self):
        if self.to_analyze is None:
            self.to_analyze = []


class AlertProcessor:
    """
    告警处理器

    负责处理 AlertManager Webhook，进行告警的创建、更新和去重。
    """

    def __init__(self, db: AsyncSession):
        """
        初始化告警处理器

        Args:
            db: 数据库会话
        """
        self.db = db
        self.alert_repository = AlertRepository()

    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        """
        解析日期时间字符串

        Args:
            dt_str: ISO 格式的日期时间字符串

        Returns:
            解析后的 datetime 对象，解析失败返回 None
        """
        if not dt_str:
            return None
        try:
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except ValueError:
            logger.warning(f"Failed to parse datetime: {dt_str}")
            return None

    def _convert_alert(
        self,
        am_alert: AlertManagerAlert,
        group_key: str,
    ) -> AlertCreate:
        """
        将 AlertManager 告警转换为内部格式

        Args:
            am_alert: AlertManager 告警对象
            group_key: 告警组键

        Returns:
            内部告警创建对象
        """
        labels = am_alert.labels or {}
        annotations = am_alert.annotations or {}

        return AlertCreate(
            fingerprint=am_alert.fingerprint,
            alert_id=labels.get("alertname"),
            group_key=group_key,
            status=am_alert.status,
            alert_name=labels.get("alertname", "unknown"),
            severity=labels.get("severity", "unknown"),
            summary=annotations.get("summary", ""),
            description=annotations.get("description", ""),
            labels=labels,
            annotations=annotations,
            starts_at=self._parse_datetime(am_alert.startsAt) or datetime.now(),
            ends_at=self._parse_datetime(am_alert.endsAt),
            last_received_at=datetime.now(),
        )

    def should_trigger_analysis(
        self,
        alert: Alert,
        old_alert: Optional[Alert],
    ) -> bool:
        """
        判断是否需要触发分析

        Args:
            alert: 当前告警对象
            old_alert: 旧的告警对象（如果是新告警则为 None）

        Returns:
            是否需要触发分析
        """
        if old_alert is None:
            return alert.status == "firing"

        if old_alert.status == "resolved" and alert.status == "firing":
            return True

        return False

    async def process_webhook(
        self,
        webhook: AlertManagerWebhook,
    ) -> ProcessResult:
        """
        处理 AlertManager Webhook

        Args:
            webhook: AlertManager Webhook 数据

        Returns:
            处理结果
        """
        result = ProcessResult()

        for am_alert in webhook.alerts:
            result.processed += 1

            alert_in = self._convert_alert(am_alert, webhook.groupKey)

            existing_alert = await self.alert_repository.get_by_fingerprint(
                self.db,
                alert_in.fingerprint,
            )

            if existing_alert is None:
                alert = await self.alert_repository.create(self.db, alert_in)
                result.created += 1
                logger.info(f"Created new alert: {alert.fingerprint}")

                if self.should_trigger_analysis(alert, None):
                    result.to_analyze.append(alert.id)
            else:
                update_in = AlertUpdate(
                    status=alert_in.status,
                    summary=alert_in.summary,
                    description=alert_in.description,
                    labels=alert_in.labels,
                    annotations=alert_in.annotations,
                    ends_at=alert_in.ends_at,
                    last_received_at=alert_in.last_received_at,
                )
                old_status = existing_alert.status
                alert = await self.alert_repository.update(self.db, existing_alert, update_in)
                result.updated += 1
                logger.info(f"Updated alert: {alert.fingerprint}, status: {old_status} -> {alert.status}")

                if self.should_trigger_analysis(alert, existing_alert):
                    result.to_analyze.append(alert.id)

        return result


def get_alert_processor(db: AsyncSession) -> AlertProcessor:
    """
    获取告警处理器实例

    Args:
        db: 数据库会话

    Returns:
        告警处理器实例
    """
    return AlertProcessor(db)

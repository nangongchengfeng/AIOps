import logging
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas import (
    AlertManagerWebhook,
    AlertManagerAlert,
    AlertCreate,
    AlertUpdate,
)
from app.db.crud import AlertCRUD
from app.db.models import Alert

logger = logging.getLogger(__name__)


@dataclass
class ProcessResult:
    processed: int = 0
    created: int = 0
    updated: int = 0
    to_analyze: List[int] = None

    def __post_init__(self):
        if self.to_analyze is None:
            self.to_analyze = []


class AlertProcessor:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.alert_crud = AlertCRUD()

    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
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
        if old_alert is None:
            return alert.status == "firing"

        if old_alert.status == "resolved" and alert.status == "firing":
            return True

        return False

    async def process_webhook(
        self,
        webhook: AlertManagerWebhook,
    ) -> ProcessResult:
        result = ProcessResult()

        for am_alert in webhook.alerts:
            result.processed += 1

            alert_in = self._convert_alert(am_alert, webhook.groupKey)

            existing_alert = await self.alert_crud.get_by_fingerprint(
                self.db,
                alert_in.fingerprint,
            )

            if existing_alert is None:
                alert = await self.alert_crud.create(self.db, alert_in)
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
                alert = await self.alert_crud.update(self.db, existing_alert, update_in)
                result.updated += 1
                logger.info(f"Updated alert: {alert.fingerprint}, status: {old_status} -> {alert.status}")

                if self.should_trigger_analysis(alert, existing_alert):
                    result.to_analyze.append(alert.id)

        return result


def get_alert_processor(db: AsyncSession) -> AlertProcessor:
    return AlertProcessor(db)

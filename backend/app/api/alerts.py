import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.models.schemas import (
    AlertManagerWebhook,
    WebhookResponse,
    Alert,
    AlertListResponse,
    Analysis,
)
from app.services.alert_processor import get_alert_processor
from app.services.alert_analyzer import get_alert_analyzer
from app.db.crud import AlertCRUD, AnalysisCRUD

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alerts", tags=["alerts"])


async def _background_analyze(alert_id: int, db: AsyncSession):
    try:
        analyzer = get_alert_analyzer(db)
        await analyzer.analyze_alert(alert_id)
    except Exception as e:
        logger.error(f"Background analysis failed for alert {alert_id}: {e}")


@router.post("/webhook", response_model=WebhookResponse)
async def receive_webhook(
    webhook: AlertManagerWebhook,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    processor = get_alert_processor(db)
    result = await processor.process_webhook(webhook)

    if settings.auto_analyze_new_alerts and result.to_analyze:
        for alert_id in result.to_analyze:
            background_tasks.add_task(_background_analyze, alert_id, db)

    return WebhookResponse(
        status="ok",
        processed=result.processed,
        created=result.created,
        updated=result.updated,
    )


@router.get("", response_model=AlertListResponse)
async def list_alerts(
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    crud = AlertCRUD()
    items, total = await crud.get_list(db, status=status, limit=limit, offset=offset)
    return AlertListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{alert_id}", response_model=Alert)
async def get_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    crud = AlertCRUD()
    alert = await crud.get_by_id(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.get("/fingerprint/{fingerprint}", response_model=Alert)
async def get_alert_by_fingerprint(fingerprint: str, db: AsyncSession = Depends(get_db)):
    crud = AlertCRUD()
    alert = await crud.get_by_fingerprint(db, fingerprint)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/{alert_id}/analyze", response_model=Analysis)
async def analyze_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    analyzer = get_alert_analyzer(db)
    try:
        return await analyzer.analyze_alert(alert_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{alert_id}/analyses", response_model=list[Analysis])
async def get_alert_analyses(alert_id: int, db: AsyncSession = Depends(get_db)):
    crud = AnalysisCRUD()
    return await crud.get_by_alert_id(db, alert_id)


@router.get("/analyses/latest", response_model=list[Analysis])
async def get_latest_analyses(limit: int = 10, db: AsyncSession = Depends(get_db)):
    crud = AnalysisCRUD()
    return await crud.get_latest(db, limit=limit)

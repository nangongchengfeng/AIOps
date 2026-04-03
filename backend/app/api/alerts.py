import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db, AsyncSessionLocal
from app.core.config import settings
from app.models.schemas import (
    AlertManagerWebhook,
    WebhookResponse,
    Alert,
    AlertListResponse,
    Analysis,
)
from app.services.alert_processor import get_alert_processor
from app.services.alert_analyzer import get_alert_analyzer, AlertAnalyzer
from app.db.crud import AlertCRUD, AnalysisCRUD

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alerts", tags=["alerts"])


async def _background_analyze(alert_id: int):
    """后台分析任务 - 使用独立的数据库 session"""
    db = AsyncSessionLocal()
    try:
        analyzer = get_alert_analyzer(db)
        await analyzer.analyze_alert(alert_id)
    except Exception as e:
        logger.error(f"Background analysis failed for alert {alert_id}: {e}")
    finally:
        await db.close()


async def _background_process_analysis(analysis_id: int):
    """后台处理分析任务 - 使用独立的数据库 session"""
    db = AsyncSessionLocal()
    try:
        analyzer = get_alert_analyzer(db)
        await analyzer.process_analysis_background(analysis_id)
    except Exception as e:
        logger.error(f"Background analysis failed for analysis {analysis_id}: {e}")
    finally:
        await db.close()


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
            background_tasks.add_task(_background_analyze, alert_id)

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
async def analyze_alert(
    alert_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """立即返回 pending 状态，后台异步执行分析"""
    analyzer = get_alert_analyzer(db)
    try:
        # 1. 立即创建 pending 状态的分析记录
        analysis = await analyzer.create_pending_analysis(alert_id=alert_id)
        # 2. 后台异步执行实际分析（使用独立的 db session）
        background_tasks.add_task(_background_process_analysis, analysis.id)
        # 3. 立即返回 pending 状态给前端
        return analysis
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

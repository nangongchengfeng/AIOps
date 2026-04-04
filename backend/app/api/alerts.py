"""
告警 API 模块

提供告警相关的 REST API 接口。
"""
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db, AsyncSessionLocal
from app.core.config import settings
from app.schemas import (
    AlertManagerWebhook,
    WebhookResponse,
    Alert,
    AlertListResponse,
    Analysis,
)
from app.services import get_alert_processor, get_alert_analyzer
from app.repository import AlertRepository, AnalysisRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alerts", tags=["alerts"])


async def _background_analyze(alert_id: int):
    """
    后台分析任务 - 使用独立的数据库 session

    Args:
        alert_id: 告警 ID
    """
    db = AsyncSessionLocal()
    try:
        analyzer = get_alert_analyzer(db)
        await analyzer.analyze_alert(alert_id)
    except Exception as e:
        logger.error(f"Background analysis failed for alert {alert_id}: {e}")
    finally:
        await db.close()


async def _background_process_analysis(analysis_id: int):
    """
    后台处理分析任务 - 使用独立的数据库 session

    Args:
        analysis_id: 分析记录 ID
    """
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
    """
    接收 AlertManager Webhook

    接收 AlertManager 发送的告警，进行处理并存储。
    如果配置了自动分析，会在后台触发分析任务。

    Args:
        webhook: AlertManager Webhook 数据
        background_tasks: 后台任务
        db: 数据库会话

    Returns:
        Webhook 处理结果
    """
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
    """
    获取告警列表

    支持按状态过滤，分页返回告警数据。

    Args:
        status: 告警状态过滤（firing/resolved），可选
        limit: 每页数量，默认 20
        offset: 偏移量，默认 0
        db: 数据库会话

    Returns:
        告警列表
    """
    crud = AlertRepository()
    items, total = await crud.get_list(db, status=status, limit=limit, offset=offset)
    return AlertListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/trend")
async def get_alert_trend(
    days: int = Query(7, ge=1, le=90, description="统计天数，1-90天"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取告警趋势统计

    按日期统计告警数量，用于趋势分析图表。

    Args:
        days: 统计天数，默认 7 天，最大 90 天
        db: 数据库会话

    Returns:
        告警趋势数据
    """
    crud = AlertRepository()
    trend_items = await crud.get_trend(db, days=days)
    total = sum(item["count"] for item in trend_items)
    return {
        "items": trend_items,
        "total": total
    }


@router.get("/fingerprint/{fingerprint}", response_model=Alert)
async def get_alert_by_fingerprint(
    fingerprint: str,
    db: AsyncSession = Depends(get_db)
):
    """
    根据指纹获取告警

    Args:
        fingerprint: 告警指纹
        db: 数据库会话

    Returns:
        告警详情

    Raises:
        HTTPException: 当告警不存在时返回 404
    """
    crud = AlertRepository()
    alert = await crud.get_by_fingerprint(db, fingerprint)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.get("/analyses/latest", response_model=list[Analysis])
async def get_latest_analyses(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    获取最新的分析记录

    Args:
        limit: 返回数量限制，默认 10
        db: 数据库会话

    Returns:
        最新分析记录列表
    """
    crud = AnalysisRepository()
    return await crud.get_latest(db, limit=limit)


@router.get("/{alert_id}", response_model=Alert)
async def get_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    根据 ID 获取告警详情

    Args:
        alert_id: 告警 ID
        db: 数据库会话

    Returns:
        告警详情

    Raises:
        HTTPException: 当告警不存在时返回 404
    """
    crud = AlertRepository()
    alert = await crud.get_by_id(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/{alert_id}/analyze", response_model=Analysis)
async def analyze_alert(
    alert_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    分析告警

    立即返回 pending 状态的分析记录，后台异步执行实际分析。

    Args:
        alert_id: 告警 ID
        background_tasks: 后台任务
        db: 数据库会话

    Returns:
        pending 状态的分析记录

    Raises:
        HTTPException: 当告警不存在时返回 404
    """
    analyzer = get_alert_analyzer(db)
    try:
        analysis = await analyzer.create_pending_analysis(alert_id=alert_id)
        background_tasks.add_task(_background_process_analysis, analysis.id)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{alert_id}/analyses", response_model=list[Analysis])
async def get_alert_analyses(
    alert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    获取告警的分析历史

    Args:
        alert_id: 告警 ID
        db: 数据库会话

    Returns:
        分析记录列表
    """
    crud = AnalysisRepository()
    return await crud.get_by_alert_id(db, alert_id)

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_db
from app.models.schemas import HealthResponse, ReadyResponse
from app.services.prometheus_client import prometheus_client

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        version="0.1.0",
    )


@router.get("/ready", response_model=ReadyResponse)
async def ready(db: AsyncSession = Depends(get_db)):
    db_ok = True
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False

    prom_ok = None
    try:
        prom_ok = await prometheus_client.check_connection()
    except Exception:
        prom_ok = False

    return ReadyResponse(
        status="ok" if (db_ok and (prom_ok is not False)) else "error",
        database=db_ok,
        prometheus=prom_ok,
    )

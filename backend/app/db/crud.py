from sqlalchemy import select, desc, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from datetime import datetime

from app.db.models import Alert, Analysis
from app.models.schemas import AlertCreate, AlertUpdate, AnalysisCreate, AnalysisUpdate


class AlertCRUD:
    @staticmethod
    async def get_by_fingerprint(db: AsyncSession, fingerprint: str) -> Optional[Alert]:
        result = await db.execute(select(Alert).where(Alert.fingerprint == fingerprint))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(db: AsyncSession, alert_id: int) -> Optional[Alert]:
        result = await db.execute(select(Alert).where(Alert.id == alert_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_list(
        db: AsyncSession,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> Tuple[List[Alert], int]:
        query = select(Alert)
        if status:
            query = query.where(Alert.status == status)
        query = query.order_by(desc(Alert.created_at))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_query)).scalar() or 0

        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        items = list(result.scalars().all())
        return items, total

    @staticmethod
    async def create(db: AsyncSession, obj_in: AlertCreate) -> Alert:
        db_obj = Alert(
            fingerprint=obj_in.fingerprint,
            alert_id=obj_in.alert_id,
            group_key=obj_in.group_key,
            status=obj_in.status,
            alert_name=obj_in.alert_name,
            severity=obj_in.severity,
            summary=obj_in.summary,
            description=obj_in.description,
            labels=obj_in.labels,
            annotations=obj_in.annotations,
            starts_at=obj_in.starts_at,
            ends_at=obj_in.ends_at,
            update_count=0,
            last_received_at=obj_in.last_received_at,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def update(db: AsyncSession, db_obj: Alert, obj_in: AlertUpdate) -> Alert:
        update_data = obj_in.model_dump(exclude_unset=True)
        update_data["update_count"] = db_obj.update_count + 1

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj


class AnalysisCRUD:
    @staticmethod
    async def get_by_id(db: AsyncSession, analysis_id: int) -> Optional[Analysis]:
        result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_alert_id(
        db: AsyncSession,
        alert_id: int,
        only_latest: bool = False,
    ) -> List[Analysis]:
        query = select(Analysis).where(Analysis.alert_id == alert_id)
        if only_latest:
            query = query.where(Analysis.is_latest == True)
        query = query.order_by(desc(Analysis.version))
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_latest(db: AsyncSession, limit: int = 10) -> List[Analysis]:
        query = (
            select(Analysis)
            .where(Analysis.is_latest == True)
            .order_by(desc(Analysis.created_at))
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def create(db: AsyncSession, obj_in: AnalysisCreate) -> Analysis:
        await db.execute(
            Analysis.__table__.update()
            .where(and_(Analysis.alert_id == obj_in.alert_id, Analysis.is_latest == True))
            .values(is_latest=False)
        )

        db_obj = Analysis(
            alert_id=obj_in.alert_id,
            version=obj_in.version,
            is_latest=obj_in.is_latest,
            status=obj_in.status,
            started_at=obj_in.started_at,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def update(db: AsyncSession, db_obj: Analysis, obj_in: AnalysisUpdate) -> Analysis:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

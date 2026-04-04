from sqlalchemy import select, desc, and_, func, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from datetime import datetime, timedelta, timezone

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

    @staticmethod
    async def get_trend(
        db: AsyncSession,
        days: int = 7,
    ) -> List[dict]:
        """
        获取告警趋势统计

        Args:
            db: 数据库会话
            days: 统计天数，默认7天

        Returns:
            按日期统计的告警数量列表，格式: [{"date": "2024-01-01", "count": 10}, ...]
        """
        # 使用 UTC 时间计算日期范围
        now_utc = datetime.now(timezone.utc)
        end_date = now_utc.date()
        start_date = end_date - timedelta(days=days - 1)

        # 先查询所有告警用于调试
        debug_query = select(Alert.id, Alert.created_at)
        debug_result = await db.execute(debug_query)
        all_alerts = debug_result.all()
        print(f"[DEBUG] Total alerts in DB: {len(all_alerts)}")
        for alert in all_alerts:
            print(f"[DEBUG] Alert {alert.id}: created_at={alert.created_at}, date={alert.created_at.date()}")

        # 按日期统计告警数量 - 使用时区安全的方式
        query = (
            select(
                func.date(Alert.created_at).label("date"),
                func.count(Alert.id).label("count")
            )
            .where(func.date(Alert.created_at) >= start_date)
            .group_by(func.date(Alert.created_at))
            .order_by(func.date(Alert.created_at))
        )

        result = await db.execute(query)
        rows = result.all()
        print(f"[DEBUG] Query result rows: {rows}")

        # 创建日期字典，确保每一天都有数据（没有数据的补0）
        trend_dict = {}
        for i in range(days):
            date = start_date + timedelta(days=i)
            trend_dict[date.isoformat()] = 0
        print(f"[DEBUG] Expected dates: {list(trend_dict.keys())}")

        # 填充实际数据
        for row in rows:
            date_str = row.date.isoformat() if hasattr(row.date, 'isoformat') else str(row.date)
            print(f"[DEBUG] Row date: {date_str}, count: {row.count}")
            if date_str in trend_dict:
                trend_dict[date_str] = row.count
            else:
                print(f"[DEBUG] Date {date_str} not in expected dates")

        # 转换为列表格式
        trend_list = [
            {"date": date, "count": count}
            for date, count in trend_dict.items()
        ]
        print(f"[DEBUG] Final trend list: {trend_list}")

        return trend_list


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

"""
告警数据访问模块

封装所有告警相关的数据库操作。
"""
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from datetime import datetime, timedelta, timezone

from app.db.models import Alert
from app.schemas import AlertCreate, AlertUpdate


class AlertRepository:
    """
    告警数据访问类

    提供告警的增删改查操作。
    """

    @staticmethod
    async def get_by_fingerprint(
        db: AsyncSession,
        fingerprint: str
    ) -> Optional[Alert]:
        """
        根据指纹获取告警

        Args:
            db: 数据库会话
            fingerprint: 告警指纹

        Returns:
            告警对象，如果不存在则返回 None
        """
        result = await db.execute(select(Alert).where(Alert.fingerprint == fingerprint))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        alert_id: int
    ) -> Optional[Alert]:
        """
        根据 ID 获取告警

        Args:
            db: 数据库会话
            alert_id: 告警 ID

        Returns:
            告警对象，如果不存在则返回 None
        """
        result = await db.execute(select(Alert).where(Alert.id == alert_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_list(
        db: AsyncSession,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> Tuple[List[Alert], int]:
        """
        获取告警列表

        Args:
            db: 数据库会话
            status: 状态过滤，可选
            limit: 每页数量
            offset: 偏移量

        Returns:
            (告警列表, 总数)
        """
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
    async def create(
        db: AsyncSession,
        obj_in: AlertCreate
    ) -> Alert:
        """
        创建告警

        Args:
            db: 数据库会话
            obj_in: 告警创建数据

        Returns:
            创建的告警对象
        """
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
    async def update(
        db: AsyncSession,
        db_obj: Alert,
        obj_in: AlertUpdate
    ) -> Alert:
        """
        更新告警

        Args:
            db: 数据库会话
            db_obj: 数据库中的告警对象
            obj_in: 更新数据

        Returns:
            更新后的告警对象
        """
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
            days: 统计天数，默认 7 天

        Returns:
            按日期统计的告警数量列表，格式: [{"date": "2024-01-01", "count": 10}, ...]
        """
        now_utc = datetime.now(timezone.utc)
        end_date = now_utc.date()
        start_date = end_date - timedelta(days=days - 1)

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

        trend_dict = {}
        for i in range(days):
            date = start_date + timedelta(days=i)
            trend_dict[date.isoformat()] = 0

        for row in rows:
            date_str = row.date.isoformat() if hasattr(row.date, 'isoformat') else str(row.date)
            if date_str in trend_dict:
                trend_dict[date_str] = row.count

        trend_list = [
            {"date": date, "count": count}
            for date, count in trend_dict.items()
        ]

        return trend_list

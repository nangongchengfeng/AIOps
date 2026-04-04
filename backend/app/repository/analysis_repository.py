"""
分析数据访问模块

封装所有分析相关的数据库操作。
"""
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.models import Analysis
from app.schemas import AnalysisCreate, AnalysisUpdate


class AnalysisRepository:
    """
    分析数据访问类

    提供分析记录的增删改查操作。
    """

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        analysis_id: int
    ) -> Optional[Analysis]:
        """
        根据 ID 获取分析记录

        Args:
            db: 数据库会话
            analysis_id: 分析记录 ID

        Returns:
            分析记录对象，如果不存在则返回 None
        """
        result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_alert_id(
        db: AsyncSession,
        alert_id: int,
        only_latest: bool = False,
    ) -> List[Analysis]:
        """
        根据告警 ID 获取分析记录列表

        Args:
            db: 数据库会话
            alert_id: 告警 ID
            only_latest: 是否只获取最新版本

        Returns:
            分析记录列表
        """
        query = select(Analysis).where(Analysis.alert_id == alert_id)
        if only_latest:
            query = query.where(Analysis.is_latest == True)
        query = query.order_by(desc(Analysis.version))
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_latest(
        db: AsyncSession,
        limit: int = 10
    ) -> List[Analysis]:
        """
        获取最新的分析记录

        Args:
            db: 数据库会话
            limit: 返回数量限制

        Returns:
            分析记录列表
        """
        query = (
            select(Analysis)
            .where(Analysis.is_latest == True)
            .order_by(desc(Analysis.created_at))
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def create(
        db: AsyncSession,
        obj_in: AnalysisCreate
    ) -> Analysis:
        """
        创建分析记录

        会自动将该告警的其他分析记录的 is_latest 设置为 False。

        Args:
            db: 数据库会话
            obj_in: 分析创建数据

        Returns:
            创建的分析记录对象
        """
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
    async def update(
        db: AsyncSession,
        db_obj: Analysis,
        obj_in: AnalysisUpdate
    ) -> Analysis:
        """
        更新分析记录

        Args:
            db: 数据库会话
            db_obj: 数据库中的分析记录对象
            obj_in: 更新数据

        Returns:
            更新后的分析记录对象
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

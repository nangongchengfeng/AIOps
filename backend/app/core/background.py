"""独立的后台任务管理器，不阻塞事件循环"""
import asyncio
import logging
from typing import Set
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)

# 存储所有运行中的后台任务
_running_tasks: Set[asyncio.Task] = set()


def get_new_db_session() -> AsyncSession:
    """创建一个新的数据库 session（不依赖请求上下文）"""
    return AsyncSessionLocal()


async def run_background_task(coro):
    """运行后台任务，自动管理生命周期"""
    task = asyncio.create_task(coro)
    _running_tasks.add(task)
    try:
        await task
    except Exception as e:
        logger.error(f"Background task failed: {e}")
    finally:
        _running_tasks.discard(task)


def start_background_task(coro):
    """启动后台任务，非阻塞"""
    asyncio.create_task(run_background_task(coro))

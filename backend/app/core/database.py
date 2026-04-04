"""
数据库配置模块

配置 SQLAlchemy 异步引擎和会话管理。
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings


# SQLite 不支持连接池参数，仅在非 SQLite 数据库时使用
engine_kwargs = {}
if "sqlite" not in settings.database_url:
    engine_kwargs = {
        "pool_size": 20,
        "max_overflow": 40,
        "pool_timeout": 30,
    }

# 创建异步引擎
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    **engine_kwargs,
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 声明基类
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    获取数据库会话依赖

    用于 FastAPI 的 Depends 注入，自动管理会话的生命周期。

    Yields:
        异步数据库会话
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    """
    创建数据库表

    在应用启动时调用，创建所有定义的数据库表。
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

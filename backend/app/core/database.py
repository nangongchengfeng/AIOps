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

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    **engine_kwargs,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

"""
应用入口模块

FastAPI 应用的初始化和配置。
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_tables
from app.api import health, alerts

# 配置日志
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    在应用启动时创建数据库表，在关闭时进行清理。

    Args:
        app: FastAPI 应用实例
    """
    logger.info("Starting up...")
    await create_tables()
    logger.info("Database tables created")
    yield
    logger.info("Shutting down...")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router, tags=["health"])
app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])


@app.get("/")
async def root():
    """
    根路径

    返回应用基本信息和文档链接。

    Returns:
        应用信息
    """
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

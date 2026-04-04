"""
配置模块

使用 Pydantic Settings 管理应用配置，支持从环境变量和 .env 文件加载。
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


# 获取项目根目录（backend 目录）
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    应用配置类

    所有配置项都可以通过环境变量覆盖，环境变量名称为大写形式。

    Attributes:
        app_name: 应用名称
        app_env: 应用环境
        debug: 是否开启调试模式
        database_url: 数据库连接 URL
        prometheus_url: Prometheus 地址
        openai_api_key: OpenAI API 密钥
        openai_base_url: OpenAI API 基础 URL
        openai_model: OpenAI 模型名称
        doubao_api_key: 豆包 API 密钥
        doubao_model: 豆包模型名称
        qwen_api_key: 通义千问 API 密钥
        qwen_model: 通义千问模型名称
        analysis_enabled: 是否启用分析功能
        analysis_timeout_seconds: 分析超时时间（秒）
        auto_analyze_new_alerts: 是否自动分析新告警
    """
    app_name: str = "aiops-mvp"
    app_env: str = "development"
    debug: bool = True

    database_url: str = "sqlite+aiosqlite:///./aiops.db"

    prometheus_url: str = "http://localhost:9090"

    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o"

    doubao_api_key: str = ""
    doubao_model: str = ""

    qwen_api_key: str = ""
    qwen_model: str = ""

    analysis_enabled: bool = True
    analysis_timeout_seconds: int = 60
    auto_analyze_new_alerts: bool = True

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# 全局配置实例
settings = Settings()

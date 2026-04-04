from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path


# 获取项目根目录（backend 目录）
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
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


settings = Settings()

# 打印配置用于调试
print("=" * 60)
print("Configuration:")
print(f"  OPENAI_API_KEY: {'set' if settings.openai_api_key else 'not set'}")
print(f"  OPENAI_BASE_URL: {settings.openai_base_url}")
print(f"  OPENAI_MODEL: {settings.openai_model}")
print(f"  Environment variables from os.environ:")
print(f"    OPENAI_API_KEY: {'set' if os.environ.get('OPENAI_API_KEY') else 'not set'}")
print(f"    OPENAI_BASE_URL: {os.environ.get('OPENAI_BASE_URL', 'not set')}")
print("=" * 60)

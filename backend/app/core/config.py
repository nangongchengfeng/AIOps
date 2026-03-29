from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    app_name: str = "aiops-mvp"
    app_env: str = "development"
    debug: bool = True

    database_url: str = "sqlite+aiosqlite:///./aiops.db"

    prometheus_url: str = "http://localhost:9090"

    llm_provider: Literal["openai", "doubao", "qwen"] = "openai"
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

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

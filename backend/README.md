# AIOps MVP - 告警根因分析系统

基于 LLM 的告警根因分析系统 MVP。

## 功能

- 接收 AlertManager webhook
- 告警去重和状态管理
- 自动查询 Prometheus 相关指标
- 调用 LLM 进行根因分析
- 提供 REST API 查询分析结果

## 快速开始

### 环境要求

- Python 3.10+
- uv

### 安装

```bash
cd backend
uv venv
uv pip install -e .[dev]
```

### 配置

复制 `.env.example` 为 `.env` 并填入配置：

```bash
cp .env.example .env
# 编辑 .env
```

### 运行

```bash
uv run uvicorn app.main:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档。

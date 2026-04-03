## 项目概述
基于 FastAPI 构建的高性能 Python 后端服务，采用分层架构设计。
**技术栈：** Python 3.11+ | FastAPI | uv | Pydantic | SQLAlchemy | PostgreSQL/MySQL | Redis | Alembic | Docker | Pytest | Loguru

## 快速开始
```bash
# 创建虚拟环境
uv venv
source .venv/bin/activate
# 安装依赖
uv pip install -r requirements.txt
# 开发模式
uvicorn app.main:app --reload
# 生产运行
python run.py
# 测试
pytest
```
## 目录结构
```
app/
├── api/           # 接口层（路由）
├── core/          # 核心配置
├── models/        # 数据库模型
├── schemas/       # Pydantic模型
├── services/      # 业务逻辑
├── repository/    # 数据访问层
├── utils/         # 工具函数
├── middleware/    # 中间件
├── tasks/         # 定时任务
└── main.py        # 入口
tests/             # 测试
migrations/        # 数据库迁移
scripts/           # 脚本
```
## 开发规范
### 核心原则
- **分层清晰**：API → Service → Repository
- **中文注释**：所有代码必须包含中文注释
- **接口文档**：所有接口必须写 docstring
- **代码限制**：函数≤50行，文件≤500行
### 命名规范
- 文件：`user_service.py`, `order_repository.py`
- 类：`UserService`, `OrderRepository`
- 函数：`get_user()`, `create_order()`
### 路由示例
```python
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    """获取用户信息"""
    return await user_service.get_user(user_id)
```
## 数据管理
### 数据库
- 使用 SQLAlchemy + Alembic
- 禁止直接写 SQL
- Repository 层封装所有数据库操作
### 统一响应格式
```json
{
    "code": 0,
    "message": "success",
    "data": {}
}
```
## 配置与部署
### 环境配置
使用 `.env` + `pydantic_settings` 管理配置
### Docker
```bash
docker build -t project .
docker-compose up -d
```
## 开发流程
1. 创建功能分支：`feature/user-api`
2. 开发代码（带中文注释）
3. 编写测试
4. 运行检查：`pytest && ruff check . && ruff format .`
5. 提交代码（遵循 Conventional Commits）
## 安全规范
- 接口鉴权
- 日志脱敏
- SQL 注入防护
- Token 校验
- 限流
## 禁止事项
- ❌ 直接操作数据库
- ❌ 在 API 层写业务逻辑
- ❌ 提交 .env 文件
- ❌ 修改 migrations 历史文件
"""
统一响应格式模块

提供标准化的 API 响应格式，包含 code、message、data 三个字段。
"""
from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, ConfigDict

T = TypeVar('T')


class Response(BaseModel, Generic[T]):
    """
    统一响应格式

    Attributes:
        code: 状态码，0 表示成功，非 0 表示失败
        message: 响应消息
        data: 响应数据
    """
    code: int = 0
    message: str = "success"
    data: Optional[T] = None

    model_config = ConfigDict(from_attributes=True)


class ListData(BaseModel, Generic[T]):
    """
    列表数据包装

    Attributes:
        items: 数据项列表
        total: 总数
        limit: 每页数量
        offset: 偏移量
    """
    items: List[T]
    total: int
    limit: int
    offset: int


def success(data: Any = None, message: str = "success") -> Response[Any]:
    """
    成功响应

    Args:
        data: 响应数据
        message: 响应消息

    Returns:
        统一格式的成功响应
    """
    return Response(code=0, message=message, data=data)


def error(code: int = 1, message: str = "error") -> Response[Any]:
    """
    错误响应

    Args:
        code: 错误码
        message: 错误消息

    Returns:
        统一格式的错误响应
    """
    return Response(code=code, message=message, data=None)

"""
Pydantic模型 - 用于请求和响应的数据验证
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


# ============ 请求模型 ============

class ContentCreateRequest(BaseModel):
    """创建内容请求"""
    type: str = Field(..., description="内容类型: video 或 article")
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    url: Optional[str] = Field(None, description="原始链接")
    source: Optional[str] = Field(None, description="来源平台")
    author: Optional[str] = Field(None, description="作者")
    metadata: Optional[dict] = Field(None, description="额外元数据")
    auto_analyze: bool = Field(True, description="是否自动触发LLM解析")


class ContentUpdateRequest(BaseModel):
    """更新内容请求"""
    title: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None


class SearchRequest(BaseModel):
    """搜索请求"""
    query: str = Field(..., description="搜索关键词")
    limit: int = Field(20, ge=1, le=100, description="返回结果数量")
    content_type: Optional[str] = Field(None, description="过滤内容类型")
    use_llm_summary: bool = Field(False, description="是否使用LLM生成总结")


class ReanalyzeRequest(BaseModel):
    """重新分析请求"""
    content_id: int = Field(..., description="内容ID")


# ============ 响应模型 ============

class ContentResponse(BaseModel):
    """内容响应"""
    id: int
    type: str
    title: str
    url: Optional[str]
    content: str
    summary: str
    keywords: List[str]
    category: str
    source: Optional[str]
    author: Optional[str]
    media_path: Optional[str]
    metadata: Optional[dict]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True


class ContentListResponse(BaseModel):
    """内容列表响应"""
    total: int
    items: List[ContentResponse]


class SearchResponse(BaseModel):
    """搜索响应"""
    query: str
    total: int
    items: List[ContentResponse]
    summary: Optional[str] = None


# ============ 通用响应 ============

class MessageResponse(BaseModel):
    """消息响应"""
    message: str
    success: bool = True

"""
API路由 - 内容管理接口
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.services.content_service import content_service
from app.services.llm_service import llm_service
from app.api.schemas import (
    ContentCreateRequest,
    ContentUpdateRequest,
    SearchRequest,
    ReanalyzeRequest,
    ContentResponse,
    ContentListResponse,
    SearchResponse,
    MessageResponse
)

router = APIRouter(prefix="/api/content", tags=["content"])


@router.post("/add", response_model=ContentResponse)
async def add_content(
    request: ContentCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """添加新内容"""
    try:
        content = await content_service.create_content(
            db=db,
            content_type=request.type,
            title=request.title,
            content=request.content,
            url=request.url,
            source=request.source,
            author=request.author,
            metadata=request.metadata,
            auto_analyze=request.auto_analyze
        )
        return ContentResponse.from_orm(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加内容失败: {str(e)}")


@router.get("/list", response_model=ContentListResponse)
async def list_contents(
    skip: int = 0,
    limit: int = 20,
    content_type: str = None,
    category: str = None,
    db: AsyncSession = Depends(get_db)
):
    """获取内容列表"""
    try:
        contents = await content_service.list_contents(
            db=db,
            skip=skip,
            limit=limit,
            content_type=content_type,
            category=category
        )
        return ContentListResponse(
            total=len(contents),
            items=[ContentResponse.from_orm(c) for c in contents]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取列表失败: {str(e)}")


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取内容详情"""
    content = await content_service.get_content(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    return ContentResponse.from_orm(content)


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    request: ContentUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    """更新内容"""
    content = await content_service.update_content(
        db=db,
        content_id=content_id,
        **{k: v for k, v in request.dict().items() if v is not None}
    )
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    return ContentResponse.from_orm(content)


@router.delete("/{content_id}", response_model=MessageResponse)
async def delete_content(
    content_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除内容"""
    success = await content_service.delete_content(db, content_id)
    if not success:
        raise HTTPException(status_code=404, detail="内容不存在")
    return MessageResponse(message="删除成功")


@router.post("/reanalyze", response_model=ContentResponse)
async def reanalyze_content(
    request: ReanalyzeRequest,
    db: AsyncSession = Depends(get_db)
):
    """重新分析内容"""
    if not llm_service:
        raise HTTPException(status_code=500, detail="LLM服务未配置")

    content = await content_service.reanalyze_content(db, request.content_id)
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    return ContentResponse.from_orm(content)

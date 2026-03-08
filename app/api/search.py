"""
搜索API路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.content_service import content_service
from app.services.llm_service import llm_service
from app.api.schemas import (
    SearchRequest,
    SearchResponse,
    ContentResponse
)

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("", response_model=SearchResponse)
async def search_content(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """搜索内容"""
    try:
        # 执行搜索
        contents = await content_service.search_contents(
            db=db,
            query=request.query,
            limit=request.limit,
            content_type=request.content_type
        )

        # 构建响应
        items = [ContentResponse.from_orm(c) for c in contents]

        # 如果需要LLM总结且有LLM服务
        summary = None
        if request.use_llm_summary and llm_service:
            try:
                contents_dict = [c.to_dict() for c in contents]
                summary = await llm_service.search_summarize(
                    query=request.query,
                    contents=contents_dict
                )
            except Exception as e:
                print(f"LLM总结失败: {e}")

        return SearchResponse(
            query=request.query,
            total=len(items),
            items=items,
            summary=summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

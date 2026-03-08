"""
内容服务 - 管理内容的增删改查
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Content
from app.services.llm_service import llm_service
from app.core.config import settings


class ContentService:
    """内容服务类"""

    @staticmethod
    async def create_content(
        db: AsyncSession,
        content_type: str,
        title: str,
        content: str,
        url: Optional[str] = None,
        source: Optional[str] = None,
        author: Optional[str] = None,
        media_path: Optional[str] = None,
        metadata: Optional[dict] = None,
        auto_analyze: bool = True
    ) -> Content:
        """
        创建新内容

        Args:
            db: 数据库会话
            content_type: 内容类型 (video/article)
            title: 标题
            content: 内容
            url: 原始链接
            source: 来源平台
            author: 作者
            media_path: 媒体文件路径
            metadata: 额外元数据
            auto_analyze: 是否自动触发LLM解析

        Returns:
            创建的内容对象
        """
        # 初始化字段
        summary = ""
        keywords = []
        category = "未分类"

        # 如果启用自动解析且有LLM服务
        if auto_analyze and llm_service:
            try:
                analysis_result = await llm_service.analyze_content(
                    content_type=content_type,
                    title=title,
                    content=content
                )
                summary = analysis_result.get("summary", "")
                keywords = analysis_result.get("keywords", [])
                category = analysis_result.get("category", "未分类")
            except Exception as e:
                print(f"自动解析失败: {e}")

        # 创建内容对象
        db_content = Content(
            type=content_type,
            title=title,
            url=url,
            content=content,
            summary=summary,
            keywords=keywords,
            category=category,
            source=source,
            author=author,
            media_path=media_path,
            metadata=metadata or {}
        )

        db.add(db_content)
        await db.commit()
        await db.refresh(db_content)

        return db_content

    @staticmethod
    async def get_content(db: AsyncSession, content_id: int) -> Optional[Content]:
        """获取单个内容"""
        result = await db.execute(select(Content).where(Content.id == content_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def list_contents(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        content_type: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Content]:
        """获取内容列表"""
        query = select(Content).order_by(Content.created_at.desc())

        # 添加过滤条件
        conditions = []
        if content_type:
            conditions.append(Content.type == content_type)
        if category:
            conditions.append(Content.category == category)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def search_contents(
        db: AsyncSession,
        query: str,
        skip: int = 0,
        limit: int = 20,
        content_type: Optional[str] = None
    ) -> List[Content]:
        """搜索内容"""
        # 构建搜索条件：在标题、内容、总结、关键词中搜索
        search_pattern = f"%{query}%"
        conditions = [
            or_(
                Content.title.like(search_pattern),
                Content.content.like(search_pattern),
                Content.summary.like(search_pattern)
            )
        ]

        # 如果有关键词，也在关键词中搜索
        # 注意：JSON字段的搜索依赖于数据库类型，这里使用LIKE简化处理

        if content_type:
            conditions.append(Content.type == content_type)

        # 如果有多个条件，需要用AND组合
        if len(conditions) > 1:
            final_condition = and_(*conditions)
        else:
            final_condition = conditions[0]

        query = (
            select(Content)
            .where(final_condition)
            .order_by(Content.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_content(
        db: AsyncSession,
        content_id: int,
        **kwargs
    ) -> Optional[Content]:
        """更新内容"""
        db_content = await ContentService.get_content(db, content_id)
        if not db_content:
            return None

        for key, value in kwargs.items():
            if hasattr(db_content, key):
                setattr(db_content, key, value)

        db_content.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_content)

        return db_content

    @staticmethod
    async def delete_content(db: AsyncSession, content_id: int) -> bool:
        """删除内容"""
        db_content = await ContentService.get_content(db, content_id)
        if not db_content:
            return False

        await db.delete(db_content)
        await db.commit()
        return True

    @staticmethod
    async def reanalyze_content(
        db: AsyncSession,
        content_id: int
    ) -> Optional[Content]:
        """重新分析内容"""
        db_content = await ContentService.get_content(db, content_id)
        if not db_content or not llm_service:
            return None

        try:
            analysis_result = await llm_service.analyze_content(
                content_type=db_content.type,
                title=db_content.title,
                content=db_content.content
            )

            db_content.summary = analysis_result.get("summary", "")
            db_content.keywords = analysis_result.get("keywords", [])
            db_content.category = analysis_result.get("category", "未分类")
            db_content.updated_at = datetime.utcnow()

            await db.commit()
            await db.refresh(db_content)

            return db_content

        except Exception as e:
            print(f"重新分析失败: {e}")
            return None


# 全局内容服务实例
content_service = ContentService()

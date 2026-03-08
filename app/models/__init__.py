"""
数据库模型定义
"""
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Content(Base):
    """内容表 - 存储微信短视频和文章"""
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)  # video/article
    title = Column(String(500))
    url = Column(String(1000))  # 原始链接
    content = Column(Text)  # 正文内容
    summary = Column(Text)  # LLM生成的总结
    keywords = Column(JSON)  # 提取的关键词列表
    category = Column(String(200))  # 分类标签
    source = Column(String(100))  # 来源平台
    author = Column(String(200))  # 作者
    media_path = Column(String(1000))  # 本地媒体文件路径
    metadata = Column(JSON)  # 额外元数据（如视频时长、阅读量等）
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "url": self.url,
            "content": self.content,
            "summary": self.summary,
            "keywords": self.keywords,
            "category": self.category,
            "source": self.source,
            "author": self.author,
            "media_path": self.media_path,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

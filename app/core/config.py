"""
核心配置
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings(BaseSettings):
    """应用配置"""

    # 应用基础配置
    APP_NAME: str = "Favorites - 微信内容智能收藏系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/favorites.db"

    # 存储配置
    STORAGE_PATH: str = "./storage"
    VIDEO_STORAGE_PATH: str = "./storage/videos"
    IMAGE_STORAGE_PATH: str = "./storage/images"

    # LLM配置
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")  # openai/glm/deepseek
    LLM_API_KEY: Optional[str] = os.getenv("LLM_API_KEY")
    LLM_API_BASE: Optional[str] = os.getenv("LLM_API_BASE")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

    # OpenAI配置
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_API_BASE: Optional[str] = os.getenv("OPENAI_API_BASE")

    # GLM配置
    GLM_API_KEY: Optional[str] = os.getenv("GLM_API_KEY")

    # DeepSeek配置
    DEEPSEEK_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")

    # 自动解析配置
    AUTO_ANALYZE: bool = True  # 是否自动触发LLM解析

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()

# 确保存储目录存在
Path(settings.STORAGE_PATH).mkdir(parents=True, exist_ok=True)
Path(settings.VIDEO_STORAGE_PATH).mkdir(parents=True, exist_ok=True)
Path(settings.IMAGE_STORAGE_PATH).mkdir(parents=True, exist_ok=True)
Path("./data").mkdir(parents=True, exist_ok=True)

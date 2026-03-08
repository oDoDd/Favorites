"""
LLM服务 - 用于内容解析和知识点提取
"""
import json
from typing import Dict, List, Optional
from openai import AsyncOpenAI
from app.core.config import settings


class LLMService:
    """LLM服务类"""

    def __init__(self):
        """初始化LLM客户端"""
        self.provider = settings.LLM_PROVIDER.lower()

        # 根据配置选择不同的LLM提供商
        if self.provider == "openai":
            api_key = settings.OPENAI_API_KEY or settings.LLM_API_KEY
            api_base = settings.OPENAI_API_BASE or settings.LLM_API_BASE
            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url=api_base
            )
        elif self.provider == "deepseek":
            api_key = settings.DEEPSEEK_API_KEY or settings.LLM_API_KEY
            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
        elif self.provider == "glm":
            api_key = settings.GLM_API_KEY or settings.LLM_API_KEY
            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://open.bigmodel.cn/api/paas/v4"
            )
        else:
            raise ValueError(f"不支持的LLM提供商: {self.provider}")

        self.model = settings.LLM_MODEL

    async def analyze_content(
        self,
        content_type: str,
        title: str,
        content: str,
        max_tokens: int = 2000
    ) -> Dict:
        """
        分析内容，提取关键知识点

        Args:
            content_type: 内容类型 (video/article)
            title: 标题
            content: 内容
            max_tokens: 最大token数

        Returns:
            包含summary, keywords, category的字典
        """
        system_prompt = """你是一个智能内容分析师，专门分析微信短视频和公众号文章。

你的任务是：
1. 用简洁的语言总结内容的核心观点和关键信息（200字以内）
2. 提取5-10个关键词，这些关键词应该能够准确反映内容的主要话题和关键信息
3. 给出一个合适的分类标签，分类应该简洁明了，便于后续检索

返回格式为JSON：
{
  "summary": "内容总结",
  "keywords": ["关键词1", "关键词2", ...],
  "category": "分类标签"
}"""

        user_prompt = f"""请分析以下{content_type == 'video' and '视频' or '文章'}：

标题：{title}

内容：
{content}

请返回JSON格式的分析结果。"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=max_tokens
            )

            result_text = response.choices[0].message.content.strip()

            # 尝试解析JSON
            if result_text.startswith("```json"):
                result_text = result_text[7:-3]
            elif result_text.startswith("```"):
                result_text = result_text[3:-3]

            result = json.loads(result_text)

            return {
                "summary": result.get("summary", ""),
                "keywords": result.get("keywords", []),
                "category": result.get("category", "未分类")
            }

        except Exception as e:
            print(f"LLM分析失败: {e}")
            return {
                "summary": "",
                "keywords": [],
                "category": "解析失败"
            }

    async def search_summarize(
        self,
        query: str,
        contents: List[Dict],
        max_tokens: int = 1500
    ) -> str:
        """
        基于搜索结果生成总结

        Args:
            query: 搜索查询
            contents: 相关内容列表
            max_tokens: 最大token数

        Returns:
            总结文本
        """
        if not contents:
            return "没有找到相关内容。"

        system_prompt = """你是一个智能搜索助手，基于相关内容为用户提供有价值的总结。

你的任务是：
1. 综合分析搜索结果，找出与用户查询最相关的内容
2. 用简洁明了的语言总结关键信息
3. 提及内容的来源和分类
4. 如果内容冲突，指出不同观点

总结应该简洁、准确、有帮助。"""

        # 构建内容摘要
        content_summaries = []
        for i, item in enumerate(contents[:5], 1):  # 最多取前5个结果
            content_summaries.append(
                f"{i}. {item['title']} (分类: {item['category']})\n"
                f"   总结: {item['summary'][:200]}..."
            )

        user_prompt = f"""用户查询：{query}

相关内容：
{chr(10).join(content_summaries)}

请提供一份有价值的总结。"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"LLM总结失败: {e}")
            return "总结生成失败，请直接查看搜索结果。"


# 全局LLM服务实例
llm_service = LLMService() if settings.LLM_API_KEY else None

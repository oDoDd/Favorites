"""
测试脚本 - 演示API的基本功能
"""
import asyncio
import httpx


async def test_api():
    """测试API功能"""
    base_url = "http://localhost:8000"

    print("=" * 60)
    print("Favorites API 测试")
    print("=" * 60)

    async with httpx.AsyncClient(base_url=base_url) as client:

        # 1. 测试根路径
        print("\n1. 测试根路径...")
        response = await client.get("/")
        print(f"   状态: {response.status_code}")
        print(f"   响应: {response.json()}")

        # 2. 测试健康检查
        print("\n2. 测试健康检查...")
        response = await client.get("/health")
        print(f"   状态: {response.status_code}")
        print(f"   响应: {response.json()}")

        # 3. 添加文章（不自动解析）
        print("\n3. 添加文章（不自动解析）...")
        article_data = {
            "type": "article",
            "title": "Python编程入门教程",
            "content": "Python是一种高级编程语言，以其简洁易读的语法而闻名。Python广泛应用于数据分析、人工智能、Web开发等领域。学习Python需要掌握基础语法、数据结构、函数、类等概念。本教程将带你从零开始学习Python编程。",
            "url": "https://mp.weixin.qq.com/s/xxx",
            "source": "微信公众号",
            "author": "Python博主",
            "auto_analyze": False
        }
        response = await client.post("/api/content/add", json=article_data)
        print(f"   状态: {response.status_code}")
        if response.status_code == 200:
            article_id = response.json()["id"]
            print(f"   文章ID: {article_id}")
        else:
            print(f"   错误: {response.text}")
            article_id = None

        # 4. 添加视频（不自动解析）
        print("\n4. 添加视频（不自动解析）...")
        video_data = {
            "type": "video",
            "title": "AI技术分享第1期",
            "content": "本期视频介绍人工智能的最新发展，包括大语言模型、计算机视觉、自然语言处理等领域的突破。我们会讨论ChatGPT、GPT-4、Claude等模型的特点和应用场景。",
            "url": "https://weixin.qq.com/xxx",
            "source": "微信视频号",
            "author": "AI科技博主",
            "media_path": "/app/storage/videos/ai_tech_1.mp4",
            "metadata": {"duration": 300, "views": 5000},
            "auto_analyze": False
        }
        response = await client.post("/api/content/add", json=video_data)
        print(f"   状态: {response.status_code}")
        if response.status_code == 200:
            video_id = response.json()["id"]
            print(f"   视频ID: {video_id}")
        else:
            print(f"   错误: {response.text}")
            video_id = None

        # 5. 获取内容列表
        print("\n5. 获取内容列表...")
        response = await client.get("/api/content/list")
        print(f"   状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   总数: {data['total']}")
            for item in data['items']:
                print(f"   - [{item['type']}] {item['title']} (ID: {item['id']})")

        # 6. 搜索内容
        print("\n6. 搜索内容...")
        search_data = {
            "query": "Python",
            "limit": 10
        }
        response = await client.post("/api/search", json=search_data)
        print(f"   状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   搜索关键词: {data['query']}")
            print(f"   结果数: {data['total']}")
            for item in data['items']:
                print(f"   - {item['title']} ({item['category']})")

        # 7. 获取单个内容详情
        if article_id:
            print("\n7. 获取文章详情...")
            response = await client.get(f"/api/content/{article_id}")
            print(f"   状态: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   标题: {data['title']}")
                print(f"   类型: {data['type']}")
                print(f"   分类: {data['category']}")
                print(f"   关键词: {data['keywords']}")

        # 8. 更新内容
        if article_id:
            print("\n8. 更新文章...")
            update_data = {
                "title": "Python编程入门教程（更新版）",
                "category": "编程教程"
            }
            response = await client.put(f"/api/content/{article_id}", json=update_data)
            print(f"   状态: {response.status_code}")
            if response.status_code == 200:
                print(f"   更新成功: {response.json()['title']}")

        # 9. 重新分析内容（需要配置LLM）
        if article_id:
            print("\n9. 重新分析文章（需要配置LLM API）...")
            reanalyze_data = {"content_id": article_id}
            response = await client.post("/api/content/reanalyze", json=reanalyze_data)
            print(f"   状态: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   分析成功")
                print(f"   总结: {data['summary'][:100]}...")
                print(f"   关键词: {data['keywords']}")
                print(f"   分类: {data['category']}")
            elif response.status_code == 500:
                print(f"   LLM服务未配置或失败")

        # 10. 删除内容（可选，注释掉以保留测试数据）
        # if article_id:
        #     print("\n10. 删除文章...")
        #     response = await client.delete(f"/api/content/{article_id}")
        #     print(f"   状态: {response.status_code}")
        #     print(f"   响应: {response.json()}")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_api())

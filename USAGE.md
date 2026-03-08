# 使用指南

## 快速开始

### 1. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入你的LLM API密钥
nano .env
```

在`.env`文件中配置你的LLM API密钥：

```env
# 使用OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxx

# 或使用DeepSeek
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxx

# 或使用智谱AI (GLM)
LLM_PROVIDER=glm
GLM_API_KEY=xxxxxxxxxxxxxxxxxx
```

### 2. 启动服务

#### 方式一：使用启动脚本（推荐）

```bash
./start.sh
```

#### 方式二：手动启动

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

#### 方式三：使用Docker

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 3. 访问API文档

服务启动后，访问：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API使用示例

### 1. 添加微信公众号文章

```bash
curl -X POST "http://localhost:8000/api/content/add" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "article",
    "title": "如何高效学习Python",
    "content": "学习Python需要掌握基础知识...",
    "url": "https://mp.weixin.qq.com/s/xxx",
    "source": "微信公众号",
    "author": "技术博主",
    "auto_analyze": true
  }'
```

### 2. 添加微信短视频（需要先上传视频）

```bash
# 首先上传视频文件到 storage/videos/
# 然后添加记录

curl -X POST "http://localhost:8000/api/content/add" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "video",
    "title": "AI技术分享视频",
    "content": "本期视频介绍AI的最新发展...",
    "url": "https://weixin.qq.com/xxx",
    "source": "微信视频号",
    "author": "AI博主",
    "media_path": "/app/storage/videos/ai_tech.mp4",
    "metadata": {"duration": 120, "views": 10000}
  }'
```

### 3. 搜索内容

```bash
# 基础搜索
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Python学习",
    "limit": 10
  }'

# 使用LLM生成总结
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "AI技术",
    "limit": 10,
    "use_llm_summary": true
  }'

# 按类型筛选
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "技术分享",
    "content_type": "video",
    "limit": 5
  }'
```

### 4. 获取内容列表

```bash
# 获取所有内容
curl "http://localhost:8000/api/content/list?skip=0&limit=20"

# 按类型筛选
curl "http://localhost:8000/api/content/list?content_type=article&limit=10"

# 按分类筛选
curl "http://localhost:8000/api/content/list?category=编程&limit=10"
```

### 5. 获取单个内容详情

```bash
curl "http://localhost:8000/api/content/1"
```

### 6. 更新内容

```bash
curl -X PUT "http://localhost:8000/api/content/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "更新后的标题",
    "category": "Python教程"
  }'
```

### 7. 重新分析内容

```bash
curl -X POST "http://localhost:8000/api/content/reanalyze" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": 1
  }'
```

### 8. 删除内容

```bash
curl -X DELETE "http://localhost:8000/api/content/1"
```

## Python客户端示例

```python
import httpx

# 初始化客户端
client = httpx.AsyncClient(base_url="http://localhost:8000")

# 添加文章
async def add_article():
    response = await client.post("/api/content/add", json={
        "type": "article",
        "title": "深度学习入门",
        "content": "深度学习是机器学习的一个分支...",
        "source": "微信公众号",
        "author": "技术专家",
        "auto_analyze": True
    })
    return response.json()

# 搜索内容
async def search_content(query):
    response = await client.post("/api/search", json={
        "query": query,
        "use_llm_summary": True
    })
    return response.json()

# 使用示例
result = await search_content("机器学习")
print(result["summary"])  # LLM生成的总结
for item in result["items"]:
    print(f"- {item['title']} ({item['category']})")
```

## 微信集成建议

### 方案1：微信机器人 + Webhook

1. 部署微信机器人（如wechaty、itchat）
2. 监听分享到机器人的文章/视频
3. 自动调用API添加内容

### 方案2：浏览器扩展

1. 开发Chrome/Firefox扩展
2. 在微信网页版/视频号页面添加"收藏"按钮
3. 点击后调用API保存内容

### 方案3：手动导入

1. 使用Postman、curl或Python脚本
2. 批量导入已有的文章/视频

## 数据管理

### 备份数据库

```bash
# 备份SQLite数据库
cp data/favorites.db data/favorites.db.backup
```

### 恢复数据库

```bash
# 恢复数据库
cp data/favorites.db.backup data/favorites.db
```

### 清理数据

```python
# 清理所有内容
import httpx
client = httpx.Client(base_url="http://localhost:8000")

# 获取所有内容
response = client.get("/api/content/list")
items = response.json()["items"]

# 删除每个内容
for item in items:
    client.delete(f"/api/content/{item['id']}")
```

## 常见问题

### 1. LLM解析失败

检查`.env`文件中的API密钥是否正确，以及网络连接是否正常。

### 2. 自动解析不工作

确认`AUTO_ANALYZE=true`，并且LLM服务已正确配置。

### 3. 搜索结果不准确

可以手动更新内容的关键词和分类，或使用"重新分析"功能。

### 4. 数据库文件锁定

确保只有一个进程在使用数据库，关闭所有访问数据库的进程。

## 性能优化

### 1. 使用PostgreSQL

对于大量数据，建议使用PostgreSQL替代SQLite：

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/favorites
```

### 2. 添加缓存

在FastAPI中添加Redis缓存，加速搜索响应。

### 3. 批量处理

使用批量API一次添加多个内容，减少网络请求。

## 安全建议

1. 修改默认端口（8000）
2. 使用环境变量管理敏感信息
3. 部署在反向代理（Nginx）后
4. 启用HTTPS
5. 限制API访问频率

## 下一步

- [ ] 添加用户认证
- [ ] 实现标签系统
- [ ] 添加收藏夹功能
- [ ] 支持导出功能
- [ ] 添加Web前端界面

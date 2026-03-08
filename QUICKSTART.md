# 快速入门指南 - 5分钟上手Favorites

## 第一步：克隆项目

```bash
cd ~/.openclaw/workspace
cd Favorites
```

## 第二步：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件
nano .env
```

在`.env`文件中配置你的LLM API密钥（三选一）：

```env
# 方案1：使用OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key

# 方案2：使用DeepSeek（推荐，便宜好用）
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-deepseek-api-key

# 方案3：使用智谱AI (GLM)
LLM_PROVIDER=glm
GLM_API_KEY=your-glm-api-key
```

## 第三步：启动服务

### 方法A：使用启动脚本（推荐）

```bash
./start.sh
```

### 方法B：手动启动

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

看到以下输出说明启动成功：

```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 第四步：测试API

### 方法A：访问API文档

在浏览器打开：http://localhost:8000/docs

你会看到Swagger UI界面，可以直接在网页上测试所有API。

### 方法B：使用curl测试

```bash
# 1. 添加一篇文章
curl -X POST "http://localhost:8000/api/content/add" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "article",
    "title": "Python学习笔记",
    "content": "今天学习了Python的基础语法，包括变量、数据类型、循环等。Python非常适合初学者。",
    "url": "https://mp.weixin.qq.com/s/xxx",
    "source": "微信公众号",
    "auto_analyze": true
  }'

# 2. 搜索内容
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Python",
    "limit": 5
  }'
```

### 方法C：运行测试脚本

```bash
# 在新终端运行
python test_api.py
```

## 第五步：集成微信内容收集

### 方案1：手动添加

从微信复制文章内容，然后使用curl或Python脚本添加：

```python
import httpx

async def add_wechat_article():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        await client.post("/api/content/add", json={
            "type": "article",
            "title": "从微信复制的标题",
            "content": "从微信复制的正文内容...",
            "source": "微信公众号",
            "auto_analyze": True
        })
```

### 方案2：运行微信集成示例

```bash
python wechat_integration_example.py
```

这会添加一些示例数据，展示如何从微信收集内容。

## 常见问题

### Q: 提示"LLM服务未配置"

A: 检查`.env`文件中的API密钥是否正确填写。

### Q: 搜索结果为空

A: 先添加一些内容，确保`auto_analyze=true`让LLM生成关键词和分类。

### Q: 如何添加视频文件？

A:
1. 将视频文件放到`storage/videos/`目录
2. 调用API添加内容，指定`media_path`

```bash
curl -X POST "http://localhost:8000/api/content/add" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "video",
    "title": "我的视频",
    "content": "视频描述...",
    "media_path": "/app/storage/videos/my_video.mp4",
    "auto_analyze": true
  }'
```

## 下一步

- 📖 阅读 [USAGE.md](USAGE.md) 了解详细用法
- 🚀 部署到生产环境（使用Docker）
- 🔗 集成微信机器人（Wechaty）
- 📱 开发Web前端界面

## 获取帮助

- 查看 API 文档: http://localhost:8000/docs
- 查看使用指南: [USAGE.md](USAGE.md)
- 查看项目结构: [README.md](README.md)

祝你使用愉快！ 🎉

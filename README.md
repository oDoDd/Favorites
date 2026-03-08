# Favorites - 微信内容智能收藏系统

## 项目简介

一个智能收藏系统，用于收集、解析和搜索微信短视频和微信公众号文章。通过大语言模型API自动提取关键知识点并进行分类，让你快速找到所需内容。

## 核心功能

- **内容收集**：支持接收微信短视频和文章
- **智能解析**：使用LLM API提取关键知识点
- **自动分类**：基于内容自动打标签和分类
- **快速搜索**：支持关键词搜索，返回总结和相关内容
- **API友好**：完整的RESTful API，便于集成

## 项目结构

```
Favorites/
├── app/
│   ├── api/              # API路由
│   │   ├── content.py    # 内容管理API
│   │   ├── search.py     # 搜索API
│   │   └── schemas.py    # Pydantic模型
│   ├── core/             # 核心配置
│   │   ├── config.py     # 应用配置
│   │   └── database.py   # 数据库连接
│   ├── models/           # 数据库模型
│   │   └── __init__.py   # Content模型
│   └── services/         # 业务逻辑
│       ├── content_service.py  # 内容服务
│       └── llm_service.py      # LLM服务
├── data/                 # 数据库文件目录
├── storage/              # 文件存储目录
│   ├── videos/           # 视频文件
│   └── images/           # 图片文件
├── main.py               # 应用入口
├── requirements.txt      # Python依赖
├── docker-compose.yml   # Docker配置
├── Dockerfile           # Docker镜像
├── test_api.py          # API测试脚本
├── wechat_integration_example.py  # 微信集成示例
├── start.sh             # 快速启动脚本
├── .env.example         # 环境变量模板
└── USAGE.md             # 详细使用指南
```

## 技术栈

- **后端**: FastAPI (Python) - 高性能异步Web框架
- **数据库**: SQLite (可升级到PostgreSQL)
- **ORM**: SQLAlchemy 2.0 (异步)
- **LLM**: 支持多种LLM API (OpenAI, GLM, DeepSeek等)
- **部署**: Docker + Docker Compose
- **API文档**: Swagger UI / ReDoc (自动生成)

## 快速开始

### 方式一：使用启动脚本（推荐）

```bash
# 1. 配置环境变量
cp .env.example .env
nano .env  # 填入你的LLM API密钥

# 2. 运行启动脚本
./start.sh
```

### 方式二：手动启动

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑.env，填入你的LLM API密钥

# 4. 启动服务
python main.py
```

### 方式三：使用Docker

```bash
# 1. 配置环境变量
cp .env.example .env
nano .env

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

### 配置LLM API

编辑`.env`文件，选择并配置LLM提供商：

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

### 访问API文档

服务启动后，访问：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## API端点

### 内容管理

- `POST /api/content/add` - 添加内容（视频/文章）
- `GET /api/content/list` - 获取内容列表
- `GET /api/content/{id}` - 获取内容详情
- `PUT /api/content/{id}` - 更新内容
- `DELETE /api/content/{id}` - 删除内容
- `POST /api/content/reanalyze` - 重新触发LLM解析

### 搜索

- `POST /api/search` - 搜索内容（支持LLM总结）

## 数据结构

### Content (内容表)

```json
{
  "id": 1,
  "type": "article",           // video 或 article
  "title": "标题",
  "url": "原始链接",
  "content": "正文内容",
  "summary": "LLM生成的总结",
  "keywords": ["关键词1", "关键词2"],
  "category": "分类标签",
  "source": "来源平台",
  "author": "作者",
  "media_path": "媒体文件路径",
  "metadata": {
    "duration": 120,
    "views": 10000
  },
  "created_at": "2026-03-08T01:00:00",
  "updated_at": "2026-03-08T01:00:00"
}
```

## 使用示例

### 添加文章

```bash
curl -X POST "http://localhost:8000/api/content/add" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "article",
    "title": "Python学习指南",
    "content": "学习Python需要掌握...",
    "url": "https://mp.weixin.qq.com/s/xxx",
    "source": "微信公众号",
    "author": "技术博主",
    "auto_analyze": true
  }'
```

### 搜索内容

```bash
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Python学习",
    "limit": 10,
    "use_llm_summary": true
  }'
```

更多示例请查看 [USAGE.md](USAGE.md)。

## 测试

运行测试脚本：

```bash
# 确保服务已启动
python main.py

# 在另一个终端运行测试
python test_api.py
```

## 微信集成

项目提供了微信集成示例，展示如何从微信收集内容：

```bash
python wechat_integration_example.py
```

集成方案包括：
- Wechaty机器人
- 浏览器扩展
- 手动批量导入

详见 [wechat_integration_example.py](wechat_integration_example.py)。

## 部署

### 生产环境建议

1. 使用PostgreSQL替代SQLite
2. 配置反向代理（Nginx）
3. 启用HTTPS
4. 添加API认证
5. 配置日志和监控

### Docker部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f favorites
```

## 常见问题

### LLM解析失败
- 检查`.env`中的API密钥是否正确
- 确认网络连接正常
- 查看服务日志获取详细错误信息

### 数据库锁定
- 确保只有一个进程在使用数据库
- 关闭所有访问数据库的进程

### 搜索结果不准确
- 手动更新关键词和分类
- 使用"重新分析"功能
- 调整搜索关键词

## 贡献

欢迎提交Issue和Pull Request！

## License

MIT

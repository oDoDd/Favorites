#!/bin/bash

# 快速启动脚本

echo "🚀 Favorites - 微信内容智能收藏系统"
echo "======================================"

# 检查.env文件是否存在
if [ ! -f .env ]; then
    echo "⚠️  .env文件不存在，从.env.example复制..."
    cp .env.example .env
    echo "✅ 请编辑.env文件，填入你的LLM API密钥"
    echo ""
    read -p "按Enter键继续，或Ctrl+C退出..."
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -r requirements.txt

# 初始化数据库
echo "🗄️  初始化数据库..."
python -c "import asyncio; from app.core.database import init_db; asyncio.run(init_db())"

# 启动服务
echo ""
echo "✅ 准备完成！启动服务..."
echo "📚 API文档: http://localhost:8000/docs"
echo ""
python main.py

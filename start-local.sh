#!/bin/bash

# 本地开发服务器启动脚本
echo "==================================="
echo "🚀 启动Jekyll本地开发服务器"
echo "==================================="
echo ""

# 检查依赖是否安装
if ! command -v bundle &> /dev/null; then
    echo "❌ Bundler未安装，请先运行："
    echo "   gem install bundler"
    exit 1
fi

# 检查Gemfile.lock是否存在
if [ ! -f "Gemfile.lock" ]; then
    echo "📦 首次运行，安装依赖..."
    bundle install
    echo ""
fi

# 清理旧构建（可选）
echo "🧹 清理旧构建文件..."
bundle exec jekyll clean 2>/dev/null || true
echo ""

# 启动服务器
echo "🎯 启动开发服务器..."
echo "📱 服务器地址: http://localhost:4000"
echo "📱 或者: http://127.0.0.1:4000"
echo ""
echo "⏹️  按 Ctrl+C 停止服务器"
echo "==================================="
echo ""

bundle exec jekyll serve

#!/bin/bash
# Nitter 爬蟲伺服器啟動腳本

echo "================================"
echo "Nitter 推文爬蟲伺服器"
echo "================================"
echo ""

# 檢查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未安裝 Python3"
    exit 1
fi

# 檢查依賴
echo "檢查依賴..."
pip3 list | grep -q "requests" || pip3 install requests
pip3 list | grep -q "beautifulsoup4" || pip3 install beautifulsoup4
pip3 list | grep -q "lxml" || pip3 install lxml

echo "✓ 依賴檢查完成"
echo ""

# 檢查配置文件
if [ ! -f "users.json" ]; then
    echo "❌ 找不到 users.json 配置文件"
    exit 1
fi

echo "開始執行爬蟲..."
echo ""

# 執行主程式
python3 nitter_server.py

echo ""
echo "================================"
echo "執行完成"
echo "================================"

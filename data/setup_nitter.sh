#!/bin/bash
# 快速架設 Nitter 伺服器（使用 Docker）

set -e

NITTER_DIR="$HOME/nitter-server"
NITTER_PORT="8080"

echo "================================"
echo "Nitter 伺服器快速架設"
echo "================================"
echo ""

# 檢查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 未安裝 Docker"
    echo "請先安裝 Docker: https://docs.docker.com/engine/install/"
    exit 1
fi

# 檢測 Docker Compose 版本
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
    echo "✓ Docker Compose (plugin) 已安裝"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
    echo "✓ Docker Compose (standalone) 已安裝"
else
    echo "❌ 未安裝 Docker Compose"
    exit 1
fi

# 檢查是否需要 sudo
if ! docker ps &> /dev/null; then
    echo "⚠ Docker 需要 sudo 權限（用戶尚未加入 docker 群組）"
    DOCKER_COMPOSE="sudo $DOCKER_COMPOSE"
fi

echo "✓ Docker 已安裝"
echo ""

# 創建目錄
echo "創建 Nitter 目錄..."
mkdir -p "$NITTER_DIR"
cd "$NITTER_DIR"

# 創建 docker-compose.yml
echo "生成配置文件..."
cat > docker-compose.yml << 'EOF'
version: '3'

services:
  nitter:
    image: zedeus/nitter:latest
    container_name: nitter
    ports:
      - "8080:8080"
    volumes:
      - ./nitter.conf:/src/nitter.conf:ro
    restart: unless-stopped 

    healthcheck:
      test: wget -nv --tries=1 --spider http://127.0.0.1:8080/jack || exit 1
      interval: 30s
      timeout: 5s
      retries: 2
EOF

# 創建 nitter.conf
cat > nitter.conf << 'EOF'
[Server]
address = "0.0.0.0"
port = 8080
https = false
httpMaxConnections = 100
staticDir = "./public"
title = "Nitter"
hostname = "localhost"

[Cache]
listMinutes = 240
rssMinutes = 10
redisHost = ""
redisPort = 6379
redisPassword = ""
redisConnections = 20
redisMaxConnections = 30

[Config]
hmacKey = "secretkey"
base64Media = false
enableRSS = true
enableDebug = false
proxy = ""
proxyAuth = ""
tokenCount = 10

[Preferences]
theme = "Nitter"
replaceTwitter = ""
replaceYouTube = ""
replaceReddit = ""
proxyVideos = true
hlsPlayback = false
infiniteScroll = false
EOF

echo "✓ 配置文件已生成"
echo ""

# 啟動服務
echo "啟動 Nitter 容器..."
$DOCKER_COMPOSE up -d

echo ""
echo "等待服務啟動..."
sleep 10

# 測試服務
echo "測試服務..."
if curl -s http://localhost:$NITTER_PORT > /dev/null; then
    echo ""
    echo "================================"
    echo "✅ Nitter 伺服器啟動成功！"
    echo "================================"
    echo ""
    echo "訪問地址: http://localhost:$NITTER_PORT"
    echo "測試用戶: http://localhost:$NITTER_PORT/elonmusk"
    echo ""
    echo "管理指令："
    echo "  查看狀態: $DOCKER_COMPOSE ps"
    echo "  查看日誌: $DOCKER_COMPOSE logs -f nitter"
    echo "  停止服務: $DOCKER_COMPOSE stop"
    echo "  重啟服務: $DOCKER_COMPOSE restart"
    echo "  移除服務: $DOCKER_COMPOSE down"
    echo ""
    echo "下一步："
    echo "1. 編輯 /home/fan/bluebird/data/users.json"
    echo "2. 確認 nitter_instances 設為: [\"localhost:8080\"]"
    echo "3. 執行爬蟲: cd /home/fan/bluebird/data && python3 nitter_server.py"
    echo ""
else
    echo ""
    echo "❌ 服務啟動失敗"
    echo "請執行以下指令查看日誌："
    echo "  cd $NITTER_DIR && $DOCKER_COMPOSE logs nitter"
    exit 1
fi

# 自建 Nitter 伺服器指南

由於公共 Nitter 實例不穩定，建議自己架設 Nitter 伺服器。

## 方式 1：使用 Docker（推薦）

### 前置需求
- Docker
- Docker Compose

### 步驟

#### 1. 創建 Nitter 目錄
```bash
mkdir -p ~/nitter-server
cd ~/nitter-server
```

#### 2. 創建 docker-compose.yml
```bash
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
￼
fan@nkmrlab2401:~/bluebird/data$ grep -n "（\|）" /home/fan/bluebird/data/nitter_server.py | head -10
43:        # 預設 Nitter 實例列表（優先順序排序）
46:            'localhost:8080',  # 本地自建實例（預設）
84:                    logger.warning("⚠ 未配置自建實例，使用預設列表（公共實例可能不穩定）")
163:            # 判斷是否為本地實例（不使用 HTTPS）
207:            max_tweets: 最大推文數（None = 全部）
222:        work_duration = 15 * 60  # 15 分鐘（秒）
231:                brea（本地實例使用 HTTP）
fan@nkmrlab2401:~/bluebird/data$ python3 -m py_compile /home/fan/bluebird/data/nitter_server.py 2>&1
  File "/home/fan/bluebird/data/nitter_server.py", line 172
    logger.debug(f"實例測試失敗 {instance}: {e}")n.commit()
                                                     ^
SyntaxError: invalid syntax
fan@nkmrlab2401:~/bluebird/data$ python3 -m py_compile /home/fan/bluebird/data/nitter_server.py 2>&1 && echo "✓ OK" || tail -5
Sorry: IndentationError: unexpected indent (nitter_server.py, line 245) 
 bashdata
 bashnitter-server
 bash
 bash
 bashfan
 bashnitter-build
 bashnitter-build
 bashnitter-build
 bashnitter-build
 bashnitter-build
 taildata
CHAT
ALL SESSIONS
Implementing Nitter RSS endpoint with XML parser
Using "Run in Terminal"
Local • 10s
IMPLEMENTING NITTER RSS ENDPOINT WITH XML PARSER
Started Nitter server and checked user data
現在的狀況：

✅ Nitter 伺服器已成功運行 - 在 http://localhost:8080，可以正常抓取資料

❌ Python 爬蟲腳本有語法錯誤 - nitter_server.py 有未閉合的三引號字串

我剛剛發現問題：

￼
fan@nkmrlab2401:~/bluebird/data$ grep -n "（\|）" /home/fan/bluebird/data/nitter_server.py | head -10
43:        # 預設 Nitter 實例列表（優先順序排序）
46:            'localhost:8080',  # 本地自建實例（預設）
84:                    logger.warning("⚠ 未配置自建實例，使用預設列表（公共實例可能不穩定）")
163:            # 判斷是否為本地實例（不使用 HTTPS）
207:            max_tweets: 最大推文數（None = 全部）
222:        work_duration = 15 * 60  # 15 分鐘（秒）
231:                brea（本地實例使用 HTTP）
fan@nkmrlab2401:~/bluebird/data$ python3 -m py_compile /home/fan/bluebird/data/nitter_server.py 2>&1
  File "/home/fan/bluebird/data/nitter_server.py", line 172
    logger.debug(f"實例測試失敗 {instance}: {e}")n.commit()
                                                     ^
SyntaxError: invalid syntax
fan@nkmrlab2401:~/bluebird/data$ python3 -m py_compile /home/fan/bluebird/data/nitter_server.py 2>&1 && echo "✓ OK" || tail -5
Sorry: IndentationError: unexpected indent (nitter_server.py, line 245) 
 bashdata
 bashnitter-server
 bash
 bash
 bashfan
 bashnitter-build
 bashnitter-build
 bashnitter-build
 bashnitter-build
 bashnitter-build
 taildata
CHAT
ALL SESSIONS
Implementing Nitter RSS endpoint with XML parser
Using "Run in Terminal"
Local • 10s
IMPLEMENTING NITTER RSS ENDPOINT WITH XML PARSER
Started Nitter server and checked user data
現在的狀況：

✅ Nitter 伺服器已成功運行 - 在 http://localhost:8080，可以正常抓取資料

❌ Python 爬蟲腳本有語法錯誤 - nitter_server.py 有未閉合的三引號字串

我剛剛發現問題：

第 138 行的 SQL 語句缺少closing ''')
檔案中有 7 個單引號三引號（應該是偶數）
你想要我：

修復語法錯誤 然後執行爬蟲？
還是暫停，你要先確認什麼？
Restore Checkpoint
繼續修復語法錯誤 但盡快

Checked and fixed syntax errors

第 138 行的 SQL 語句缺少closing ''')
檔案中有 7 個單引號三引號（應該是偶數）
你想要我：

修復語法錯誤 然後執行爬蟲？
還是暫停，你要先確認什麼？
Restore Checkpoint
繼續修復語法錯誤 但盡快

Checked and fixed syntax errors

```

#### 3. 創建配置文件 nitter.conf
```bash
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
```

#### 4. 啟動 Nitter
```bash
docker-compose up -d
```

#### 5. 檢查狀態
```bash
# 查看容器狀態
docker-compose ps

# 查看日誌
docker-compose logs -f nitter

# 測試訪問
curl http://localhost:8080
```

#### 6. 更新 users.json
將 `nitter_instances` 改為：
```json
"nitter_instances": ["localhost:8080"]
```

---

## 方式 2：使用 Nimble 編譯（進階）

### 前置需求
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install -y libsass-dev libpcre3-dev git

# 安裝 Nim 和 Nimble
curl https://nim-lang.org/choosenim/init.sh -sSf | sh
echo 'export PATH=$HOME/.nimble/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 步驟

#### 1. 創建 Nitter 用戶（可選）
```bash
sudo useradd -m -s /bin/bash nitter
sudo su - nitter
```

#### 2. 克隆並編譯
```bash
cd ~
git clone https://github.com/zedeus/nitter
cd nitter
nimble build -d:danger --mm:refc
nimble scss
nimble md
```

#### 3. 配置
```bash
cp nitter.example.conf nitter.conf
# 編輯 nitter.conf，主要修改：
# - [Server] address = "0.0.0.0"
# - [Server] port = 8080
# - [Config] hmacKey = "your-secret-key"
```

#### 4. 執行
```bash
# 前台執行（測試用）
./nitter

# 或使用 systemd 背景執行
```

---

## 方式 3：使用 systemd 服務（生產環境）

創建服務文件 `/etc/systemd/system/nitter.service`：

```ini
[Unit]
Description=Nitter (An alternative Twitter front-end)
After=network.target

[Service]
Type=simple
User=nitter
WorkingDirectory=/home/nitter/nitter
ExecStart=/home/nitter/nitter/nitter
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

啟動服務：
```bash
sudo systemctl daemon-reload
sudo systemctl enable nitter
sudo systemctl start nitter
sudo systemctl status nitter
```

---

## 配置 Nginx 反向代理（可選）

如果需要使用域名訪問：

```nginx
server {
    listen 80;
    server_name nitter.yourdomain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

配置後更新 `users.json`：
```json
"nitter_instances": ["nitter.yourdomain.com"]
```

---

## 多實例配置

如果架設了多個 Nitter 伺服器（提高可靠性）：

```json
{
  "settings": {
    "nitter_instances": [
      "localhost:8080",
      "192.168.1.100:8080",
      "nitter.yourdomain.com"
    ]
  }
}
```

程式會按順序測試，自動選擇可用的實例。

---

## 故障排除

### 1. 容器無法啟動
```bash
# 查看詳細日誌
docker-compose logs nitter

# 檢查端口是否被占用
sudo netstat -tlnp | grep 8080

# 重啟容器
docker-compose restart nitter
```

### 2. 連接被拒絕
```bash
# 確認服務正在運行
curl http://localhost:8080

# 檢查防火牆
sudo ufw allow 8080
```

### 3. Guest Token 錯誤
編輯 `nitter.conf`：
```ini
[Config]
tokenCount = 0  # 禁用 guest accounts
```

### 4. 記憶體不足
增加 Docker 記憶體限制：
```yaml
services:
  nitter:
    # ...
    deploy:
      resources:
        limits:
          memory: 512M
```

---

## 效能優化

### 1. 使用 Redis 快取（可選）

```bash
# 添加 Redis 到 docker-compose.yml
services:
  redis:
    image: redis:alpine
    container_name: nitter-redis
    restart: unless-stopped
  
  nitter:
    # ... 其他配置
    depends_on:
      - redis
```

更新 `nitter.conf`：
```ini
[Cache]
redisHost = "redis"
redisPort = 6379
```

### 2. 調整 Token 數量
```ini
[Config]
tokenCount = 10  # 增加 token 數量提高請求速度
```

---

## 測試自建實例

```bash
# 測試基本訪問
curl http://localhost:8080

# 測試用戶頁面
curl http://localhost:8080/elonmusk

# 使用爬蟲測試
cd /home/fan/bluebird/data
python3 nitter_server.py
```

---

## 安全建議

⚠️ **僅供本地/內網使用**  
如果不需要公開訪問，建議：
```yaml
ports:
  - "127.0.0.1:8080:8080"  # 僅監聽本地
```

⚠️ **使用強密鑰**  
修改 `nitter.conf`：
```ini
[Config]
hmacKey = "$(openssl rand -base64 32)"
```

⚠️ **定期更新**  
```bash
docker-compose pull
docker-compose up -d
```

---

## 快速測試指令

```bash
# Docker 方式（最快）
mkdir -p ~/nitter-server && cd ~/nitter-server
curl -o docker-compose.yml https://raw.githubusercontent.com/zedeus/nitter/master/docker-compose.yml
curl -o nitter.conf https://raw.githubusercontent.com/zedeus/nitter/master/nitter.example.conf
docker-compose up -d

# 等待 10 秒後測試
sleep 10
curl http://localhost:8080/elonmusk
```

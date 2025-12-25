# Nitter 推文爬蟲伺服器

自動從 Nitter 實例抓取多個用戶的推文並存入 SQLite 資料庫。

## 功能特點

✅ **批量抓取** - 一次抓取多個用戶的推文  
✅ **自動重試** - 實例失敗時自動切換  
✅ **增量更新** - 避免重複抓取  
✅ **進度追蹤** - 詳細的日誌記錄  
✅ **靈活配置** - JSON 配置文件管理用戶  

## 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 配置用戶

編輯 `users.json` 文件，設定要抓取的用戶：

```json
{
  "users": [
    {
      "username": "elonmusk",
      "max_tweets": 500
    },
    {
      "username": "openai",
      "max_tweets": null
    }
  ],
  "settings": {
    "request_delay": 2,
    "user_delay": 5
  }
}
```

- `max_tweets`: 限制抓取數量，`null` 表示抓取全部
- `request_delay`: 每次請求間隔（秒）
- `user_delay`: 用戶間延遲（秒）

### 3. 執行爬蟲

```bash
python nitter_server.py
```

或使用啟動腳本：

```bash
chmod +x run.sh
./run.sh
```

## 資料庫結構

### tweets 表
- `tweet_id`: 推文 ID（主鍵）
- `text`: 推文內容
- `author_id`: 作者用戶名
- `created_at`: 發布時間
- `hashtags`: 標籤（逗號分隔）
- `urls`: 連結（逗號分隔）
- `media_type`: 媒體類型（photo/video）
- `media_urls`: 媒體 URL（逗號分隔）
- `scraped_at`: 抓取時間

### scrape_logs 表
記錄每次爬取的詳細信息：
- 用戶名
- 找到的推文數
- 新增/更新數量
- 狀態（成功/失敗）
- 錯誤訊息

## 查詢範例

### 查看最新推文

```sql
SELECT author_id, text, created_at 
FROM tweets 
ORDER BY created_at DESC 
LIMIT 20;
```

### 統計各用戶推文數

```sql
SELECT author_id, COUNT(*) as tweet_count
FROM tweets
GROUP BY author_id
ORDER BY tweet_count DESC;
```

### 查看爬取日誌

```sql
SELECT username, tweets_found, tweets_new, status, completed_at
FROM scrape_logs
ORDER BY started_at DESC;
```

## 注意事項

⚠️ **Nitter 實例可用性** - Nitter 公共實例可能不穩定，程式會自動切換  
⚠️ **請求頻率** - 建議設定適當延遲避免被封鎖  
⚠️ **私人帳號** - 無法抓取受保護的帳號  

## 進階功能

### 定時執行（cron）

在 Linux 上設定每日自動抓取：

```bash
# 編輯 crontab
crontab -e

# 每天凌晨 2 點執行
0 2 * * * cd /home/fan/bluebird/data && python nitter_server.py >> scraper.log 2>&1
```

### 匯出為 SQL

如需將資料庫匯出為 SQL 文件：

```bash
sqlite3 mydb.db .dump > backup.sql
```

## 故障排除

### 所有實例都失敗

Nitter 公共實例可能全部離線，可以：
1. 等待一段時間重試
2. 自己架設 Nitter 實例
3. 在 `nitter_server.py` 中添加更多實例

### 記憶體不足

對於推文數量極多的帳號，可以設定 `max_tweets` 限制。

## 授權

MIT License

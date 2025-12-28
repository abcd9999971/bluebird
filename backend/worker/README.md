# Cloudflare Workers 部署指南

## 專案概述
這是一個使用 Cloudflare Workers 和 D1 Database 的 Twitter Timeline API 後端。

## 功能特性
- ✅ RESTful API 端點
- ✅ D1 Database（SQLite）支援
- ✅ CORS 支援
- ✅ TypeScript 支援
- ✅ 完整的推文、成員、統計 API

## API 端點

### 1. 獲取所有成員資訊
```
GET /api/members
```

### 2. 獲取推文列表
```
GET /api/tweets?author=polka&year=2025&month=8&limit=50&offset=0
```
查詢參數：
- `author`: 成員 ID（可選）
- `year`: 年份（可選）
- `month`: 月份（可選）
- `search`: 搜尋關鍵字（可選）
- `limit`: 每頁數量（預設 50）
- `offset`: 偏移量（預設 0）

### 3. 獲取統計資訊
```
GET /api/stats
```

### 4. 新增推文
```
POST /api/tweets
Content-Type: application/json

{
  "authorId": "polka",
  "content": "推文內容",
  "imageUrl": "https://example.com/image.jpg" // 可選
}
```

### 5. 處理喜歡/取消喜歡
```
POST /api/likes
Content-Type: application/json

{
  "tweetId": 1,
  "userIp": "192.168.1.1",
  "action": "like" // 或 "unlike"
}
```

### 6. 獲取喜歡狀態
```
GET /api/likes/status?tweetIds=1,2,3&userIp=192.168.1.1
```

## 部署步驟

### 前置要求
1. 安裝 [Node.js](https://nodejs.org/) (v18 或更高版本)
2. 註冊 [Cloudflare 帳號](https://dash.cloudflare.com/sign-up)

### 1. 安裝依賴
```bash
cd backend/worker
npm install
```

### 2. 登入 Cloudflare
```bash
npx wrangler login
```
這會打開瀏覽器，讓你授權 Wrangler 訪問你的 Cloudflare 帳號。

### 3. 創建 D1 數據庫（如果還沒有）
```bash
# 創建新的 D1 數據庫
npx wrangler d1 create twitter-timeline

# 記下輸出的 database_id，更新 wrangler.jsonc 中的 database_id
```

如果你已經有數據庫，可以查看現有數據庫：
```bash
npx wrangler d1 list
```

### 4. 初始化數據庫結構
```bash
# 執行 schema.sql 創建表格
npx wrangler d1 execute twitter-timeline --file=./schema.sql
```

### 5. 本地開發測試
```bash
# 啟動本地開發伺服器
npm run dev
```
訪問 `http://localhost:8787` 測試 API。

### 6. 部署到 Cloudflare
```bash
# 部署到生產環境
npm run deploy
```

部署成功後，你會看到類似這樣的輸出：
```
Published bluebird-api (1.23 sec)
  https://bluebird-api.your-subdomain.workers.dev
```

### 7. 驗證部署
訪問你的 Workers URL 來驗證：
```bash
# 測試基本端點
curl https://bluebird-api.your-subdomain.workers.dev/

# 測試成員列表
curl https://bluebird-api.your-subdomain.workers.dev/api/members

# 測試推文列表
curl https://bluebird-api.your-subdomain.workers.dev/api/tweets
```

## 數據庫管理

### 查看數據庫內容
```bash
# 進入 D1 控制台
npx wrangler d1 execute twitter-timeline --command "SELECT * FROM members LIMIT 5"

# 查看推文
npx wrangler d1 execute twitter-timeline --command "SELECT * FROM tweets LIMIT 10"
```

### 導入現有數據
如果你有 dump.sql 文件：
```bash
npx wrangler d1 execute twitter-timeline --file=../../dump.sql
```

### 備份數據庫
```bash
# 導出數據
npx wrangler d1 export twitter-timeline --output=backup.sql
```

## 環境配置

### 生產環境變數
如果需要設置環境變數：
```bash
# 設置 secret
npx wrangler secret put API_KEY

# 在 wrangler.jsonc 中設置變數
# "vars": { "ENVIRONMENT": "production" }
```

### 自定義域名
1. 在 Cloudflare Dashboard 中進入 Workers & Pages
2. 選擇你的 Worker
3. 點擊 "Triggers" > "Add Custom Domain"
4. 輸入你的域名（例如：api.yourdomain.com）

## 監控與除錯

### 查看日誌
```bash
# 實時查看日誌
npx wrangler tail
```

### Cloudflare Dashboard
訪問 [Cloudflare Dashboard](https://dash.cloudflare.com/) 查看：
- 請求統計
- 錯誤率
- 響應時間
- D1 數據庫查詢

## 更新前端 API 配置

部署後，需要更新前端配置以使用新的 API URL：

### 方法 1：環境變數（推薦）
在前端專案中創建 `.env` 文件：
```env
VITE_API_BASE_URL=https://bluebird-api.your-subdomain.workers.dev
```

### 方法 2：直接修改配置
更新前端中的 API URL（例如在 `frontend/page/src/composables/useApi.js`）：
```javascript
const API_BASE_URL = 'https://bluebird-api.your-subdomain.workers.dev';
```

## 常見問題

### 1. 部署時提示 "database not found"
確保 `wrangler.jsonc` 中的 `database_id` 正確，可以用 `npx wrangler d1 list` 查看。

### 2. CORS 錯誤
已在代碼中添加 CORS 支援。如果需要限制域名：
```typescript
'Access-Control-Allow-Origin': 'https://yourdomain.com'
```

### 3. 查詢速度慢
D1 是免費的 SQLite 數據庫，對於大量數據可能需要優化查詢或添加索引。

### 4. 更新代碼後如何重新部署
```bash
npm run deploy
```
每次修改代碼後都需要重新部署。

## 成本估算
Cloudflare Workers 免費方案：
- ✅ 100,000 請求/天
- ✅ 10ms CPU 時間/請求
- ✅ D1: 5GB 存儲，每天 100,000 次讀取

對於小到中型專案完全免費！

## 參考資料
- [Cloudflare Workers 文檔](https://developers.cloudflare.com/workers/)
- [D1 Database 文檔](https://developers.cloudflare.com/d1/)
- [Wrangler CLI 文檔](https://developers.cloudflare.com/workers/wrangler/)

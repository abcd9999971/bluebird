# Cloudflare Workers 部署指南

## 前置準備

1. 註冊 [Cloudflare](https://dash.cloudflare.com/) 帳號
2. 安裝 Wrangler CLI:
```bash
npm install -g wrangler
```

3. 登入 Cloudflare:
```bash
wrangler login
```

## 建立 D1 資料庫

### 1. 建立資料庫
```bash
cd backend/worker
wrangler d1 create bluebird-db
```

記下返回的 `database_id`，並更新 `wrangler.jsonc` 中的 `database_id`。

### 2. 初始化資料庫結構
```bash
wrangler d1 execute bluebird-db --file=./schema.sql
```

### 3. 上傳資料

首先同步本地資料:
```bash
cd ../..
python sync_to_d1.py
```

然後從本地 D1 資料庫導出 SQL:
```bash
cd backend/worker
# 導出資料
sqlite3 .wrangler/state/v3/d1/miniflare-D1DatabaseObject/db.sqlite .dump > data.sql
# 上傳到 Cloudflare D1
wrangler d1 execute bluebird-db --file=./data.sql
```

## 部署應用

### 部署後端
```bash
cd backend/worker
wrangler deploy
```

部署成功後會得到一個 URL，例如 `https://bluebird.your-subdomain.workers.dev`

### 部署前端

#### Option 1: Cloudflare Pages（推薦）

1. 建置前端:
```bash
cd frontend/page
npm run build
```

2. 部署到 Cloudflare Pages:
```bash
npx wrangler pages deploy dist
```

#### Option 2: 其他靜態網站託管

可以部署到 Vercel、Netlify 等平台，記得設定環境變數指向後端 Worker URL。

## 更新資料流程

當您抓取新推文後:

1. 同步到本地 D1:
```bash
python sync_to_d1.py
```

2. 導出並上傳到雲端:
```bash
cd backend/worker
sqlite3 .wrangler/state/v3/d1/miniflare-D1DatabaseObject/db.sqlite .dump > data.sql
wrangler d1 execute bluebird-db --file=./data.sql
```

## 注意事項

- Cloudflare D1 目前處於 Beta 階段，有[使用限制](https://developers.cloudflare.com/d1/platform/limits/)
- 免費方案限制: 每日 10萬次讀取、10萬次寫入
- 資料庫大小限制: 500 MB
- 對於本專案（<2000筆推文），免費方案綽綽有餘

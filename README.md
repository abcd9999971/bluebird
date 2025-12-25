# いきづらい部！部員日誌

基於 Vue.js 3 和 Cloudflare Workers 的成員日誌應用程式，結合 Nitter 推文爬蟲系統，提供完整的推文抓取、同步及展示功能。採用舊推特經典配色與現代化 UI 設計，完整支援桌面版和手機版響應式布局。

## 📋 目錄

- [專案架構](#專案架構)
- [快速開始](#快速開始)
- [主要功能](#主要功能)
- [技術架構](#技術架構)
- [專案結構](#專案結構)
- [開發指南](#開發指南)
- [資料流程](#資料流程)
- [部署說明](#部署說明)
- [授權聲明](#授權聲明)

## 🏗️ 專案架構

本專案包含三個主要部分：

```
資料抓取 (Nitter) → 資料同步 (sync_to_d1.py) → 後端服務 (Cloudflare Workers) → 前端展示 (Vue.js)
```

### 核心組件

1. **資料抓取層** (`data/`)
   - Nitter 推文爬蟲系統
   - SQLite 資料庫 (`mydb.db`)
   - 自動化抓取腳本

2. **資料同步層** (根目錄)
   - `sync_to_d1.py` - 將 Nitter 資料同步至 Cloudflare D1

3. **後端服務層** (`backend/worker/`)
   - Cloudflare Workers API
   - D1 資料庫管理
   - RESTful API 端點

4. **前端展示層** (`frontend/page/`)
   - Vue.js 3 應用程式
   - 響應式 UI 設計
   - 成員日誌展示系統

## 🚀 快速開始

### 環境要求

- **Node.js** 20.19.0+ 或 22.12.0+
- **Python** 3.8+（用於資料抓取和同步）
- **npm** 或 yarn

### 安裝與執行

#### 1. 啟動後端服務

```bash
cd backend/worker
npm install
npm run dev
```

後端服務將在 `http://localhost:8787` 執行。

#### 2. 啟動前端應用

```bash
cd frontend/page
npm install
npm run dev
```

前端應用將在 `http://localhost:5173` 執行。

#### 3. 資料抓取（選用）

如需從 Twitter/X 抓取新資料：

```bash
cd data
pip install -r requirements.txt
python nitter_server.py
```

#### 4. 資料同步

將抓取的資料同步到 Cloudflare D1：

```bash
python sync_to_d1.py
```

## ✨ 主要功能

### 核心功能

- **響應式設計** - 支援桌面版、平板版和手機版，智慧布局切換
- **成員篩選** - 可依成員、年份、月份篩選推文
- **搜尋功能** - 支援推文內容和成員名稱搜尋，搜尋結果突顯顯示
- **個人資料系統** - 每個成員都有詳細的個人資料頁面
- **日期導航器** - 快速跳轉到特定日期的推文

### 使用者體驗

- **主題切換** - 支援明暗主題切換
- **推文互動** - 按讚、分享功能
- **下拉重新整理** - 手機版下拉重新整理推文

### 手機版特色

- **手機版導航** - 專為手機設計的橫向滾動導航
- **底部導航欄** - 手機版快速導航
- **橫屏適配** - 最佳化手機橫屏模式布局
- **生日提醒** - 成員生日時顯示特別提醒橫幅

### 資料管理

- **自動抓取** - Nitter 爬蟲批量抓取多個用戶推文
- **增量更新** - 避免重複抓取，只獲取新推文
- **資料同步** - 一鍵將本地資料同步至雲端 D1 資料庫

## 🛠️ 技術架構

### 前端技術堆疊

- **Vue.js 3** - Composition API 和響應式系統
- **Vite** - 快速的前端建構工具
- **Vue I18n** - 國際化支援
- **html2canvas** - 推文圖片生成

### 後端技術堆疊

- **Cloudflare Workers** - 邊緣運算平台
- **Cloudflare D1** - SQLite 資料庫
- **RESTful API** - 標準化的 API 設計

### 資料抓取技術

- **Nitter** - Twitter/X 的開源前端
- **Python** - 爬蟲腳本語言
- **SQLite** - 本地資料庫

### 設計系統

- **CSS 變數系統** - 統一的設計系統和主題管理
- **響應式設計** - 支援多種螢幕尺寸和裝置
- **Material Symbols Outlined** - Google 圖示字體
- **Noto Sans JP** - 日文字體最佳化

## 📁 專案結構

```
bluebird/
├── data/                          # 資料抓取系統
│   ├── mydb.db                   # SQLite 資料庫（Nitter 爬蟲資料）
│   ├── nitter_server.py          # Nitter 爬蟲主程式
│   ├── nittertweets.py           # 推文抓取模組
│   ├── users.json                # 用戶配置檔案
│   ├── requirements.txt          # Python 依賴
│   └── README.md                 # Nitter 使用說明
│
├── sync_to_d1.py                 # 資料同步腳本
│
├── backend/                       # 後端服務
│   └── worker/
│       ├── src/index.ts          # Cloudflare Workers API
│       ├── schema.sql            # D1 資料庫結構
│       ├── wrangler.jsonc        # Cloudflare 配置
│       └── package.json
│
├── frontend/                      # 前端應用
│   └── page/
│       ├── src/
│       │   ├── App.vue           # 主應用元件
│       │   ├── main.js           # 應用入口
│       │   ├── components/       # Vue 元件
│       │   │   ├── layout/       # 佈局元件
│       │   │   ├── posts/        # 推文元件
│       │   │   ├── modals/       # 彈出視窗
│       │   │   ├── ui/           # UI 元件
│       │   │   └── features/     # 功能元件
│       │   ├── composables/      # Composition API
│       │   ├── utils/            # 工具函式
│       │   ├── locales/          # 國際化
│       │   └── assets/           # 靜態資源
│       ├── vite.config.js
│       └── package.json
│
├── DEPLOYMENT.md                  # 部署指南
└── README.md                      # 本文件
```

## 💻 開發指南

### 資料抓取流程

1. **配置用戶** - 編輯 `data/users.json` 設定要抓取的 Twitter/X 用戶
2. **執行爬蟲** - 運行 `python data/nitter_server.py`
3. **檢查資料** - 資料會儲存至 `data/mydb.db`

詳細說明請參考 [`data/README.md`](data/README.md)

### 資料同步流程

`sync_to_d1.py` 腳本會：

1. 從 `data/mydb.db` 讀取 Nitter 爬蟲資料
2. 轉換資料格式符合 D1 資料庫結構
3. 同步至 `backend/worker/.wrangler/state/v3/d1/.../db.sqlite`
4. 本地開發環境即可使用最新資料

```bash
# 執行資料同步
python sync_to_d1.py
```

### API 端點

後端提供以下 API 端點：

- `GET /api/members` - 獲取所有成員資訊
- `GET /api/tweets` - 獲取推文列表（支援篩選）
  - 參數：`author`, `year`, `month`, `search`, `limit`, `offset`
- `GET /api/stats` - 獲取統計資訊
- `POST /api/tweets` - 新增推文
- `POST /api/likes` - 處理喜歡/取消喜歡
- `GET /api/likes/status` - 獲取喜歡狀態

### 元件開發

前端採用模組化元件設計：

- **佈局元件** (`layout/`) - 頁面結構和導航
- **推文元件** (`posts/`) - 推文顯示和互動
- **彈出視窗** (`modals/`) - 詳情和個人資料
- **UI 元件** (`ui/`) - 可重用基礎元件
- **功能元件** (`features/`) - 搜尋、篩選等功能

詳細的元件架構說明請參考完整 README 的「元件架構」章節。

### 國際化

使用 Vue I18n 進行文字管理：

- 語言包位於 `frontend/page/src/locales/`
- 目前支援日文 (`ja.json`)
- 可輕鬆擴展至其他語言

## 🔄 資料流程

### 完整資料流

```
1. Twitter/X 推文
   ↓
2. Nitter 爬蟲抓取 (data/nitter_server.py)
   ↓
3. 存入本地 SQLite (data/mydb.db)
   ↓
4. 資料同步腳本 (sync_to_d1.py)
   ↓
5. Cloudflare D1 資料庫 (本地/雲端)
   ↓
6. Workers API (backend/worker)
   ↓
7. Vue.js 前端展示 (frontend/page)
```

### 開發環境資料流

```
data/mydb.db → sync_to_d1.py → backend/worker/.wrangler/...db.sqlite
                                         ↓
                                   localhost:8787 (API)
                                         ↓
                                   localhost:5173 (前端)
```

### 生產環境資料流

```
data/mydb.db → sync_to_d1.py → 匯出 SQL → wrangler d1 execute
                                              ↓
                                         Cloudflare D1
                                              ↓
                                         Workers API
                                              ↓
                                         Cloudflare Pages
```

## 🚀 部署說明

詳細部署指南請參考 [DEPLOYMENT.md](DEPLOYMENT.md)

### 快速部署

#### 後端部署

```bash
cd backend/worker
wrangler deploy
```

#### 前端部署

```bash
cd frontend/page
npm run build
npx wrangler pages deploy dist
```

#### 資料更新

```bash
# 1. 抓取新推文
python data/nitter_server.py

# 2. 同步到本地 D1
python sync_to_d1.py

# 3. 匯出並上傳到雲端
cd backend/worker
sqlite3 .wrangler/state/v3/d1/miniflare-D1DatabaseObject/db.sqlite .dump > data.sql
wrangler d1 execute bluebird-db --file=./data.sql
```

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request 來改善這個專案。

## 📄 授權聲明

### 版權聲明

本專案為完全非官方專案，僅供學習和研究使用，無任何商業目的。專案中所包含的所有版權素材和文字，其版權均屬於「©プロジェクトイキヅライブ！」，本專案不擁有相關版權。

### 免責宣告

本專案僅為技術展示和學習用途，所有相關內容的版權歸原權利人所有。如有任何版權問題，請聯絡原權利人處理。

- 本專案僅供個人學習和研究使用
- 禁止將本專案用於任何商業用途
- 使用者需自行承擔使用本專案的所有風險和責任

[ガイドライン | イキヅライブ！ LOVELIVE! BLUEBIRD](https://www.lovelive-anime.jp/lovehigh/guideline/)

如有任何疑問或需要進一步資訊，請參閱上述官方連結。

---

## 📚 相關文件

- [部署指南](DEPLOYMENT.md) - Cloudflare 部署完整說明
- [Nitter 爬蟲說明](data/README.md) - 資料抓取系統使用指南
- [前端資源說明](frontend/page/ASSETS_README.md) - 前端資源管理

## 🔗 相關連結

- [Cloudflare Workers 文件](https://developers.cloudflare.com/workers/)
- [Cloudflare D1 文件](https://developers.cloudflare.com/d1/)
- [Vue.js 3 文件](https://vuejs.org/)
- [Vite 文件](https://vitejs.dev/)
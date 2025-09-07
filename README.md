# いきづらい部！ 部員日誌

基於 Vue.js 3 和 Cloudflare Workers 的成員日誌應用程式，採用舊推特經典配色與現代化UI設計，完整支援桌面版和手機版響應式布局。

## 主要功能

- **響應式設計**：支援桌面版、平板版和手機版，智能布局切換
- **成員篩選**：可依成員、年份、月份篩選推文
- **搜尋功能**：支援推文內容和成員名稱搜尋
- **個人資料系統**：每個成員都有詳細的個人資料頁面
- **日期導航器**：快速跳轉到特定日期的推文
- **主題切換**：支援明暗主題切換
- **推文互動**：點讚、分享功能
- **L高介紹**：主頁包含完整的L高介紹內容
- **手機版導航**：專為手機設計的橫向滾動導航

## 專案結構

```
bluebird-master/
├── backend/                     # 後端 Cloudflare Workers
│   ├── worker/
│   │   ├── src/index.ts        # 主要API邏輯
│   │   └── schema.sql          # 資料庫結構
│   └── package.json
├── frontend/                    # 前端 Vue.js 應用
│   └── page/
│       ├── src/
│       │   ├── App.vue         # 主要應用組件
│       │   ├── main.js         # 應用入口
│       │   ├── components/     # Vue 組件目錄
│       │   │   ├── layout/     # 佈局組件
│       │   │   │   ├── LeftSidebar.vue    # 左側邊欄
│       │   │   │   ├── PostsHeader.vue    # 推文標題列
│       │   │   │   ├── MobileNav.vue      # 手機版導航
│       │   │   │   └── RightSidebar.vue   # 右側邊欄
│       │   │   ├── posts/      # 推文相關組件
│       │   │   │   ├── MemberHeader.vue   # 成員橫幅
│       │   │   │   ├── PostList.vue       # 推文列表
│       │   │   │   └── PostItem.vue       # 推文項目
│       │   │   ├── modals/     # 彈窗組件
│       │   │   │   ├── PostDetailModal.vue  # 推文詳情彈窗
│       │   │   │   ├── ProfileModal.vue     # 個人資料彈窗
│       │   │   │   └── DateNavModal.vue     # 日期導航彈窗
│       │   │   ├── ui/         # UI 通用組件
│       │   │   │   ├── Loader.vue           # 載入器
│       │   │   │   ├── ToTopButton.vue      # 回到頂部按鈕
│       │   │   │   ├── ToastNotification.vue # Toast 通知
│       │   │   │   └── TimelineBar.vue      # 時間軸裝飾組件
│       │   ├── utils/          # 工具函數
│       │   │   ├── assets.js   # 資源管理
│       │   │   └── html2canvas-helper.js # 圖片分享
│       │   └── assets/
│       │       └── styles.css  # 全域樣式檔案
│       └── package.json
└── README.md
```

## 快速開始

### 1. 啟動後端服務

```bash
cd backend/worker
npm install
npm run dev
```

後端服務將在 `http://localhost:8787` 運行。

### 2. 啟動前端應用

```bash
cd frontend/page
npm install
npm run dev
```

前端應用將在 `http://localhost:5173` 運行。

### 3. 初始化資料庫

後端服務啟動後，資料庫會自動使用預設的成員和推文資料。

## API 端點

- `GET /api/members` - 獲取所有成員資訊
- `GET /api/tweets` - 獲取推文列表（支援篩選）
- `GET /api/stats` - 獲取統計資訊
- `POST /api/tweets` - 新增推文
- `POST /api/likes` - 處理喜歡/取消喜歡
- `GET /api/likes/status` - 獲取喜歡狀態

## 主要功能

### 成員系統
- 10位成員，每位都有獨特的顏色主題
- 個人資料頁面，包含詳細資訊
- 支援成員篩選

### 推文系統
- 支援文字內容和圖片
- 自動解析hashtag
- 時間軸顯示
- 喜歡功能

### 搜尋和篩選
- 全文搜尋
- 按成員篩選
- 按日期篩選
- 只顯示喜歡的推文

### 主題系統
- 深色/淺色主題
- 成員主題色彩
- 自動主題切換

## 技術特點

### 前端技術
- **Vue.js 3**：使用 Composition API 和響應式系統
- **CSS 變數系統**：統一的設計系統和主題管理
- **響應式設計**：支援多種螢幕尺寸和設備
- **圖示系統**：Material Symbols Outlined 圖示字體
- **字體優化**：Noto Sans JP 字體 CDN 載入

### 後端技術
- **Cloudflare Workers**：邊緣運算平台
- **SQLite (D1)**：輕量級資料庫
- **RESTful API**：標準化的 API 設計

### 功能特色
- **推文篩選**：多維度篩選系統
- **搜尋功能**：全文搜尋和即時結果
- **日期導航**：智能日期跳轉系統
- **個人資料**：完整的成員資料管理
- **圖片分享**：html2canvas 圖片生成

## 組件架構

### 佈局組件
- **LeftSidebar.vue** - 左側邊欄，包含主導航、搜尋、成員篩選、主題切換
- **PostsHeader.vue** - 推文區標題列，包含手機版操作按鈕
- **MobileNav.vue** - 手機版橫向滾動導航，成員頭像選擇
- **RightSidebar.vue** - 右側邊欄，日期導航器和年月篩選

### 推文組件
- **MemberHeader.vue** - 成員橫幅，顯示選擇成員的頭像、名稱、自我介紹按鈕
- **PostList.vue** - 推文列表容器，管理推文項目和空狀態
- **PostItem.vue** - 單個推文項目，包含頭像、內容、互動按鈕

### 彈窗組件
- **PostDetailModal.vue** - 推文詳情彈窗，顯示完整推文內容
- **ProfileModal.vue** - 個人資料彈窗，顯示成員詳細資訊
- **DateNavModal.vue** - 手機版日期導航彈窗，年月日期選擇

### UI 組件
- **Loader.vue** - 載入動畫，資料載入時顯示
- **ToTopButton.vue** - 回到頂部按鈕，長頁面滾動輔助
- **ToastNotification.vue** - Toast 通知，操作結果提示
- **TimelineBar.vue** - 時間軸裝飾組件，視覺化推文分佈

## 響應式設計

- **桌面版**：三欄式布局（左側導航、中間時間軸、右側日期導航）
- **平板版**：隱藏右側日期導航，保持雙欄布局
- **手機版**：單欄布局，頂部手機版導航，橫向滾動成員選擇

## 主題系統

- **明暗主題**：支援自動切換和手動切換
- **成員主題**：每個成員都有獨特的品牌色彩
- **CSS 變數**：統一的設計系統和色彩管理

## 開發說明

### 新增推文
推文會自動從後端資料庫載入，支援即時更新。

### 自定義樣式
所有樣式都在 `frontend/page/src/assets/styles.css` 中定義，使用CSS變數系統。

### 響應式設計
專案完全支援響應式設計，在不同螢幕尺寸下都有良好的使用體驗。

## 部署

### 後端部署
```bash
cd backend/worker
npm run deploy
```

### 前端部署
```bash
cd frontend/page
npm run build
```

## 貢獻

歡迎提交Issue和Pull Request來改善這個專案！

## 授權

本專案僅供學習和研究使用。




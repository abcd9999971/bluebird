# いきづらい部！ 部員日誌

基於 Vue.js 3 和 Cloudflare Workers 的成員日誌應用程式，採用舊推特經典配色與現代化UI設計，完整支援桌面版和手機版響應式布局。

## 📋 目錄

- [快速開始](#-快速開始)
- [主要功能](#-主要功能)
- [技術架構](#-技術架構)
- [組件架構](#-組件架構)
- [專案結構](#-專案結構)
- [API 文檔](#-api-文檔)
- [開發指南](#-開發指南)
- [部署說明](#-部署說明)

## 🚀 快速開始

### 環境要求
- Node.js 20.19.0+ 或 22.12.0+
- npm 或 yarn

### 安裝與運行

#### 1. 啟動後端服務
```bash
cd backend/worker
npm install
npm run dev
```
後端服務將在 `http://localhost:8787` 運行。

#### 2. 啟動前端應用
```bash
cd frontend/page
npm install
npm run dev
```
前端應用將在 `http://localhost:5173` 運行。

#### 3. 初始化資料庫
後端服務啟動後，資料庫會自動使用預設的成員和推文資料。

## ✨ 主要功能

### 🎯 核心功能
- **響應式設計**：支援桌面版、平板版和手機版，智能布局切換
- **成員篩選**：可依成員、年份、月份篩選推文
- **搜尋功能**：支援推文內容和成員名稱搜尋，搜尋結果高亮顯示
- **個人資料系統**：每個成員都有詳細的個人資料頁面
- **日期導航器**：快速跳轉到特定日期的推文

### 🎨 用戶體驗
- **主題切換**：支援明暗主題切換
- **推文互動**：點讚、分享功能
- **滑動手勢**：左滑點讚，右滑分享
- **下拉刷新**：手機版下拉刷新推文
- **鍵盤快捷鍵**：J/K 上下瀏覽，L 點讚，R 分享，Esc 關閉

### 📱 手機版特色
- **手機版導航**：專為手機設計的橫向滾動導航
- **底部導航欄**：手機版快速導航
- **橫屏適配**：優化手機橫屏模式布局
- **生日提醒**：成員生日時顯示特別提醒橫幅

### ⚡ 性能優化
- **保守性能優化**：採用CSS硬體加速和圖片預載入，確保所有推文都能正常載入
- **智能時間軸分組**：基於節點壅擠度自動切換月份顯示模式，避免時間軸過於擁擠
- **組件架構優化**：清理未使用的組件，確保所有組件都在正確的目錄結構中

## 🏗️ 技術架構

### 前端技術棧
- **Vue.js 3**：使用 Composition API 和響應式系統
- **Vite**：快速的前端建構工具
- **Vue I18n**：國際化支援
- **html2canvas**：推文圖片生成

### 後端技術棧
- **Cloudflare Workers**：邊緣運算平台
- **SQLite (D1)**：輕量級資料庫
- **RESTful API**：標準化的 API 設計

### 設計系統
- **CSS 變數系統**：統一的設計系統和主題管理
- **響應式設計**：支援多種螢幕尺寸和設備，包含橫屏適配
- **圖示系統**：Material Symbols Outlined 圖示字體
- **字體優化**：Noto Sans JP 字體 CDN 載入

## 🧩 組件架構

本專案採用 Vue 3 Composition API 和模組化組件設計，遵循單一職責原則和關注點分離。

### 架構設計理念

1. **分層架構**：UI組件 → 業務組件 → 佈局組件 → 頁面組件
2. **職責分離**：每個組件只負責特定功能，避免職責混雜
3. **可重用性**：UI組件和業務組件可在不同場景中重用
4. **狀態管理**：使用 Composables 集中管理狀態和邏輯
5. **響應式優先**：所有組件都支援桌面、平板、手機三種尺寸

### 組件層級關係

```
App.vue (根組件)
├── 佈局組件層 (Layout Components)
│   ├── AppLayout.vue (統一佈局包裝)
│   ├── LeftSidebar.vue
│   ├── PostsHeader.vue  
│   ├── MobileNav.vue
│   ├── RightSidebar.vue
│   └── BottomNavigation.vue
├── 業務組件層 (Business Components)
│   ├── MemberHeader.vue
│   ├── PostList.vue
│   └── PostItem.vue
├── 彈窗組件層 (Modal Components)
│   ├── PostDetailModal.vue
│   ├── ProfileModal.vue
│   └── DateNavModal.vue
└── UI組件層 (UI Components)
    ├── Loader.vue
    ├── ToTopButton.vue
    ├── ToastNotification.vue
    ├── TimelineBar.vue
    ├── PullRefreshIndicator.vue
    └── BirthdayReminder.vue
```

### 組件分類詳解

#### 佈局組件 (Layout Components)
- **AppLayout.vue** - 統一佈局包裝組件，整合所有佈局相關組件
- **LeftSidebar.vue** - 左側邊欄，包含主導航、搜尋、成員篩選、主題切換
- **PostsHeader.vue** - 推文區標題列，簡化版標題顯示
- **MobileNav.vue** - 手機版橫向滾動導航，成員頭像選擇
- **RightSidebar.vue** - 右側邊欄，日期導航器和年月篩選
- **BottomNavigation.vue** - 底部導航欄，手機版快速導航

#### 推文組件 (Post Components)
- **MemberHeader.vue** - 成員橫幅，顯示選擇成員的頭像、名稱、自我介紹按鈕
- **PostList.vue** - 推文列表容器，管理推文項目和空狀態
- **PostItem.vue** - 單個推文項目，包含頭像、內容、互動按鈕，支援點擊成員名稱篩選

#### 彈窗組件 (Modal Components)
- **PostDetailModal.vue** - 推文詳情彈窗，顯示完整推文內容
- **ProfileModal.vue** - 個人資料彈窗，顯示成員詳細資訊
- **DateNavModal.vue** - 手機版日期導航彈窗，年月日期選擇

#### UI組件 (UI Components)
- **Loader.vue** - 載入動畫，資料載入時顯示
- **ToTopButton.vue** - 回到頂部按鈕，長頁面滾動輔助
- **ToastNotification.vue** - Toast 通知，操作結果提示
- **TimelineBar.vue** - 時間軸裝飾組件，視覺化推文分佈，智能月份分組避免節點壅擠
- **PullRefreshIndicator.vue** - 下拉刷新指示器，手機版刷新功能
- **BirthdayReminder.vue** - 生日提醒，成員生日時顯示

### Composables 組合式函數
- **useApi.js** - API 請求管理，統一處理所有後端通訊
- **useAppState.js** - 應用程式狀態管理，集中管理全域狀態
- **useImageLoader.js** - 圖片載入管理，優化圖片載入效能
- **useKeyboardShortcuts.js** - 鍵盤快捷鍵管理，支援 J/K/L/R/Esc 等操作
- **useSwipeGestures.js** - 滑動手勢管理，支援左滑點讚、右滑分享
- **usePullRefresh.js** - 下拉刷新管理，手機版刷新功能

### 組件間通信機制

1. **Props 向下傳遞**：父組件向子組件傳遞資料和配置
2. **Events 向上傳遞**：子組件通過 emit 向父組件發送事件
3. **Composables 狀態共享**：使用 `useAppState` 實現跨組件狀態共享
4. **Provide/Inject**：深層組件間的直接通信（用於主題、配置等）

### 狀態管理架構

```
useAppState (全域狀態中心)
├── 用戶偏好 (prefs)
│   ├── 主題設定 (dark/light)
│   └── 語言設定
├── 應用狀態 (ui)
│   ├── 載入狀態
│   ├── 彈窗控制
│   └── 搜尋狀態
├── 資料狀態
│   ├── 推文資料 (allTweets)
│   ├── 成員資料 (authors)
│   └── 篩選條件 (filters)
└── 計算屬性
    ├── 篩選後推文 (filteredTweets)
    ├── 可用年份 (availableYears)
    └── 品牌顏色 (brandColor)
```

### 頁面視圖組件
- **PostDetailView.vue** - 推文詳情頁面，獨立頁面顯示推文內容，包含返回按鈕和完整互動功能
- **TimelineView.vue** - 時間軸頁面，專用的時間軸視圖，整合所有推文相關組件和功能

### 組件開發指南

#### 新增組件原則
1. **單一職責**：每個組件只負責一個特定功能
2. **可重用性**：設計時考慮在不同場景中的重用
3. **Props 驗證**：使用 TypeScript 或 PropTypes 驗證傳入參數
4. **事件命名**：使用動詞開頭的駝峰命名（如 `handleClick`、`onSubmit`）
5. **樣式隔離**：使用 `scoped` 樣式避免樣式污染

#### 組件命名規範
- **佈局組件**：描述其佈局功能（如 `LeftSidebar`、`BottomNavigation`）
- **業務組件**：描述其業務功能（如 `PostItem`、`MemberHeader`）
- **UI組件**：描述其UI功能（如 `Loader`、`ToastNotification`）
- **彈窗組件**：以 `Modal` 結尾（如 `PostDetailModal`）

#### 組件目錄結構
```
components/
├── index.js           # 統一導出文件
├── layout/            # 佈局相關組件
├── modals/            # 彈窗組件
├── posts/             # 推文相關業務組件
└── ui/                # 通用UI組件
```

## 📁 專案結構

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
│       │   │   ├── index.js    # 組件統一導出
│       │   │   ├── layout/     # 佈局組件
│       │   │   │   ├── AppLayout.vue      # 統一佈局包裝
│       │   │   │   ├── LeftSidebar.vue    # 左側邊欄
│       │   │   │   ├── PostsHeader.vue    # 推文標題列
│       │   │   │   ├── MobileNav.vue      # 手機版導航
│       │   │   │   ├── RightSidebar.vue   # 右側邊欄
│       │   │   │   └── BottomNavigation.vue # 底部導航欄
│       │   │   ├── posts/      # 推文相關組件
│       │   │   │   ├── MemberHeader.vue   # 成員橫幅
│       │   │   │   ├── PostList.vue       # 推文列表
│       │   │   │   └── PostItem.vue       # 推文項目
│       │   │   ├── modals/     # 彈窗組件
│       │   │   │   ├── PostDetailModal.vue  # 推文詳情彈窗
│       │   │   │   ├── ProfileModal.vue     # 個人資料彈窗
│       │   │   │   └── DateNavModal.vue     # 日期導航彈窗
│       │   │   └── ui/         # UI 通用組件
│       │   │       ├── Loader.vue           # 載入器
│       │   │       ├── ToTopButton.vue      # 回到頂部按鈕
│       │   │       ├── ToastNotification.vue # Toast 通知
│       │   │       ├── TimelineBar.vue      # 時間軸裝飾組件
│       │   │       ├── PullRefreshIndicator.vue # 下拉刷新指示器
│       │   │       └── BirthdayReminder.vue # 生日提醒
│       │   ├── composables/    # Vue 3 Composition API 組合式函數
│       │   │   ├── useApi.js   # API 請求管理
│       │   │   ├── useAppState.js # 應用程式狀態管理
│       │   │   ├── useImageLoader.js # 圖片載入管理
│       │   │   ├── useKeyboardShortcuts.js # 鍵盤快捷鍵管理
│       │   │   ├── useSwipeGestures.js # 滑動手勢管理
│       │   │   └── usePullRefresh.js # 下拉刷新管理
│       │   ├── views/          # 頁面視圖組件
│       │   │   ├── PostDetailView.vue # 推文詳情頁面
│       │   │   └── TimelineView.vue   # 時間軸頁面
│       │   ├── utils/          # 工具函數
│       │   │   ├── assets.js   # 資源管理
│       │   │   ├── constants.js # 常數定義
│       │   │   ├── formatters.js # 格式化工具
│       │   │   └── html2canvas-helper.js # 圖片分享
│       │   ├── member.json     # 成員資料檔案
│       │   ├── post.json       # 推文資料檔案
│       │   ├── locales/        # 國際化語言檔案
│       │   │   └── ja.json     # 日文語言檔案
│       │   ├── i18n.js         # 國際化配置
│       │   └── assets/
│       │       └── styles.css  # 全域樣式檔案
│       └── package.json
└── README.md
```

## 📚 API 文檔

### 端點列表
- `GET /api/members` - 獲取所有成員資訊
- `GET /api/tweets` - 獲取推文列表（支援篩選）
- `GET /api/stats` - 獲取統計資訊
- `POST /api/tweets` - 新增推文
- `POST /api/likes` - 處理喜歡/取消喜歡
- `GET /api/likes/status` - 獲取喜歡狀態

### 請求參數

#### GET /api/tweets
- `author` (string): 成員ID篩選
- `year` (string): 年份篩選
- `month` (string): 月份篩選
- `search` (string): 搜尋關鍵字
- `limit` (number): 每頁數量，預設50
- `offset` (number): 偏移量，預設0

#### POST /api/likes
```json
{
  "tweetId": 123,
  "userIp": "127.0.0.1",
  "action": "like" // 或 "unlike"
}
```

## 🛠️ 開發指南

### 資料檔案管理
- **`member.json`**：存放成員的靜態資料，包含姓名、顏色、個人資料等
- **`post.json`**：存放推文的備用資料，當後端連接失敗時使用
- 這些 JSON 檔案會在應用程式啟動時載入，並透過 `utils/assets.js` 中的函數處理動態屬性

### 工具函數模組
- **`utils/constants.js`**：統一管理應用程式常數，包含成員顏色、API 端點、儲存鍵值等
- **`utils/formatters.js`**：提供時間、文字、數字等格式化功能
- **`utils/assets.js`**：處理靜態資源載入和成員資料處理
- **`utils/html2canvas-helper.js`**：圖片分享功能，將推文轉換為圖片

### 國際化支援
- 使用 [vue-i18n](https://vue-i18n.intlify.dev/) 進行文本管理
- 目前支援日文，語言包位於 `src/locales/ja.json`
- 所有 UI 文本都透過 `t()` 函數進行翻譯
- 未來可輕鬆擴展至其他語言，只需添加對應的語言包檔案

### 新增推文
推文會自動從後端資料庫載入，支援即時更新。目前已包含100條測試推文，涵蓋2025-2026年的完整時間軸，方便測試各種功能。測試推文內容貼近角色特色，同時明確標示為測試用途。

### 性能優化
- **保守的CSS優化**：使用CSS硬體加速（transform: translateZ(0)）和contain屬性來優化渲染性能
- **圖片預載入**：在組件載入時預載入所有成員頭像，提升用戶體驗
- **圖片渲染優化**：使用image-rendering屬性優化圖片顯示品質
- **簡化架構**：採用直接渲染確保穩定性，移除複雜的虛擬滾動機制
- **智能時間軸分組**：基於節點壅擠度自動切換月份顯示模式，避免時間軸過於擁擠
- **組件架構優化**：清理未使用的組件，確保所有組件都在正確的目錄結構中

### 自定義樣式
所有樣式都在 `frontend/page/src/assets/styles.css` 中定義，使用CSS變數系統。

### 響應式設計
專案完全支援響應式設計，在不同螢幕尺寸下都有良好的使用體驗。

## 🚀 部署說明

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

## 🤝 貢獻

歡迎提交Issue和Pull Request來改善這個專案！

## 📄 授權

本專案僅供學習和研究使用。

---

## 📝 更新日誌

### v1.0.0 (2025-01-XX)
- ✨ 初始版本發布
- 🎨 完整的響應式設計
- 📱 手機版優化
- 🎯 完整的推文系統
- 🔍 搜尋和篩選功能
- 🎭 成員個人資料系統
- ⚡ 性能優化
- 🏗️ 組件架構重構
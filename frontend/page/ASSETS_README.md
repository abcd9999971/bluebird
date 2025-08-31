# 本地資源管理系統

## 概述

本專案已完全遷移到本地資源管理系統，所有圖片資源都存儲在本地，確保 html2canvas 能正確生成包含頭貼的推文圖片。

## 資料夾結構

```
public/assets/images/
├── avatars/          # 成員頭貼
│   ├── polka.png
│   ├── mai.png
│   ├── akira.png
│   ├── hanabi.png
│   ├── miracle.png
│   ├── noriko.png
│   ├── yukuri.png
│   ├── aurora.png
│   ├── midori.png
│   ├── shion.png
│   └── project-avatar.jpg
├── banners/          # 成員橫幅
│   ├── polka-banner.jpg
│   ├── mai-banner.jpg
│   ├── akira-banner.jpg
│   ├── hanabi-banner.jpg
│   ├── miracle-banner.jpg
│   ├── noriko-banner.jpg
│   ├── yukuri-banner.jpg
│   ├── aurora-banner.jpg
│   ├── midori-banner.jpg
│   ├── shion-banner.jpg
│   └── project-banner.jpg
├── logos/            # Logo 和標誌
│   ├── emblem.png
│   └── logo3.svg
└── project/          # 專案相關圖片
    └── satellite.png
```

## 資源管理模組

### `src/utils/assets.js`

統一的資源管理模組，提供：

- `ASSETS`: 所有資源路徑的常數定義
- `MEMBER_AVATARS`: 成員 ID 到頭貼的映射
- `MEMBER_BANNERS`: 成員 ID 到橫幅的映射
- `getMemberAvatar(memberId)`: 獲取成員頭貼
- `getMemberBanner(memberId)`: 獲取成員橫幅
- `preloadImages()`: 預載入所有圖片資源

### `src/utils/html2canvas-helper.js`

專門的 html2canvas 工具模組，提供：

- `captureTweetAsImage()`: 生成推文截圖
- `shareTweetAsImage()`: 完整的推文分享流程
- 優化的配置，確保圖片正確載入

## 使用方法

### 1. 獲取成員資源

```javascript
import { getMemberAvatar, getMemberBanner } from './utils/assets.js';

// 獲取成員頭貼
const avatarUrl = getMemberAvatar('polka');

// 獲取成員橫幅
const bannerUrl = getMemberBanner('polka');
```

### 2. 生成推文圖片

```javascript
import { shareTweetAsImage } from './utils/html2canvas-helper.js';

// 生成並下載推文圖片
const success = await shareTweetAsImage(tweet, author, isDarkMode);
```

### 3. 預載入資源

```javascript
import { preloadImages } from './utils/assets.js';

// 預載入所有圖片資源（用於 html2canvas）
await preloadImages();
```

## 下載腳本

### `download-assets.cjs`

用於下載所有需要的圖片資源到本地：

```bash
node download-assets.cjs
```

## 優勢

1. **解決 CORS 問題**: 本地資源避免了跨域限制
2. **確保圖片載入**: html2canvas 能正確處理本地圖片
3. **統一管理**: 所有資源路徑集中管理
4. **易於維護**: 清晰的資料夾結構和命名規範
5. **性能優化**: 預載入機制確保圖片快速載入

## 注意事項

1. 確保所有圖片資源都已下載到正確的資料夾
2. 新增成員時需要同時更新資源管理模組和下載腳本
3. 圖片檔案命名必須與程式碼中的映射一致
4. 定期檢查圖片資源是否完整

## 更新流程

當需要新增或更新圖片資源時：

1. 更新 `download-assets.cjs` 中的資源配置
2. 執行下載腳本：`node download-assets.cjs`
3. 更新 `src/utils/assets.js` 中的映射
4. 測試確保所有功能正常運作

## 修正記錄

### 2025-08-31
- 修正所有成員橫幅 URL，確保每個成員都有正確的橫幅圖片
- 更新下載腳本中的橫幅配置
- 重新下載所有橫幅圖片

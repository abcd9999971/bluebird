<template>
  <!-- 
    いきづらい部！ 部員日誌 - 主要應用程式根組件
    
    此組件作為整個應用程式的根組件，負責：
    1. 應用程式的整體結構和佈局
    2. 載入狀態的管理
    3. 主要組件的協調和資料傳遞
    4. 全域狀態的統一管理
    
    架構設計理念：
    - 採用分層架構，將 UI 和邏輯分離
    - 使用組合式 API 進行狀態管理
    - 響應式設計，支援桌面版和手機版
    - 模組化組件設計，提升可維護性
  -->
  <div id="app">
    <!-- 
      應用程式邏輯組件
      管理所有的業務邏輯、狀態和事件處理
      此組件不包含 UI 元素，僅作為邏輯容器
    -->
    <AppLogic ref="appLogic" />
    
    <!-- 
      載入器組件
      在應用程式資料載入完成前顯示載入動畫
      確保使用者體驗的流暢性
    -->
    <BaseLoader v-if="!appLogic?.ui?.loaded" />
    
    <!-- 
      主要應用程式界面
      當資料載入完成後顯示完整的應用程式界面
    -->
    <div v-else-if="appLogic" class="app-shell">
      <!-- 
        應用程式佈局組件
        負責整體的佈局結構，包含：
        - 左側邊欄（導航、搜尋、篩選）
        - 主要內容區域（時間軸）
        - 右側邊欄（日期導航）
        - 時間軸裝飾桿
      -->
      <AppLayout
        :filters="appLogic.filters"
        :ui="appLogic.ui"
        :prefs="appLogic.prefs"
        :authors="appLogic.authors"
        :characterOrder="appLogic.characterOrder"
        :dateGroups="appLogic.dateGroups"
        :scroller="appLogic.scroller"
        :brandColor="appLogic.brandColor"
        :availableYears="appLogic.availableYears"
        :availableMonths="appLogic.availableMonths"
        @resetFilters="appLogic.resetFilters"
        @focusSearch="appLogic.focusSearch"
        @onSearchBlur="appLogic.onSearchBlur"
        @toggleLikedFilter="appLogic.toggleLikedFilter"
        @setMemberFilter="appLogic.setMemberFilter"
        @toggleTheme="appLogic.toggleTheme"
        @setYear="appLogic.setYear"
        @setMonthFilter="appLogic.setMonthFilter"
        @scrollToDate="appLogic.scrollToDate"
      >
        <!-- 
          時間軸視圖插槽
          將時間軸相關的組件和功能整合在一個視圖中
          包含：標題列、搜尋框、導航、成員橫幅、推文列表
        -->
        <template #timeline>
          <TimelineView
            :ui="appLogic.ui"
            :filters="appLogic.filters"
            :prefs="appLogic.prefs"
            :authors="appLogic.authors"
            :characterOrder="appLogic.characterOrder"
            :projectInfo="appLogic.projectInfo"
            :filteredTweets="appLogic.filteredTweets"
            :headerTitle="appLogic.headerTitle"
            @focusSearch="appLogic.focusSearch"
            @toggleMobileSearch="appLogic.toggleMobileSearch"
            @openDateNavigationModal="appLogic.openDateNavigationModal"
            @onSearchBlur="appLogic.onSearchBlur"
            @toggleTheme="appLogic.toggleTheme"
            @resetFilters="appLogic.resetFilters"
            @toggleLikedFilter="appLogic.toggleLikedFilter"
            @setMemberFilter="appLogic.setMemberFilter"
            @openProfileModal="appLogic.openProfileModal"
            @openDetail="appLogic.openDetail"
            @toggleLike="appLogic.toggleLike"
            @shareTweet="appLogic.shareTweet"
            @handleTweetTextClick="appLogic.handleTweetTextClick"
          />
        </template>
      </AppLayout>

      <!-- 
        全域組件容器
        管理所有全域性的組件，包含：
        - 彈窗組件（推文詳情、個人資料、日期導航）
        - 通知組件（Toast、回到頂部按鈕）
        - 互動組件（下拉刷新、底部導航、生日提醒）
      -->
      <GlobalComponents
        :ui="appLogic.ui"
        :filters="appLogic.filters"
        :prefs="appLogic.prefs"
        :authors="appLogic.authors"
        :availableYears="appLogic.availableYears"
        :availableMonths="appLogic.availableMonths"
        :dateGroups="appLogic.dateGroups"
        :scroller="appLogic.scroller"
        :toast="appLogic.toast"
        :pullRefreshState="appLogic.pullRefreshState"
        :shouldShowRefreshIndicator="appLogic.shouldShowRefreshIndicator"
        @closeAllModals="appLogic.closeAllModals"
        @setYear="appLogic.setYear"
        @setMonthFilter="appLogic.setMonthFilter"
        @scrollToDate="appLogic.scrollToDate"
        @resetFilters="appLogic.resetFilters"
        @focusSearch="appLogic.focusSearch"
        @toggleLikedFilter="appLogic.toggleLikedFilter"
        @openDateNavigationModal="appLogic.openDateNavigationModal"
        @toggleTheme="appLogic.toggleTheme"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

/**
 * いきづらい部！ 部員日誌 - 主要應用程式根組件
 * 
 * 此組件採用最新的 Vue 3 組合式 API 設計，主要職責：
 * 1. 作為應用程式的根組件，協調各個子組件
 * 2. 管理應用程式的整體狀態和生命週期
 * 3. 處理組件間的資料傳遞和事件通信
 * 4. 提供統一的錯誤處理和載入狀態管理
 * 
 * 架構特色：
 * - 分層架構：UI 層、邏輯層、資料層分離
 * - 組合式 API：使用 Vue 3 的組合式 API 進行狀態管理
 * - 響應式設計：支援桌面版、平板、手機三種尺寸
 * - 模組化設計：每個組件職責明確，便於維護和測試
 * - 國際化支援：使用 vue-i18n 進行多語言支援
 * 
 * 維護注意事項：
 * - 此組件主要負責組件協調，具體業務邏輯已移至 AppLogic.vue
 * - 新增功能時請優先考慮在對應的子組件中實現
 * - 修改狀態管理邏輯時請同步更新 AppLogic.vue
 * - 保持組件間的鬆耦合，避免直接操作子組件內部狀態
 */

// === 組件引入 ===
import BaseLoader from './components/ui/BaseLoader.vue';
import AppLayout from './components/layout/AppLayout.vue';
import TimelineView from './components/views/TimelineView.vue';
import GlobalComponents from './components/containers/GlobalComponents.vue';
import AppLogic from './components/containers/AppLogic.vue';

// === 應用程式邏輯管理 ===
// 使用 AppLogic 組件來管理所有的業務邏輯和狀態
// 這樣可以將 App.vue 專注於組件協調和 UI 結構
const appLogic = ref(null);

// === 生命週期管理 ===
onMounted(() => {
  // 應用程式掛載完成
  // 所有的初始化邏輯都在 AppLogic 組件中處理
  console.log('いきづらい部！ 部員日誌應用程式已啟動');
});
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  background-color: var(--bg-primary);
}
</style>
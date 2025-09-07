<template>
  <!-- 時間軸標題 -->
  <header class="timeline-header">
    <div class="mobile-header">
      <!-- 手機版搜尋按鈕 -->
      <button class="action-btn" @click="toggleMobileSearch" :title="t('search_placeholder')">
        <span class="icon">{{ ui.showMobileSearch ? 'close' : 'search' }}</span>
      </button>
      <!-- 手機版日期導航按鈕 -->
      <button class="action-btn" @click="openDateNavModal" :title="t('quick_scroll_title')">
        <span class="icon">calendar_month</span>
      </button>
      <!-- 手機版搜尋輸入框 -->
      <input 
        v-if="ui.showMobileSearch" 
        ref="mobileSearchInput" 
        type="text" 
        class="search-input mobile-search-input" 
        :placeholder="t('search_placeholder')" 
        v-model.trim="filters.search" 
        @blur="onSearchBlur" 
      />
    </div>
    <!-- 標題文字 -->
    <h1 v-if="!ui.showMobileSearch">{{ headerTitle }}</h1>
    <div class="mobile-header" v-if="!ui.showMobileSearch">
      <!-- 手機版主題切換按鈕 -->
      <button class="action-btn" @click="toggleTheme" :title="t('dark_mode_label')">
        <span class="icon">{{ prefs.dark ? 'dark_mode' : 'light_mode' }}</span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';

// 定義 props - 從父組件接收的資料
const props = defineProps({
  ui: Object,
  filters: Object,
  prefs: Object,
  headerTitle: String
});

// 定義 emits - 向父組件發送的事件
const emit = defineEmits([
  'focusSearch',
  'openDateNavModal', 
  'onSearchBlur',
  'toggleTheme',
  'toggleMobileSearch'
]);

// 手機版搜尋輸入框的 ref
const mobileSearchInput = ref(null);

// 翻譯函數 - 獲取多語言文字
const t = (key) => {
  const translations = {
    'ja': { 
      search_placeholder: '日誌を検索',
      quick_scroll_title: '日付で移動',
      dark_mode_label: 'テーマ切り替え'
    }
  };
  return translations['ja']?.[key] || key;
};

// 事件處理函數 - 聚焦搜尋框
const focusSearch = () => emit('focusSearch');

// 事件處理函數 - 切換手機版搜尋框
const toggleMobileSearch = () => emit('toggleMobileSearch');

// 事件處理函數 - 開啟日期導航彈窗
const openDateNavModal = () => emit('openDateNavModal');

// 事件處理函數 - 搜尋框失去焦點時的處理
const onSearchBlur = () => emit('onSearchBlur');

// 事件處理函數 - 切換主題
const toggleTheme = () => emit('toggleTheme');
</script>

<style scoped>
.timeline-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 58px;
  backdrop-filter: blur(12px);
}

.mobile-header {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) / 2);
}

h1 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  flex: 1;
  text-align: center;
}

.action-btn {
  display: flex;
  align-items: center;
  border: none;
  background: transparent;
  padding: var(--spacing-unit);
  border-radius: 50%;
  color: var(--text-secondary);
  transition: var(--transition-fast);
  cursor: pointer;
}

.action-btn:hover {
  transform: scale(1.1);
  background-color: var(--bg-hover);
}

.icon {
  font-family: 'Material Symbols Outlined';
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-feature-settings: 'liga';
  -webkit-font-smoothing: antialiased;
  vertical-align: middle;
}

.mobile-search-input {
  flex-grow: 1;
  margin: 0 var(--spacing-unit);
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
  border: 1px solid var(--border-secondary);
  border-radius: var(--radius-full);
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: 1rem;
  transition: var(--transition-fast);
}

.mobile-search-input:focus {
  outline: none;
  border-color: var(--brand-color);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand-color) 20%, transparent);
}

/* 桌面版樣式 */
@media (min-width: 769px) {
  .mobile-header {
    display: none;
  }
  
  h1 {
    text-align: left;
  }
}

/* 手機版樣式 */
@media (max-width: 768px) {
  .timeline-header {
    padding: calc(var(--spacing-unit) * 0.75);
  }
  
  h1 {
    font-size: 1.1rem;
  }
}
</style>

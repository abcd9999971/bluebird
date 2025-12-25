<template>
  <!-- 手機版底部導航欄 -->
  <nav class="bottom-navigation">
    <!-- 主頁按鈕 -->
    <button 
      class="nav-item" 
      :class="{ active: !filters.member && !filters.onlyLiked }"
      @click="resetFilters"
    >
      <span class="nav-icon">home</span>
      <span class="nav-label">{{ t('home_button_text') }}</span>
    </button>

    <!-- 搜尋按鈕 -->
    <button 
      class="nav-item" 
      :class="{ active: filters.search }"
      @click="focusSearch"
    >
      <span class="nav-icon">search</span>
      <span class="nav-label">{{ t('search_placeholder') }}</span>
    </button>

    <!-- 喜歡的日誌按鈕 -->
    <button 
      class="nav-item" 
      :class="{ active: filters.onlyLiked }"
      @click="toggleLikedFilter"
    >
      <span class="nav-icon">favorite</span>
      <span class="nav-label">{{ t('filter_liked') }}</span>
    </button>

    <!-- 日期導航按鈕 -->
    <button 
      class="nav-item" 
      @click="openDateNavigationModal"
    >
      <span class="nav-icon">calendar_month</span>
      <span class="nav-label">{{ t('date_navigation') }}</span>
    </button>

    <!-- 主題切換按鈕 -->
    <button 
      class="nav-item" 
      @click="toggleTheme"
    >
      <span class="nav-icon">{{ prefs.dark ? 'light_mode' : 'dark_mode' }}</span>
      <span class="nav-label">{{ t('theme_toggle') }}</span>
    </button>
  </nav>
</template>

<script setup>
// 定義 props
const props = defineProps({
  filters: Object,
  prefs: Object
});

// 定義 emits
const emit = defineEmits([
  'resetFilters',
  'focusSearch',
  'toggleLikedFilter',
  'openDateNavigationModal',
  'toggleTheme'
]);

// 翻譯函數
const t = (key) => {
  const translations = {
    'ja': {
      home_button_text: 'ホーム',
      search_placeholder: '検索',
      filter_liked: 'いいね',
      date_navigation: '日付',
      theme_toggle: 'テーマ'
    }
  };
  return translations['ja']?.[key] || key;
};

// 事件處理函數
const resetFilters = () => emit('resetFilters');
const focusSearch = () => emit('focusSearch');
const toggleLikedFilter = () => emit('toggleLikedFilter');
const openDateNavigationModal = () => emit('openDateNavigationModal');
const toggleTheme = () => emit('toggleTheme');
</script>

<style scoped>
.bottom-navigation {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--glass-bg);
  border-top: var(--glass-border);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: calc(var(--spacing-unit) * 0.5) 0;
  z-index: 100;
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.25);
  padding: calc(var(--spacing-unit) * 0.5);
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-fast);
  border-radius: var(--radius-sm);
  min-width: 60px;
}

.nav-item:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.nav-item.active {
  color: var(--brand-color);
  background-color: color-mix(in srgb, var(--brand-color) 10%, transparent);
}

.nav-icon {
  font-family: 'Material Symbols Outlined';
  font-size: 20px;
  line-height: 1;
}

.nav-label {
  font-size: 0.7rem;
  font-weight: 500;
  white-space: nowrap;
}

/* 桌面版隱藏 */
@media (min-width: 769px) {
  .bottom-navigation {
    display: none;
  }
}

/* 安全區域適配 */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .bottom-navigation {
    padding-bottom: calc(var(--spacing-unit) * 0.5 + env(safe-area-inset-bottom));
  }
}
</style>

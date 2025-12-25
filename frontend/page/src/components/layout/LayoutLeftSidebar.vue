<template>
  <!-- 左側邊欄 -->
  <aside class="sidebar-left">
    <div class="main-nav">
      <!-- 主頁按鈕 -->
      <button class="nav-btn" :class="{ active: !filters.member && !filters.onlyLiked }" @click="resetFilters">
        <span class="icon">home</span>
        {{ t('home_button_text') }}
      </button>
      
      <!-- 搜尋框/按鈕 -->
      <div v-if="ui.showSearchInput" class="search-container">
        <input 
          ref="searchInput"
          v-model="filters.search"
          type="text" 
          class="search-input" 
          :placeholder="t('search_placeholder')"
          @blur="onSearchBlur"
        >
      </div>
      <button v-else class="nav-btn" @click="focusSearch">
        <span class="icon">search</span>
        {{ t('search_placeholder') }}
      </button>
      
      <!-- 喜歡的日誌篩選按鈕 -->
      <button class="nav-btn" :class="{ active: filters.onlyLiked }" @click="toggleLikedFilter">
        <span class="icon">favorite</span>
        {{ t('filter_liked') }}
      </button>
    </div>

      <!-- 成員篩選區域 -->
      <div class="filters-nav">
       <button 
         v-for="memberId in characterOrder" 
         :key="memberId"
         class="nav-btn member-btn" 
         :class="{ active: filters.member === memberId }"
         :data-member-id="memberId"
         @click="setMemberFilter(memberId)"
       >
         <img :src="authors[memberId]?.avatar_url || ''" :alt="authors[memberId]?.name_ja || memberId" class="filter-avatar">
         <span class="nav-text">{{ authors[memberId]?.name_ja || memberId }}</span>
       </button>
      </div>

    <!-- 說明小卡 -->
    <div class="info-card">
      <img src="/assets/images/logos/logo3.svg" alt="Logo">
      <div v-html="t('unofficial_site_notice')"></div>
    </div>
    
    <!-- 主題切換按鈕 -->
    <div class="settings-btn-container">
      <button class="nav-btn" @click="toggleTheme">
        <span class="icon">{{ prefs.dark ? 'light_mode' : 'dark_mode' }}</span>
        {{ t('dark_mode_label') }}
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, nextTick, onMounted, onBeforeUnmount } from 'vue';

/**
 * Props 定義 - 從父組件接收的資料
 */
const props = defineProps({
  filters: Object,      // 篩選條件狀態
  ui: Object,          // UI 顯示狀態
  prefs: Object,       // 使用者偏好設定
  authors: Object,     // 成員資料
  characterOrder: Array // 成員顯示順序
});

/**
 * Emits 定義 - 向父組件發送的事件
 */
const emit = defineEmits([
  'resetFilters',       // 重置所有篩選條件
  'focusSearch',        // 聚焦搜尋框
  'onSearchBlur',       // 搜尋框失去焦點
  'toggleLikedFilter',  // 切換喜愛篩選
  'setMemberFilter',    // 設定成員篩選
  'toggleTheme'         // 切換主題
]);

// 搜尋輸入框的 ref
const searchInput = ref(null);

/**
 * 成員印象色配置 - 各成員專屬的品牌色彩
 */
const memberColors = {
  'polka': '#ccb12e',   // 高橋ポルカ - 金黃色
  'mai': '#009fdf',     // 麻布麻衣 - 藍色  
  'akira': '#88d66e',   // 五桐玲 - 綠色
  'hanabi': '#ff2021',  // 駒形花火 - 紅色
  'miracle': '#ffb7f1', // 金澤奇跡 - 粉色
  'noriko': '#ae62ff',  // 調布のりこ - 紫色
  'yukuri': '#5ecbd1',  // 春宮ゆかり - 青綠色
  'aurora': '#fd589e',  // 此花輝夜 - 玫瑰色
  'midori': '#16b500',  // 山田真緑 - 深綠色
  'shion': '#9b9b9b'    // 佐々木翔音 - 灰色
};

/**
 * 設定成員按鈕的 hover 效果
 * 動態綁定成員印象色並處理滑鼠懸停時的視覺反饋
 */
const setupMemberHoverEffects = () => {
  const memberButtons = document.querySelectorAll('.filters-nav .nav-btn');
  
  memberButtons.forEach((button, index) => {
    const memberId = props.characterOrder[index];
    const memberColor = memberColors[memberId] || props.authors[memberId]?.color;
    
    if (memberColor) {
      button.addEventListener('mouseenter', () => {
        button.style.setProperty('--member-color', memberColor);
        button.classList.add('member-hover');
      });
      
      button.addEventListener('mouseleave', () => {
        button.classList.remove('member-hover');
        button.style.removeProperty('--member-color');
      });
    }
  });
};

/**
 * 組件掛載後執行
 * 等待 DOM 更新完成後設定成員按鈕的 hover 效果
 */
onMounted(() => {
  nextTick(() => {
    setupMemberHoverEffects();
  });
});

/**
 * 組件卸載前清理
 * 移除所有事件監聽器以避免記憶體洩漏
 */
onBeforeUnmount(() => {
  const memberButtons = document.querySelectorAll('.filters-nav .nav-btn');
  memberButtons.forEach(button => {
    button.removeEventListener('mouseenter', null);
    button.removeEventListener('mouseleave', null);
  });
});

// 使用統一的國際化系統
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

// 事件處理函數 - 重置所有篩選條件
const resetFilters = () => emit('resetFilters');

// 事件處理函數 - 聚焦搜尋框
const focusSearch = () => emit('focusSearch');

// 事件處理函數 - 搜尋框失去焦點時的處理
const onSearchBlur = () => emit('onSearchBlur');

// 事件處理函數 - 切換喜歡篩選
const toggleLikedFilter = () => emit('toggleLikedFilter');

// 事件處理函數 - 設定成員篩選
const setMemberFilter = (memberId) => emit('setMemberFilter', memberId);

// 事件處理函數 - 切換主題
const toggleTheme = () => emit('toggleTheme');
</script>

<style scoped>
.sidebar-left {
  width: 300px;
  padding: var(--spacing-unit);
  position: sticky;
  top: 0;
  height: 100vh;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(12px);
}

.main-nav {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing-unit) / 2);
  margin-bottom: var(--spacing-unit);
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-unit);
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 1.5);
  background: transparent;
  border: none;
  color: var(--text-primary);
  text-align: left;
  cursor: pointer;
  border-radius: var(--radius-full);
  transition: var(--transition-fast);
  font-size: 1.2rem;
  font-weight: 400;
  width: fit-content;
}

.nav-btn:hover {
  background-color: var(--bg-hover);
  transform: scale(1.03);
}

.nav-btn.active {
  font-weight: 700;
  color: var(--brand-color);
  background-color: color-mix(in srgb, var(--brand-color) 10%, transparent);
  transform: scale(1.02);
  box-shadow: var(--shadow-2);
}

/* 成員按鈕特殊樣式 */
.nav-btn.member-btn {
  position: relative;
  overflow: hidden;
  transition: var(--transition-bounce);
}

.nav-btn.member-btn .nav-text {
  transition: var(--transition-smooth);
}

/* 成員印象色hover效果 */
.nav-btn.member-btn:hover:not(.active) {
  transform: scale(1.05) translateY(-1px);
  box-shadow: var(--shadow-2);
  background-color: var(--bg-hover);
}

.nav-btn.member-btn:hover:not(.active) .nav-text {
  color: var(--member-color, var(--brand-color));
  font-weight: 600;
}

/* 活躍狀態的成員按鈕使用印象色 */
.nav-btn.member-btn.active {
  transform: scale(1.02);
  box-shadow: var(--shadow-2);
  background-color: color-mix(in srgb, var(--member-color, var(--brand-color)) 10%, transparent);
}
.nav-btn.member-btn.active .nav-text {
  color: var(--member-color, var(--brand-color));
  font-weight: 700;
}

.search-container {
  margin-block: calc(var(--spacing-unit) / 2);
}

.search-input {
  width: 100%;
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
  border: 1px solid var(--border-secondary);
  border-radius: var(--radius-full);
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: 1rem;
  transition: var(--transition-fast);
}

.search-input:focus {
  outline: none;
  border-color: var(--brand-color);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand-color) 20%, transparent);
}

.filters-nav {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing-unit) / 2);
  border-top: 1px solid var(--border-primary);
  margin-top: calc(var(--spacing-unit) * 2);
  padding-top: calc(var(--spacing-unit) * 2);
}

.filter-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
}

.info-card {
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 1.5);
  margin-top: calc(var(--spacing-unit) * 2);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: var(--spacing-unit);
  background-color: color-mix(in srgb, var(--bg-secondary) 50%, transparent);
}

.info-card img {
  width: 40px;
}

.settings-btn-container {
  margin-top: auto;
}

.icon {
  font-family: 'Material Symbols Outlined';
  font-weight: normal;
  font-style: normal;
  font-size: 28px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-feature-settings: 'liga';
  font-feature-settings: 'liga';
  -webkit-font-smoothing: antialiased;
  vertical-align: middle;
}

/* 手機版樣式 */
@media (max-width: 768px) {
  .sidebar-left {
    display: none;
  }
}
</style>

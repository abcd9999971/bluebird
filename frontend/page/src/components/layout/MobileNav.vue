<template>
  <!-- 手機版導航 -->
  <nav 
    class="mobile-nav" 
    ref="navContainer"
    @keydown="handleKeydown"
    tabindex="0"
  >
    <!-- 手機版：主頁按鈕 -->
    <img 
      :src="projectInfo?.avatar || '/assets/images/avatars/project-avatar.jpg'" 
      :alt="projectInfo?.name_ja || 'いきづらい部'" 
      class="mobile-avatar" 
      :class="{'active': !filters.member && !filters.onlyLiked}" 
      @click="resetFilters"
    />
    <!-- 手機版：喜歡的日誌按鈕 -->
    <button 
      class="mobile-filter-btn"
      :class="{'active': filters.onlyLiked}"
      @click="toggleLikedFilter"
      :title="t('filter_liked')"
    >
      <span class="icon">favorite</span>
    </button>
    <!-- 手機版：成員列表 -->
    <img 
      v-for="key in characterOrder" 
      :key="'m-'+key" 
      :src="authors[key]?.avatar || ''" 
      :alt="authors[key]?.name_ja || key" 
      class="mobile-avatar" 
      :class="{'active': filters.member===key}" 
      @click="setMemberFilter(key)"
    />
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

// 定義 props - 從父組件接收的資料
const props = defineProps({
  filters: Object,
  authors: Object,
  characterOrder: Array,
  projectInfo: Object
});

// 定義 emits - 向父組件發送的事件
const emit = defineEmits([
  'resetFilters',
  'toggleLikedFilter',
  'setMemberFilter'
]);

// 組件引用
const navContainer = ref(null);

// 翻譯函數 - 獲取多語言文字
const t = (key) => {
  const translations = {
    'ja': { 
      filter_liked: 'いいねした日誌'
    }
  };
  return translations['ja']?.[key] || key;
};

// 事件處理函數 - 重置所有篩選條件
const resetFilters = () => emit('resetFilters');

// 事件處理函數 - 切換喜歡篩選
const toggleLikedFilter = () => emit('toggleLikedFilter');

// 事件處理函數 - 設定成員篩選
const setMemberFilter = (memberId) => emit('setMemberFilter', memberId);

// 鍵盤導航處理
const handleKeydown = (event) => {
  if (!navContainer.value) return;
  
  const scrollAmount = 100; // 每次滾動的像素數
  
  switch (event.key) {
    case 'ArrowLeft':
      event.preventDefault();
      navContainer.value.scrollBy({
        left: -scrollAmount,
        behavior: 'smooth'
      });
      break;
    case 'ArrowRight':
      event.preventDefault();
      navContainer.value.scrollBy({
        left: scrollAmount,
        behavior: 'smooth'
      });
      break;
    case 'Home':
      event.preventDefault();
      navContainer.value.scrollTo({
        left: 0,
        behavior: 'smooth'
      });
      break;
    case 'End':
      event.preventDefault();
      navContainer.value.scrollTo({
        left: navContainer.value.scrollWidth,
        behavior: 'smooth'
      });
      break;
  }
};

// 生命週期
onMounted(() => {
  // 讓導航容器可以接收鍵盤焦點
  if (navContainer.value) {
    navContainer.value.focus();
  }
});
</script>

<style scoped>
/* 使用全局樣式，移除重複定義 */

.mobile-nav::-webkit-scrollbar {
  display: none;
}

.mobile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 3px solid transparent;
  transition: var(--transition-fast);
  flex-shrink: 0;
  cursor: pointer;
  object-fit: cover;
  display: block;
}

.mobile-avatar.active {
  border-color: var(--brand-color);
  transform: scale(1.08);
}

.mobile-filter-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 3px solid transparent;
  background: transparent;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition-fast);
  flex-shrink: 0;
  cursor: pointer;
}

.mobile-filter-btn.active {
  border-color: var(--brand-color);
  color: var(--brand-color);
  transform: scale(1.08);
}

.mobile-filter-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.icon {
  font-family: 'Material Symbols Outlined';
  font-weight: normal;
  font-style: normal;
  font-size: 20px;
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

/* 手機版顯示 */
@media (max-width: 768px) {
  .mobile-nav {
    display: flex !important;
  }
}

/* 桌面版隱藏 */
@media (min-width: 769px) {
  .mobile-nav {
    display: none !important;
  }
}

/* 手機版樣式 */
@media (max-width: 768px) {
  .mobile-nav {
    position: sticky;
    top: 60px; /* 在標題下方 */
    z-index: 9;
    backdrop-filter: blur(12px);
    background-color: color-mix(in srgb, var(--bg-secondary) 90%, transparent);
  }
}
</style>

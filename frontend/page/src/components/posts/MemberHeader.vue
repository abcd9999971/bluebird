<template>
  <!-- 成員橫幅 -->
  <div v-if="filters.member || (!filters.member && !filters.onlyLiked)" class="member-header">
    <!-- 橫幅背景 -->
    <div class="member-banner" :style="currentBannerStyle"></div>
    
    <!-- 成員頭像 -->
    <img 
      v-if="filters.member" 
      :src="authors[filters.member]?.avatar_url || ''" 
      :alt="authors[filters.member]?.name_ja || filters.member" 
      class="member-avatar"
    >
    <img 
      v-else 
      :src="projectInfo?.avatar_url || '/assets/images/avatars/project-avatar.jpg'" 
      :alt="projectInfo?.name_ja || 'いきづらい部'" 
      class="member-avatar"
    >
    
    <!-- 成員資訊按鈕（右上） -->
    <div v-if="filters.member" class="member-meta-top">
      <button class="profile-btn" @click="openProfileModal(authors[filters.member])">
        {{ t('profile_button') }}
      </button>
    </div>
    
     <!-- 成員名稱和 ID 容器 -->
     <div v-if="filters.member" class="member-name-container">
       <span class="member-name">{{ authors[filters.member]?.name_ja || filters.member }}</span>
       <div class="member-id-container">
         <a 
           :href="getTwitterUrl(authors[filters.member]?.twitter_id || authors[filters.member]?.id || `@${filters.member}`)"
           target="_blank"
           rel="noopener noreferrer"
           class="member-id-link"
           @mouseenter="showTooltip = true"
           @mouseleave="showTooltip = false"
         >
           {{ authors[filters.member]?.twitter_id || authors[filters.member]?.id || `@${filters.member}` }}
         </a>
         <!-- 懸停提示框 -->
         <div 
           v-if="showTooltip" 
           class="x-tooltip"
         >
           {{ t('x_account_tooltip') }}
         </div>
       </div>
     </div>
     <div v-else-if="!filters.member" class="member-name-container">
       <span class="member-name">{{ projectInfo?.name_ja || 'いきづらい部' }}</span>
       <div class="member-id-container">
         <a 
           :href="getTwitterUrl(projectInfo?.id || '@ikizulive_staff')"
           target="_blank"
           rel="noopener noreferrer"
           class="member-id-link"
           @mouseenter="showTooltip = true"
           @mouseleave="showTooltip = false"
         >
           {{ projectInfo?.id || '@ikizulive_staff' }}
         </a>
         <!-- 懸停提示框 -->
         <div 
           v-if="showTooltip" 
           class="x-tooltip"
         >
           {{ t('x_account_tooltip') }}
         </div>
       </div>
     </div>
    
    <!-- 主頁自我介紹按鈕 -->
    <div v-if="!filters.member" class="member-meta-top">
      <button class="profile-btn" @click="openProfileModal(projectInfo)">
        {{ projectInfo?.profile_btn_text || 'L高とは' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// 定義 props - 從父組件接收的資料
const props = defineProps({
  filters: Object,
  authors: Object,
  projectInfo: Object
});

// 定義 emits - 向父組件發送的事件
const emit = defineEmits(['openProfileModal']);

// 提示框狀態
const showTooltip = ref(false);

// 翻譯函數 - 獲取多語言文字
const t = (key) => {
  const translations = {
    'ja': { 
      profile_button: '自己紹介',
      x_account_tooltip: '公式Xアカウントへ'
    }
  };
  return translations['ja']?.[key] || key;
};

// 計算當前橫幅樣式
const currentBannerStyle = computed(() => {
  const current = props.filters.member ? props.authors[props.filters.member] : props.projectInfo;
  return current?.banner_url ? { backgroundImage: `url(${current.banner_url})` } : { backgroundColor: current?.color || '#1d9bf0' };
});

// 事件處理函數 - 開啟個人資料彈窗
const openProfileModal = (author) => emit('openProfileModal', author);

// 工具函數 - 生成 Twitter/X 連結 URL
const getTwitterUrl = (twitterId) => {
  // 移除 @ 符號（如果有的話）並生成 X.com 連結
  const cleanId = twitterId.replace('@', '');
  return `https://x.com/${cleanId}`;
};
</script>

<style scoped>
.member-header {
  position: relative;
  margin-bottom: 70px;
  animation: member-fade-in 0.5s ease-out;
}

.member-banner {
  height: 230px;
  background-size: cover;
  background-position: center;
  background-color: var(--brand-color);
  width: 100%;
}

.member-avatar {
  width: 130px;
  height: 130px;
  border-radius: 50%;
  border: 4px solid var(--bg-secondary);
  position: absolute;
  top: 165px;
  left: calc(var(--spacing-unit) * 3);
  object-fit: cover;
  z-index: 10;
}

.member-meta-top {
  position: absolute;
  top: 240px;
  right: calc(var(--spacing-unit) * 3);
  display: flex;
  gap: var(--spacing-unit);
}

/* 成員名稱和 ID 容器 - 使用 Flexbox 水平排列 */
.member-name-container {
  position: absolute;
  top: 240px;
  left: 170px;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.5);
}

/* 成員名稱 - 主要標題樣式 */
.member-name {
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--text-primary);
}

/* 成員 ID 容器 */
.member-id-container {
  position: relative;
  display: inline-block;
}

/* 成員 ID 連結 - 可點擊的 Twitter/X 連結 */
.member-id-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 1rem;
  font-weight: 400;
  transition: color var(--transition-duration) ease;
}

/* 成員 ID 連結懸停效果 */
.member-id-link:hover {
  color: var(--brand-color);
  text-decoration: underline;
}

/* X 帳號提示框樣式 */
.x-tooltip {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-top: 8px;
  padding: 6px 12px;
  background-color: var(--bg-tooltip);
  color: var(--text-tooltip);
  border: 1px solid var(--border-tooltip);
  border-radius: 8px;
  font-size: 0.85rem;
  white-space: nowrap;
  z-index: 1000;
  box-shadow: var(--shadow-tooltip);
  backdrop-filter: blur(8px);
  animation: tooltip-fade-in 0.2s ease-out;
}

/* 提示框箭頭 */
.x-tooltip::after {
  content: '';
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 5px solid transparent;
  border-bottom-color: var(--bg-tooltip);
}

/* 提示框淡入動畫 */
@keyframes tooltip-fade-in {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

.profile-btn {
  background-color: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-secondary);
  font-weight: 700;
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
  border-radius: var(--radius-full);
  transition: var(--transition-fast);
  z-index: 10;
  cursor: pointer;
}

.profile-btn:active {
  animation: button-press 0.1s ease-out;
}

html[data-member-theme="true"] .profile-btn {
  border-color: var(--brand-color);
  color: var(--brand-color);
}

html[data-member-theme="true"] .profile-btn:hover {
  background-color: color-mix(in srgb, var(--brand-color) 10%, transparent);
}

.profile-btn:hover {
  background-color: var(--bg-hover);
}

/* 手機版樣式已移至全局 CSS 文件 */
</style>

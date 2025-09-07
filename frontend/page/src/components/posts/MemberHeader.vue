<template>
  <!-- 成員橫幅 -->
  <div v-if="filters.member || (!filters.member && !filters.onlyLiked)" class="member-header">
    <!-- 橫幅背景 -->
    <div class="member-banner" :style="currentBannerStyle"></div>
    
    <!-- 成員頭像 -->
    <img 
      v-if="filters.member" 
      :src="authors[filters.member]?.avatar || ''" 
      :alt="authors[filters.member]?.name_ja || filters.member" 
      class="member-avatar"
    >
    <img 
      v-else 
      :src="projectInfo?.avatar || '/assets/images/avatars/project-avatar.jpg'" 
      :alt="projectInfo?.name_ja || 'いきづらい部'" 
      class="member-avatar"
    >
    
    <!-- 成員資訊按鈕（右上） -->
    <div v-if="filters.member" class="member-meta-top">
      <button class="profile-btn" @click="openProfileModal(authors[filters.member])">
        {{ t('profile_button') }}
      </button>
    </div>
    
    <!-- 成員名稱 -->
    <div v-if="filters.member" class="member-name">{{ authors[filters.member]?.name_ja || filters.member }}</div>
    <div v-if="filters.member" class="member-id">{{ authors[filters.member]?.id || `@${filters.member}` }}</div>
    <div v-else-if="!filters.member" class="member-name">{{ projectInfo?.name_ja || 'いきづらい部' }}</div>
    <div v-else-if="!filters.member" class="member-id">{{ projectInfo?.id || '@ikizulive_staff' }}</div>
    
    <!-- 主頁自我介紹按鈕 -->
    <div v-if="!filters.member" class="member-meta-top">
      <button class="profile-btn" @click="openProfileModal(projectInfo)">
        {{ projectInfo?.profile_btn_text || 'L高とは' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

// 定義 props - 從父組件接收的資料
const props = defineProps({
  filters: Object,
  authors: Object,
  projectInfo: Object
});

// 定義 emits - 向父組件發送的事件
const emit = defineEmits(['openProfileModal']);

// 翻譯函數 - 獲取多語言文字
const t = (key) => {
  const translations = {
    'ja': { 
      profile_button: '自己紹介'
    }
  };
  return translations['ja']?.[key] || key;
};

// 計算當前橫幅樣式
const currentBannerStyle = computed(() => {
  const current = props.filters.member ? props.authors[props.filters.member] : props.projectInfo;
  return current?.banner ? { backgroundImage: `url(${current.banner})` } : { backgroundColor: current?.color || '#1d9bf0' };
});

// 事件處理函數 - 開啟個人資料彈窗
const openProfileModal = (author) => emit('openProfileModal', author);
</script>

<style scoped>
.member-header {
  position: relative;
  margin-bottom: 70px;
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

.member-name {
  font-size: 1.35rem;
  font-weight: 700;
  position: absolute;
  top: 240px;
  left: 170px;
  z-index: 10;
}

.member-id {
  color: var(--text-secondary);
  position: absolute;
  top: 270px;
  left: 170px;
  z-index: 10;
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

<template>
  <div class="filter-feature">
    <!-- 成員篩選 -->
    <div class="member-filter-section">
      <div class="filter-header">
        <h3>{{ t('member_filter') }}</h3>
        <button 
          class="clear-filter-btn"
          :disabled="!selectedMember"
          @click="clearMemberFilter"
        >
          <span class="icon">clear</span>
        </button>
      </div>
      
      <!-- 桌面版成員網格 -->
      <div v-if="!isMobile" class="member-grid">
        <button
          v-for="memberId in characterOrder"
          :key="memberId"
          class="member-filter-btn"
          :class="{ 
            'active': selectedMember === memberId,
            'has-posts': hasPosts(memberId)
          }"
          :style="{ '--member-color': authors[memberId]?.color }"
          @click="selectMember(memberId)"
        >
          <img 
            :src="getMemberAvatar(memberId)" 
            :alt="authors[memberId]?.name_ja"
            class="member-avatar"
          />
          <span class="member-name">{{ authors[memberId]?.name_ja }}</span>
        </button>
      </div>

      <!-- 手機版成員橫向滾動 -->
      <div v-else class="mobile-member-scroll">
        <button
          v-for="memberId in characterOrder"
          :key="memberId"
          class="mobile-member-btn"
          :class="{ 
            'active': selectedMember === memberId,
            'has-posts': hasPosts(memberId)
          }"
          :style="{ '--member-color': authors[memberId]?.color }"
          @click="selectMember(memberId)"
        >
          <img 
            :src="getMemberAvatar(memberId)" 
            :alt="authors[memberId]?.name_ja"
            class="mobile-avatar"
          />
        </button>
      </div>
    </div>

    <!-- 其他篩選選項 -->
    <div class="other-filters">
      <!-- 只顯示喜歡的推文 -->
      <button 
        class="filter-toggle-btn"
        :class="{ 'active': onlyLiked }"
        @click="toggleLikedFilter"
      >
        <span class="icon">favorite</span>
        <span class="label">{{ t('show_liked_only') }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { getMemberAvatar } from '../../utils/assets.js';

/**
 * 篩選功能組件
 * 統一的篩選功能，包含成員篩選和喜歡篩選
 * 支援桌面版和手機版不同布局
 */

// Props 定義
const props = defineProps({
  selectedMember: {
    type: String,
    default: null
  },
  onlyLiked: {
    type: Boolean,
    default: false
  },
  authors: {
    type: Object,
    required: true
  },
  characterOrder: {
    type: Array,
    required: true
  },
  isMobile: {
    type: Boolean,
    default: false
  },
  tweetStats: {
    type: Object,
    default: () => ({})
  }
});

// Emits 定義
const emit = defineEmits(['select-member', 'clear-member', 'toggle-liked']);

// 國際化
const { t } = useI18n();

// 計算屬性
const hasPosts = (memberId) => {
  return props.tweetStats[memberId] > 0;
};

// 方法
const selectMember = (memberId) => {
  const newSelection = props.selectedMember === memberId ? null : memberId;
  emit('select-member', newSelection);
};

const clearMemberFilter = () => {
  emit('clear-member');
};

const toggleLikedFilter = () => {
  emit('toggle-liked');
};
</script>

<style scoped>
.filter-feature {
  width: 100%;
}

/* 成員篩選區域 */
.member-filter-section {
  margin-bottom: var(--spacing-unit);
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-unit);
}

.filter-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.clear-filter-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 50%;
  transition: var(--transition-fast);
}

.clear-filter-btn:hover:not(:disabled) {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.clear-filter-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.clear-filter-btn .icon {
  font-family: 'Material Symbols Outlined';
  font-size: 18px;
  line-height: 1;
}

/* 桌面版成員網格 */
.member-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: var(--spacing-unit);
}

.member-filter-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.5);
  padding: var(--spacing-unit);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  background-color: var(--bg-primary);
  cursor: pointer;
  transition: var(--transition-fast);
  position: relative;
}

.member-filter-btn:hover {
  background-color: var(--bg-hover);
  border-color: var(--member-color);
}

.member-filter-btn.active {
  background-color: color-mix(in srgb, var(--member-color) 10%, var(--bg-primary));
  border-color: var(--member-color);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--member-color) 20%, transparent);
}

.member-filter-btn.has-posts::after {
  content: '';
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background-color: var(--member-color);
  border-radius: 50%;
}

.member-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--border-primary);
  transition: var(--transition-fast);
}

.member-filter-btn.active .member-avatar {
  border-color: var(--member-color);
}

.member-name {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-primary);
  text-align: center;
  line-height: 1.2;
}

/* 手機版成員橫向滾動 */
.mobile-member-scroll {
  display: flex;
  gap: var(--spacing-unit);
  overflow-x: auto;
  padding: 0 var(--spacing-unit);
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.mobile-member-scroll::-webkit-scrollbar {
  display: none;
}

.mobile-member-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border: 2px solid var(--border-primary);
  border-radius: 50%;
  background-color: var(--bg-primary);
  cursor: pointer;
  transition: var(--transition-fast);
  position: relative;
  flex-shrink: 0;
}

.mobile-member-btn:hover {
  border-color: var(--member-color);
  transform: scale(1.05);
}

.mobile-member-btn.active {
  border-color: var(--member-color);
  background-color: color-mix(in srgb, var(--member-color) 10%, var(--bg-primary));
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--member-color) 20%, transparent);
}

.mobile-member-btn.has-posts::after {
  content: '';
  position: absolute;
  top: 4px;
  right: 4px;
  width: 12px;
  height: 12px;
  background-color: var(--member-color);
  border-radius: 50%;
  border: 2px solid var(--bg-primary);
}

.mobile-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
}

/* 其他篩選選項 */
.other-filters {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing-unit) * 0.5);
}

.filter-toggle-btn {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.5);
  padding: calc(var(--spacing-unit) * 0.75);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition-fast);
  font-family: inherit;
  font-size: 0.9rem;
}

.filter-toggle-btn:hover {
  background-color: var(--bg-hover);
  border-color: var(--brand-color);
}

.filter-toggle-btn.active {
  background-color: color-mix(in srgb, var(--brand-color) 10%, var(--bg-primary));
  border-color: var(--brand-color);
  color: var(--brand-color);
}

.filter-toggle-btn .icon {
  font-family: 'Material Symbols Outlined';
  font-size: 18px;
  line-height: 1;
}

.filter-toggle-btn .label {
  font-weight: 500;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .member-grid {
    display: none;
  }
}

@media (min-width: 769px) {
  .mobile-member-scroll {
    display: none;
  }
}
</style>

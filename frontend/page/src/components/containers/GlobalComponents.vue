<template>
  <div class="global-components">
    <!-- 遮罩層 -->
    <div class="overlay" :class="{ show: ui.overlay }" @click="closeAllModals"></div>

    <!-- 推文詳情彈窗 -->
    <PostDetailModal 
      :ui="ui"
      @closeModal="closeAllModals"
    />

    <!-- 個人資料彈窗 -->
    <ProfileModal 
      :ui="ui"
      @closeModal="closeAllModals"
    />
      
    <!-- 手機版日期導航彈窗 -->
    <DateNavigationModal 
      :ui="ui"
      :filters="filters"
      :availableYears="availableYears"
      :availableMonths="availableMonths"
      :dateGroups="dateGroups"
      :scroller="scroller"
      @closeModal="closeAllModals"
      @setYear="setYear"
      @setMonthFilter="setMonthFilter"
      @scrollToDate="scrollToDate"
    />

    <!-- 回到頂部按鈕 -->
    <BaseToTopButton :show="ui.showTop" />

    <!-- Toast 通知 -->
    <BaseToastNotification :toast="toast" />

    <!-- 下拉刷新指示器 -->
    <BasePullRefreshIndicator
      :visible="shouldShowRefreshIndicator()"
      :pullDistance="pullRefreshState.pullDistance"
      :isRefreshing="pullRefreshState.isRefreshing"
    />

    <!-- 底部導航欄 -->
    <LayoutBottomNavigation
      :filters="filters"
      :prefs="prefs"
      @resetFilters="resetFilters"
      @focusSearch="focusSearch"
      @toggleLikedFilter="toggleLikedFilter"
      @openDateNavigationModal="openDateNavigationModal"
      @toggleTheme="toggleTheme"
    />

    <!-- 生日提醒 -->
    <BaseBirthdayReminder
      :authors="authors"
      @close="() => {}"
    />
  </div>
</template>

<script setup>
/**
 * 全域組件容器
 * 統一管理所有全域組件，如彈窗、通知、導航等
 * 簡化 App.vue 的複雜度
 */

// 組件引入
import PostDetailModal from '../modals/PostDetailModal.vue';
import ProfileModal from '../modals/ProfileModal.vue';
import DateNavigationModal from '../modals/DateNavigationModal.vue';
import BaseToTopButton from '../ui/BaseToTopButton.vue';
import BaseToastNotification from '../ui/BaseToastNotification.vue';
import BasePullRefreshIndicator from '../ui/BasePullRefreshIndicator.vue';
import LayoutBottomNavigation from '../layout/LayoutBottomNavigation.vue';
import BaseBirthdayReminder from '../ui/BaseBirthdayReminder.vue';

// Props 定義
const props = defineProps({
  ui: {
    type: Object,
    required: true
  },
  filters: {
    type: Object,
    required: true
  },
  prefs: {
    type: Object,
    required: true
  },
  authors: {
    type: Object,
    required: true
  },
  availableYears: {
    type: Array,
    required: true
  },
  availableMonths: {
    type: Array,
    required: true
  },
  dateGroups: {
    type: Array,
    required: true
  },
  scroller: {
    type: Object,
    required: true
  },
  toast: {
    type: Object,
    required: true
  },
  pullRefreshState: {
    type: Object,
    required: true
  },
  shouldShowRefreshIndicator: {
    type: Function,
    required: true
  }
});

// Emits 定義
const emit = defineEmits([
  'closeAllModals',
  'setYear',
  'setMonthFilter',
  'scrollToDate',
  'resetFilters',
  'focusSearch',
  'toggleLikedFilter',
  'openDateNavigationModal',
  'toggleTheme'
]);

// 方法
const closeAllModals = () => {
  emit('closeAllModals');
};

const setYear = (year) => {
  emit('setYear', year);
};

const setMonthFilter = (month) => {
  emit('setMonthFilter', month);
};

const scrollToDate = (tweetId) => {
  emit('scrollToDate', tweetId);
};

const resetFilters = () => {
  emit('resetFilters');
};

const focusSearch = () => {
  emit('focusSearch');
};

const toggleLikedFilter = () => {
  emit('toggleLikedFilter');
};

const openDateNavigationModal = () => {
  emit('openDateNavigationModal');
};

const toggleTheme = () => {
  emit('toggleTheme');
};
</script>

<style scoped>
.global-components {
  position: relative;
  z-index: 1;
}

/* 遮罩層樣式 */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 100;
  opacity: 0;
  visibility: hidden;
  transition: var(--transition-fast);
}

.overlay.show {
  opacity: 1;
  visibility: visible;
}
</style>

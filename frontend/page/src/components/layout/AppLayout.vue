<template>
  <div class="app-layout">
    <!-- 左側邊欄 -->
    <LayoutLeftSidebar 
      :filters="filters"
      :ui="ui"
      :prefs="prefs"
      :authors="authors"
      :characterOrder="characterOrder"
      @resetFilters="resetFilters"
      @focusSearch="focusSearch"
      @onSearchBlur="onSearchBlur"
      @toggleLikedFilter="toggleLikedFilter"
      @toggleQuotesFilter="toggleQuotesFilter"
      @setMemberFilter="setMemberFilter"
      @toggleTheme="toggleTheme"
    />

    <!-- 主要時間軸區域 -->
    <main class="timeline">
      <slot name="timeline"></slot>
    </main>

    <!-- 時間軸裝飾桿 -->
    <BaseTimelineBar 
      :dateGroups="dateGroups"
      :activeDate="scroller.activeDate"
      :brandColor="brandColor"
    />

    <!-- 右側邊欄 -->
    <LayoutRightSidebar 
      :filters="filters"
      :availableYears="availableYears"
      :availableMonths="availableMonths"
      :dateGroups="dateGroups"
      :scroller="scroller"
      @setYear="setYear"
      @setMonthFilter="setMonthFilter"
      @scrollToDate="scrollToDate"
    />
  </div>
</template>

<script setup>
/**
 * 應用程式佈局組件
 * 統一管理應用程式的主要佈局結構
 * 包含左側邊欄、主要內容區域、時間軸裝飾桿、右側邊欄
 */

// 組件引入
import LayoutLeftSidebar from './LayoutLeftSidebar.vue';
import LayoutRightSidebar from './LayoutRightSidebar.vue';
import BaseTimelineBar from '../ui/BaseTimelineBar.vue';

// Props 定義
const props = defineProps({
  filters: {
    type: Object,
    required: true
  },
  ui: {
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
  characterOrder: {
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
  brandColor: {
    type: String,
    required: true
  },
  availableYears: {
    type: Array,
    required: true
  },
  availableMonths: {
    type: Array,
    required: true
  }
});

// Emits 定義
const emit = defineEmits([
  'resetFilters',
  'focusSearch',
  'onSearchBlur',
  'toggleLikedFilter',
  'toggleQuotesFilter',
  'setMemberFilter',
  'toggleTheme',
  'setYear',
  'setMonthFilter',
  'scrollToDate'
]);

// 方法
const resetFilters = () => {
  emit('resetFilters');
};

const focusSearch = () => {
  emit('focusSearch');
};

const onSearchBlur = () => {
  emit('onSearchBlur');
};

const toggleLikedFilter = () => {
  emit('toggleLikedFilter');
};

const toggleQuotesFilter = () => {
  emit('toggleQuotesFilter');
};

const setMemberFilter = (member) => {
  emit('setMemberFilter', member);
};

const toggleTheme = () => {
  emit('toggleTheme');
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
</script>

<style scoped>
.app-layout {
  display: flex;
  width: 100%;
  max-width: var(--main-max-width);
}

.timeline {
  width: 100%;
  max-width: var(--timeline-width);
  min-width: 0;
  border-left: 1px solid var(--border-primary);
  border-right: 1px solid var(--border-primary);
  background-color: color-mix(in srgb, var(--bg-secondary) 85%, transparent);
  min-height: 100vh;
  backdrop-filter: blur(12px);
}
</style>

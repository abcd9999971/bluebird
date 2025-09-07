<template>
  <div class="app-layout">
    <!-- 左側邊欄 -->
    <LeftSidebar 
      :filters="filters"
      :ui="ui"
      :prefs="prefs"
      :authors="authors"
      :characterOrder="characterOrder"
      @resetFilters="$emit('resetFilters')"
      @focusSearch="$emit('focusSearch')"
      @onSearchBlur="$emit('onSearchBlur')"
      @toggleLikedFilter="$emit('toggleLikedFilter')"
      @setMemberFilter="$emit('setMemberFilter')"
      @toggleTheme="$emit('toggleTheme')"
    />

    <!-- 主要時間軸區域 -->
    <main class="timeline">
      <!-- 時間軸標題列 -->
      <PostsHeader 
        :ui="ui"
        :filters="filters"
        :prefs="prefs"
        :headerTitle="headerTitle"
        @focusSearch="$emit('focusSearch')"
        @toggleMobileSearch="$emit('toggleMobileSearch')"
        @openDateNavModal="$emit('openDateNavModal')"
        @onSearchBlur="$emit('onSearchBlur')"
        @toggleTheme="$emit('toggleTheme')"
      />
      
      <!-- 手機版搜尋框 -->
      <div v-if="ui.showMobileSearch" class="mobile-search-container">
        <div class="mobile-search-box">
          <input
            ref="mobileSearchInput"
            v-model="filters.search"
            type="text"
            :placeholder="t('search_placeholder')"
            class="mobile-search-input"
            @blur="$emit('onSearchBlur')"
            @keyup.enter="$emit('onSearchBlur')"
          />
          <button 
            class="mobile-search-close"
            @click="ui.showMobileSearch = false"
          >
            <span class="icon">close</span>
          </button>
        </div>
      </div>
      
      <!-- 手機版導航列 -->
      <MobileNav 
        :filters="filters"
        :authors="authors"
        :characterOrder="characterOrder"
        :projectInfo="projectInfo"
        @resetFilters="$emit('resetFilters')"
        @toggleLikedFilter="$emit('toggleLikedFilter')"
        @setMemberFilter="$emit('setMemberFilter')"
      />

      <!-- 成員橫幅區域 -->
      <MemberHeader 
        :filters="filters"
        :authors="authors"
        :projectInfo="projectInfo"
        @openProfileModal="$emit('openProfileModal')"
      />

      <!-- 推文列表 -->
      <PostList 
        :filteredTweets="filteredTweets"
        :authors="authors"
        :ui="ui"
        :searchTerm="filters.search"
        @openDetail="$emit('openDetail')"
        @toggleLike="$emit('toggleLike')"
        @shareTweet="$emit('shareTweet')"
        @handleTweetTextClick="$emit('handleTweetTextClick')"
        @filterByMember="$emit('setMemberFilter')"
      />
    </main>

    <!-- 時間軸裝飾桿 -->
    <TimelineBar 
      :dateGroups="dateGroups"
      :activeDate="scroller.activeDate"
      :brandColor="brandColor"
    />

    <!-- 右側邊欄 -->
    <RightSidebar 
      :filters="filters"
      :availableYears="availableYears"
      :availableMonths="availableMonths"
      :dateGroups="dateGroups"
      :scroller="scroller"
      @setYear="$emit('setYear', $event)"
      @setMonthFilter="$emit('setMonthFilter', $event)"
      @scrollToDate="$emit('scrollToDate', $event)"
    />
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n';
import {
  LeftSidebar,
  PostsHeader,
  MobileNav,
  MemberHeader,
  PostList,
  TimelineBar,
  RightSidebar
} from '../index.js';

// Props 定義
defineProps({
  filters: Object,
  ui: Object,
  prefs: Object,
  authors: Object,
  characterOrder: Array,
  projectInfo: Object,
  headerTitle: String,
  filteredTweets: Array,
  dateGroups: Array,
  scroller: Object,
  brandColor: String,
  availableYears: Array,
  availableMonths: Array
});

// Events 定義
defineEmits([
  'resetFilters',
  'focusSearch',
  'onSearchBlur',
  'toggleLikedFilter',
  'setMemberFilter',
  'toggleTheme',
  'toggleMobileSearch',
  'openDateNavModal',
  'openProfileModal',
  'openDetail',
  'toggleLike',
  'shareTweet',
  'handleTweetTextClick',
  'setYear',
  'setMonthFilter',
  'scrollToDate'
]);

const { t } = useI18n();
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

/* 手機版搜尋框樣式 */
.mobile-search-container {
  position: sticky;
  top: 58px;
  z-index: 9;
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  padding: var(--spacing-unit);
  backdrop-filter: blur(12px);
}

.mobile-search-box {
  display: flex;
  align-items: center;
  gap: var(--spacing-unit);
  background-color: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  padding: calc(var(--spacing-unit) * 0.5);
}

.mobile-search-input {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 1rem;
  padding: calc(var(--spacing-unit) * 0.5);
  outline: none;
}

.mobile-search-input::placeholder {
  color: var(--text-secondary);
}

.mobile-search-close {
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

.mobile-search-close:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.mobile-search-close .icon {
  font-family: 'Material Symbols Outlined';
  font-size: 20px;
  line-height: 1;
}

/* 桌面版隱藏手機版搜尋框 */
@media (min-width: 769px) {
  .mobile-search-container {
    display: none;
  }
}
</style>

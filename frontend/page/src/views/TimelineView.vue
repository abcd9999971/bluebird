<template>
  <div class="timeline-view">
    <!-- 時間軸標題列 -->
    <LayoutPostsHeader 
      :ui="ui"
      :filters="filters"
      :prefs="prefs"
      :headerTitle="headerTitle"
      v-model:viewMode="viewMode"
      @focusSearch="focusSearch"
      @toggleMobileSearch="toggleMobileSearch"
      @openDateNavigationModal="openDateNavigationModal"
      @onSearchBlur="onSearchBlur"
      @toggleTheme="toggleTheme"
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
          @blur="onSearchBlur"
          @keyup.enter="onSearchBlur"
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
    <LayoutMobileNavigation 
      :filters="filters"
      :authors="authors"
      :characterOrder="characterOrder"
      :projectInfo="projectInfo"
      @resetFilters="resetFilters"
      @toggleLikedFilter="toggleLikedFilter"
      @setMemberFilter="setMemberFilter"
    />

    <!-- 成員橫幅區域 -->
    <PostMemberHeader 
      :filters="filters"
      :authors="authors"
      :projectInfo="projectInfo"
      @openProfileModal="openProfileModal"
    />

    <!-- 推文列表與媒體網格切換 -->
    <Transition name="fade" mode="out-in">
      <div v-if="viewMode === 'list'" key="list">
        <!-- 推文列表 (List View) -->
        <PostListContainer 
          :filteredTweets="filteredTweets"
          :authors="authors"
          :ui="ui"
          :searchTerm="filters.search"
          @openDetail="openDetail"
          @toggleLike="toggleLike"
          @shareTweet="shareTweet"
          @handleTweetTextClick="handleTweetTextClick"
          @filterByMember="setMemberFilter"
          @jumpToTweet="(tweetId, authorId) => emit('jumpToTweet', tweetId, authorId)"
        />
      </div>

      <div v-else-if="viewMode === 'media'" key="media">
        <!-- 媒體網格 (Gallery View) -->
        <PostMediaGrid
          :tweets="filteredTweets"
          @openDetail="openDetail"
        />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';

// 組件引入
import LayoutPostsHeader from '../components/layout/LayoutPostsHeader.vue';
import LayoutMobileNavigation from '../components/layout/LayoutMobileNavigation.vue';
import PostMemberHeader from '../components/posts/PostMemberHeader.vue';
import PostListContainer from '../components/posts/PostListContainer.vue';
import PostMediaGrid from '../components/posts/PostMediaGrid.vue';

/**
 * 時間軸視圖組件
 * 整合所有時間軸相關的組件和功能
 * 簡化 App.vue 的複雜度
 */

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
  characterOrder: {
    type: Array,
    required: true
  },
  projectInfo: {
    type: Object,
    required: true
  },
  filteredTweets: {
    type: Array,
    required: true
  },
  headerTitle: {
    type: String,
    required: true
  }
});

// Emits 定義
const emit = defineEmits([
  'focusSearch',
  'toggleMobileSearch',
  'openDateNavigationModal',
  'onSearchBlur',
  'toggleTheme',
  'resetFilters',
  'toggleLikedFilter',
  'setMemberFilter',
  'openProfileModal',
  'openDetail',
  'toggleLike',
  'shareTweet',
  'handleTweetTextClick',
  'jumpToTweet'
]);

// 響應式變數
const mobileSearchInput = ref(null);
const viewMode = ref('list');

// 國際化
const { t } = useI18n();

// 方法
const focusSearch = () => {
  emit('focusSearch');
};

const toggleMobileSearch = () => {
  emit('toggleMobileSearch');
  if (props.ui.showMobileSearch) {
    nextTick(() => {
      mobileSearchInput.value?.focus();
    });
  }
};

const openDateNavigationModal = () => {
  emit('openDateNavigationModal');
};

const onSearchBlur = () => {
  emit('onSearchBlur');
};

const toggleTheme = () => {
  emit('toggleTheme');
};

const resetFilters = () => {
  emit('resetFilters');
};

const toggleLikedFilter = () => {
  emit('toggleLikedFilter');
};

const setMemberFilter = (member) => {
  emit('setMemberFilter', member);
};

const openProfileModal = (author) => {
  emit('openProfileModal', author);
};

const openDetail = (tweet) => {
  emit('openDetail', tweet);
};

const toggleLike = (tweet) => {
  emit('toggleLike', tweet);
};

const shareTweet = (tweet) => {
  emit('shareTweet', tweet);
};

const handleTweetTextClick = (event) => {
  emit('handleTweetTextClick', event);
};
</script>

<style scoped>
.timeline-view {
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

/* 視圖切換動畫 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>

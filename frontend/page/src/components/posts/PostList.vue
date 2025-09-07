<template>
  <!-- 推文列表 -->
  <div v-if="filteredTweets.length > 0">
    <PostItem 
      v-for="tweet in filteredTweets" 
      :key="tweet.id"
      :tweet="tweet"
      :authors="authors"
      :ui="ui"
      @openDetail="openDetail"
      @toggleLike="toggleLike"
      @shareTweet="shareTweet"
      @handleTweetTextClick="handleTweetTextClick"
    />
  </div>

  <!-- 空狀態 -->
  <div v-else class="empty-state">
    <span class="icon">sentiment_dissatisfied</span>
    <p>{{ t('empty_state_text') }}</p>
  </div>
</template>

<script setup>
import PostItem from './PostItem.vue';

// 定義 props - 從父組件接收的資料
const props = defineProps({
  filteredTweets: Array,
  authors: Object,
  ui: Object
});

// 定義 emits - 向父組件發送的事件
const emit = defineEmits([
  'openDetail',
  'toggleLike',
  'shareTweet',
  'handleTweetTextClick'
]);

// 翻譯函數 - 獲取多語言文字
const t = (key) => {
  const translations = {
    'ja': { 
      empty_state_text: '該当する日誌はありません。'
    }
  };
  return translations['ja']?.[key] || key;
};

// 事件處理函數 - 開啟推文詳情
const openDetail = (tweet) => emit('openDetail', tweet);

// 事件處理函數 - 切換喜歡狀態
const toggleLike = (tweet) => emit('toggleLike', tweet);

// 事件處理函數 - 分享推文
const shareTweet = (tweet) => emit('shareTweet', tweet);

// 事件處理函數 - 處理推文文字點擊（hashtag）
const handleTweetTextClick = (e) => emit('handleTweetTextClick', e);
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: calc(var(--spacing-unit) * 4);
  color: var(--text-secondary);
  text-align: center;
}

.empty-state .icon {
  font-family: 'Material Symbols Outlined';
  font-weight: normal;
  font-style: normal;
  font-size: 64px;
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
  margin-bottom: var(--spacing-unit);
  opacity: 0.5;
}

.empty-state p {
  font-size: 1.1rem;
  margin: 0;
}

/* 手機版樣式 */
@media (max-width: 768px) {
  .empty-state {
    padding: calc(var(--spacing-unit) * 2);
  }
  
  .empty-state .icon {
    font-size: 3rem;
  }
  
  .empty-state p {
    font-size: 1rem;
  }
}
</style>

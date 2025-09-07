<template>
  <!-- 推文列表 -->
  <div v-if="filteredTweets.length > 0" class="post-list-container">
    <!-- 直接渲染所有推文，採用保守的優化方式 -->
    <PostListItem 
      v-for="tweet in filteredTweets" 
      :key="tweet.id"
      :tweet="tweet"
      :authors="authors"
      :ui="ui"
      :searchTerm="searchTerm"
      @openDetail="openDetail"
      @toggleLike="toggleLike"
      @shareTweet="shareTweet"
      @handleTweetTextClick="handleTweetTextClick"
      @filterByMember="filterByMember"
    />
  </div>

  <!-- 空狀態 -->
  <div v-else class="empty-state">
    <span class="icon">sentiment_dissatisfied</span>
    <p>{{ t('empty_state_text') }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import PostListItem from './PostListItem.vue';

// 定義 props - 從父組件接收的資料
const props = defineProps({
  filteredTweets: Array,
  authors: Object,
  ui: Object,
  searchTerm: {
    type: String,
    default: ''
  }
});

// 定義 emits - 向父組件發送的事件
const emit = defineEmits([
  'openDetail',
  'toggleLike',
  'shareTweet',
  'handleTweetTextClick',
  'filterByMember'
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

// 事件處理函數 - 按成員篩選
const filterByMember = (authorId) => emit('filterByMember', authorId);

// 保守的優化方式：使用CSS優化和基本性能改進
// 生命週期管理
onMounted(() => {
  // 預載入關鍵圖片以提升用戶體驗
  if (props.authors) {
    const avatarUrls = Object.values(props.authors)
      .map(author => author.avatar_url)
      .filter(url => url);
    
    // 預載入頭像圖片
    avatarUrls.forEach(url => {
      const img = new Image();
      img.src = url;
    });
  }
});

onBeforeUnmount(() => {
  // 清理邏輯
});
</script>

<style scoped>
.post-list-container {
  width: 100%;
  /* 保守的優化：使用CSS硬體加速和優化渲染 */
  contain: layout style paint;
  will-change: scroll-position;
}

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

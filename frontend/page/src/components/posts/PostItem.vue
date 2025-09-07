<template>
  <!-- 推文項目 -->
  <article 
    class="tweet"
    :data-tweet-id="tweet.id"
    @click="openDetail(tweet)"
  >
    <!-- 推文頭像 -->
    <img 
      :src="tweet.avatar_url || authors[tweet.author_id]?.avatar || ''" 
      :alt="tweet.name_ja || authors[tweet.author_id]?.name_ja || tweet.author_id" 
      class="tweet-avatar"
    >
    
    <div class="tweet-body">
      <!-- 推文標題行 -->
      <div class="tweet-header">
        <span class="tweet-name">{{ tweet.name_ja || authors[tweet.author_id]?.name_ja || tweet.author_id }}@いきづらい部！</span>
        <span class="tweet-id">{{ tweet.twitter_id || authors[tweet.author_id]?.id || `@${tweet.author_id}` }}</span>
        <span class="tweet-time">{{ formatTime(tweet.created_at) }}</span>
      </div>
      
      <!-- 推文內容 -->
      <div class="tweet-text" v-html="linkify(tweet.content)" @click="handleTweetTextClick"></div>
      
      <!-- 推文操作按鈕 -->
      <div class="tweet-actions">
        <!-- 喜歡按鈕 -->
        <button 
          class="action-btn like" 
          :class="{ 'is-liked': tweet.liked, pop: tweet._pop }"
          @click.stop="toggleLike(tweet)"
        >
          <span class="icon">favorite</span>
        </button>
        <!-- 分享按鈕 -->
        <button 
          class="action-btn share" 
          :class="{ 'is-sharing': ui.isSharing === tweet.id }"
          @click.stop="shareTweet(tweet)"
        >
          <span class="icon">share</span>
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
// 定義 props - 從父組件接收的資料
const props = defineProps({
  tweet: Object,
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

// 文字連結化處理 - 將hashtag轉換為可點擊連結
const linkify = (text) => (text || '').replace(/#([\w\u3000-\u9fff\u3040-\u30ff\uff00-\uffef!-]+)/g, '<a href="#" class="hashtag">#$1</a>');

// 時間格式化 - 將時間戳轉換為易讀格式
const formatTime = (s) => new Intl.DateTimeFormat('ja-JP', { 
  year: 'numeric', 
  month: 'long', 
  day: 'numeric', 
  hour: '2-digit', 
  minute: '2-digit', 
  hour12: false 
}).format(new Date(s));

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
.tweet {
  display: flex;
  gap: calc(var(--spacing-unit) * 1.5);
  padding: calc(var(--spacing-unit) * 1.5) calc(var(--spacing-unit) * 2);
  border-bottom: 1px solid var(--border-primary);
  background-color: transparent;
  transition: var(--transition-fast);
  scroll-margin-top: 60px;
  cursor: pointer;
}

.tweet:hover {
  background-color: var(--bg-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.tweet-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  transition: var(--transition-fast);
}

.tweet-avatar:hover {
  transform: scale(1.08) rotate(2deg);
}

.tweet-body {
  flex: 1;
  min-width: 0;
}

.tweet-header {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.5);
  margin-bottom: calc(var(--spacing-unit) * 0.25);
}

.tweet-name {
  font-weight: 700;
  color: var(--text-primary);
}

.tweet-id {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.tweet-time {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-left: auto;
}

.tweet-text {
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 1.05rem;
  color: var(--text-primary);
  line-height: 1.5;
  margin-bottom: var(--spacing-unit);
}

.tweet-text :deep(.hashtag) {
  color: var(--brand-color);
  text-decoration: none;
}

.tweet-text :deep(.hashtag):hover {
  text-decoration: underline;
}

.tweet-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--spacing-unit);
}

.action-btn {
  display: flex;
  align-items: center;
  border: none;
  background: transparent;
  padding: var(--spacing-unit);
  border-radius: 50%;
  color: var(--text-secondary);
  transition: var(--transition-fast);
  cursor: pointer;
}

.action-btn:hover {
  transform: scale(1.1);
}

.action-btn.like:hover {
  background-color: color-mix(in srgb, var(--accent-pink) 10%, transparent);
  color: var(--accent-pink);
}

.action-btn.share:hover {
  background-color: color-mix(in srgb, var(--share-green) 10%, transparent);
  color: var(--share-green);
}

.action-btn.like.is-liked {
  color: var(--accent-pink);
}

.action-btn.like.is-liked .icon {
  font-variation-settings: 'FILL' 1;
}

.action-btn.is-sharing {
  animation: breath 1s ease-in-out infinite;
}

.action-btn.like.pop {
  animation: heart-pop .42s cubic-bezier(.175,.885,.32,1.275);
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

@keyframes heart-pop {
  0%{ transform: scale(1);}
  50%{ transform: scale(1.35);}
  100%{ transform: scale(1);}
}

@keyframes breath {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(0.92); }
}

/* 手機版樣式 */
@media (max-width: 768px) {
  .tweet {
    padding: calc(var(--spacing-unit) * 0.75);
  }
  
  .tweet-avatar {
    width: 40px;
    height: 40px;
  }
  
  .tweet-header {
    flex-direction: column;
    align-items: flex-start;
    gap: calc(var(--spacing-unit) * 0.25);
  }
  
  .tweet-time {
    margin-left: 0;
    order: -1;
  }
  
  .tweet-name, .tweet-id {
    font-size: 0.9rem;
  }
  
  .tweet-text {
    font-size: 0.95rem;
  }
}
</style>

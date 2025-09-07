<template>
  <!-- 推文項目 -->
  <article 
    class="tweet"
    :data-tweet-id="tweet.id"
    @click="openDetail(tweet)"
  >
    <!-- 推文頭像 -->
    <img 
      :src="tweet.avatar_url || authors[tweet.author_id]?.avatar_url || ''" 
      :alt="tweet.name_ja || authors[tweet.author_id]?.name_ja || tweet.author_id" 
      class="tweet-avatar"
    >
    
    <div class="tweet-body">
      <!-- 推文標題行 -->
      <div class="tweet-header">
        <div class="tweet-author-info">
          <span class="tweet-name">{{ tweet.name_ja || authors[tweet.author_id]?.name_ja || tweet.author_id }}@いきづらい部！</span>
          <span class="tweet-id">{{ tweet.twitter_id || authors[tweet.author_id]?.twitter_id || `@${tweet.author_id}` }}</span>
        </div>
        <div class="tweet-time-container">
          <span 
            class="tweet-time" 
            @click.stop="toggleTimeFormat"
            @mouseenter="showTooltip = true"
            @mouseleave="showTooltip = false"
          >
            {{ displayTime }}
          </span>
          <!-- 懸停提示框 -->
          <div 
            v-if="showTooltip" 
            class="time-tooltip"
          >
            {{ formatTime(tweet.created_at) }}
          </div>
        </div>
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
import { ref, computed } from 'vue';
import { formatTime, linkify } from '../../utils/formatters.js';

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

// 日期格式狀態
const showFullTime = ref(false);
const showTooltip = ref(false);

// 計算顯示的時間格式
const displayTime = computed(() => {
  if (showFullTime.value) {
    return formatTime(props.tweet.created_at);
  } else {
    // 簡短格式：只顯示月日
    const date = new Date(props.tweet.created_at);
    return new Intl.DateTimeFormat('ja-JP', { 
      month: 'long', 
      day: 'numeric'
    }).format(date);
  }
});

// 事件處理函數 - 開啟推文詳情
const openDetail = (tweet) => emit('openDetail', tweet);

// 事件處理函數 - 切換喜歡狀態
const toggleLike = (tweet) => emit('toggleLike', tweet);

// 事件處理函數 - 分享推文
const shareTweet = (tweet) => emit('shareTweet', tweet);

// 事件處理函數 - 處理推文文字點擊（hashtag）
const handleTweetTextClick = (e) => emit('handleTweetTextClick', e);

// 事件處理函數 - 切換時間格式
const toggleTimeFormat = () => {
  showFullTime.value = !showFullTime.value;
};
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
  justify-content: space-between;
  margin-bottom: calc(var(--spacing-unit) * 0.25);
  gap: calc(var(--spacing-unit) * 1);
}

.tweet-author-info {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.5);
  flex: 1;
  min-width: 0;
}

.tweet-name {
  font-weight: 700;
  color: var(--text-primary);
}

.tweet-id {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.tweet-time-container {
  position: relative;
  display: inline-block;
}

.tweet-time {
  color: var(--text-secondary);
  font-size: 0.9rem;
  cursor: pointer;
  transition: var(--transition-fast);
  white-space: nowrap;
  flex-shrink: 0;
}

.tweet-time:hover {
  color: var(--text-primary);
  text-decoration: underline;
}

/* 懸停提示框樣式 */
.time-tooltip {
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
.time-tooltip::after {
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
  font-feature-settings: 'liga';
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
    flex-direction: row;
    align-items: center;
    gap: calc(var(--spacing-unit) * 0.5);
    flex-wrap: nowrap;
  }
  
  .tweet-author-info {
    flex-direction: row;
    align-items: center;
    gap: calc(var(--spacing-unit) * 0.25);
    flex: 1;
    min-width: 0;
  }
  
  .tweet-name, .tweet-id {
    font-size: 0.85rem;
    white-space: nowrap;
  }
  
  .tweet-id {
    flex-shrink: 0;
  }
  
  .tweet-time {
    font-size: 0.8rem;
    flex-shrink: 0;
  }
  
  .tweet-text {
    font-size: 0.95rem;
  }
}
</style>

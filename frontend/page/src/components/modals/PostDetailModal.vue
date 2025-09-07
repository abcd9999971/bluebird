<template>
  <!-- 推文詳情彈窗 -->
  <div v-if="ui.detail" class="modal" :class="{ show: ui.detail }">
    <div class="modal-header">
      <h3>{{ t('tweet_detail_header') }}</h3>
      <button class="modal-close-btn" @click="closeModal">&times;</button>
    </div>
    <div class="modal-content">
      <article v-if="ui.detailTweet" class="tweet">
        <!-- 推文頭像 -->
        <img 
          :src="ui.detailTweet.avatar_url" 
          :alt="ui.detailTweet.name_ja" 
          class="tweet-avatar"
        >
        <div class="tweet-body">
          <!-- 推文標題行 -->
          <div class="tweet-header">
            <span class="tweet-name">{{ ui.detailTweet.name_ja }}@いきづらい部！</span>
            <span class="tweet-id">{{ ui.detailTweet.twitter_id }}</span>
            <span class="tweet-time">{{ formatTime(ui.detailTweet.created_at) }}</span>
          </div>
          <!-- 推文內容 -->
          <div class="tweet-text" v-html="linkify(ui.detailTweet.content)"></div>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
// 定義 props - 從父組件接收的資料
const props = defineProps({
  ui: Object
});

// 定義 emits - 向父組件發送的事件
const emit = defineEmits(['closeModal']);

// 翻譯函數 - 獲取多語言文字
const t = (key) => {
  const translations = {
    'ja': { 
      tweet_detail_header: '日誌詳細'
    }
  };
  return translations['ja']?.[key] || key;
};

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

// 事件處理函數 - 關閉彈窗
const closeModal = () => emit('closeModal');
</script>

<style scoped>
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--border-radius);
  max-width: 600px;
  width: 90vw;
  max-height: 80vh;
  overflow: hidden;
  z-index: 1001;
  opacity: 0;
  transition: opacity var(--transition-duration) ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal.show {
  opacity: 1;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-unit);
  border-bottom: 1px solid var(--border-primary);
  background-color: var(--bg-secondary);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
}

.modal-close-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  background-color: var(--bg-hover);
  color: var(--text-primary);
  cursor: pointer;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color var(--transition-duration) ease;
}

.modal-close-btn:hover {
  background-color: color-mix(in srgb, var(--text-primary) 10%, transparent);
}

.modal-content {
  padding: var(--spacing-unit);
  overflow-y: auto;
  max-height: calc(80vh - 80px);
}

.tweet {
  display: flex;
  gap: calc(var(--spacing-unit) * 0.75);
}

.tweet-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.tweet-body {
  flex: 1;
  min-width: 0;
}

.tweet-header {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.5);
  margin-bottom: calc(var(--spacing-unit) * 0.5);
  flex-wrap: wrap;
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
  color: var(--text-primary);
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 1.1rem;
}

.tweet-text :deep(.hashtag) {
  color: var(--brand-color);
  text-decoration: none;
}

.tweet-text :deep(.hashtag):hover {
  text-decoration: underline;
}

/* 手機版樣式 */
@media (max-width: 768px) {
  .modal {
    width: 95vw;
    max-height: 90vh;
  }
  
  .modal-header {
    padding: calc(var(--spacing-unit) * 0.75);
  }
  
  .modal-header h3 {
    font-size: 1.1rem;
  }
  
  .modal-content {
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
  
  .tweet-text {
    font-size: 1rem;
  }
}
</style>

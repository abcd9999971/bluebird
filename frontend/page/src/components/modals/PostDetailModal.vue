<template>
  <!-- 推文詳情彈窗 -->
  <Transition name="modal">
    <div v-if="ui.detail" class="modal-overlay" @click.self="closeModal">
      <div class="modal show">
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
                <div class="tweet-author-info">
                  <span 
                    class="tweet-name clickable" 
                    @click.stop="filterByMember(ui.detailTweet.author_id)"
                  >
                    {{ displayName }}
                  </span>
                  <span 
                    class="tweet-id clickable" 
                    @click.stop="filterByMember(ui.detailTweet.author_id)"
                  >
                    {{ ui.detailTweet.twitter_id }}
                  </span>
                </div>
                <div class="tweet-time-container">
                  <span 
                    class="tweet-time" 
                    @click.stop="toggleTimeFormat"
                  >
                    {{ displayTime }}
                  </span>
                </div>
              </div>
              <!-- 推文內容 -->
              <div class="tweet-text" v-html="linkify(ui.detailTweet.content)"></div>
              
              <!-- 推文媒體（如果有圖片） -->
              <div v-if="ui.detailTweet.image_url || ui.detailTweet.media_urls" class="tweet-media">
                <img 
                  :src="ui.detailTweet.image_url || ui.detailTweet.media_urls" 
                  :alt="'推文圖片'"
                  class="tweet-image"
                />
                <div v-if="ui.detailTweet.media_type" class="media-badge">
                  <span class="icon">{{ ui.detailTweet.media_type === 'photo' ? 'image' : 'play_circle' }}</span>
                  <span>{{ ui.detailTweet.media_type }}</span>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed } from 'vue';

// 定義 props - 從父組件接收的資料
const props = defineProps({
  ui: Object,
  filters: Object,
  authors: Object
});

// 定義 emits - 向父組件發送的事件
const emit = defineEmits(['closeModal', 'setMemberFilter', 'filterByMember']);

// 日期格式狀態
const showFullTime = ref(false);

// 檢查是否包含特定 hashtag
const hasProjectTag = computed(() => {
  return props.ui.detailTweet?.content && props.ui.detailTweet.content.includes('#いきづらい部');
});

// 檢查作者是否為成員
const isMember = computed(() => {
  if (!props.ui.detailTweet?.author_id || !props.authors) return false;
  return !!props.authors[props.ui.detailTweet.author_id];
});

// 顯示名稱：只有成員且包含 hashtag 時才顯示後綴
const displayName = computed(() => {
  const baseName = props.ui.detailTweet?.name_ja || '';
  if (isMember.value && hasProjectTag.value) {
    return `${baseName}@いきづらい部！`;
  }
  return baseName;
});

// 計算顯示的時間格式
const displayTime = computed(() => {
  if (showFullTime.value) {
    return formatTime(props.ui.detailTweet.created_at);
  } else {
    // 簡短格式：只顯示月日
    const date = new Date(props.ui.detailTweet.created_at);
    return new Intl.DateTimeFormat('ja-JP', { 
      month: 'long', 
      day: 'numeric'
    }).format(date);
  }
});

// 翻譯函數 - 獲取多語言文字
const t = (key) => {
  const translations = {
    'ja': { 
      tweet_detail_header: '日誌詳細',
      member_filter_tooltip: 'このメンバーの日誌を表示'
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

// 事件處理函數 - 切換時間格式
const toggleTimeFormat = () => {
  showFullTime.value = !showFullTime.value;
};

// 事件處理函數 - 按成員篩選
const filterByMember = (authorId) => emit('filterByMember', authorId);

// 事件處理函數 - 處理 ID 點擊
const handleIdClick = (tweet) => {
  // 如果當前不是在該成員的頁面，則啟用該成員的篩選器
  if (props.filters.member !== tweet.author_id) {
    emit('setMemberFilter', tweet.author_id);
  }
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: var(--bg-secondary);
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
  backdrop-filter: blur(12px);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  width: min(92vw, 600px);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-xl);
  overflow: hidden;
}

/* Modal Transition */
.modal-enter-active, .modal-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.modal-enter-active .modal, .modal-leave-active .modal {
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
}

.modal-enter-from .modal, .modal-leave-to .modal {
  transform: translateY(20px) scale(0.98);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-unit);
  border-bottom: 1px solid var(--border-primary);
  background-color: var(--bg-tertiary);
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
  flex-shrink: 0;
  transition: var(--transition-fast);
  object-fit: cover;
  object-position: center;
  /* 改善圖片縮放品質 */
  image-rendering: auto;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  transform: translateZ(0);
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
  position: relative;
}

.tweet-name {
  font-weight: 700;
  color: var(--text-primary);
}

.tweet-name.clickable {
  cursor: pointer;
  transition: var(--transition-fast);
}

.tweet-name.clickable:hover {
  color: var(--brand-color);
  text-decoration: underline;
}

.tweet-id {
  color: var(--text-secondary);
  font-size: 0.9rem;
  cursor: pointer;
  transition: var(--transition-fast);
}

.tweet-id.clickable {
  cursor: pointer;
  transition: var(--transition-fast);
}

.tweet-id.clickable:hover {
  color: var(--brand-color);
  text-decoration: underline;
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

/* 推文媒體樣式 */
.tweet-media {
  position: relative;
  margin-top: calc(var(--spacing-unit) * 1.5);
  border-radius: var(--radius-md);
  overflow: hidden;
  max-width: 100%;
}

.tweet-image {
  width: 100%;
  height: auto;
  max-height: 600px;
  object-fit: contain;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-primary);
}

.media-badge {
  position: absolute;
  top: calc(var(--spacing-unit) * 0.5);
  right: calc(var(--spacing-unit) * 0.5);
  background-color: color-mix(in srgb, var(--bg-secondary) 90%, transparent);
  backdrop-filter: blur(8px);
  padding: calc(var(--spacing-unit) * 0.5) calc(var(--spacing-unit) * 0.75);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.25);
  font-size: 0.85rem;
  color: var(--text-primary);
}

.media-badge .icon {
  font-family: 'Material Symbols Outlined';
  font-size: 20px;
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

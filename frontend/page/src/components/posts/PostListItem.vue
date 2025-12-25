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
      @error="(e) => e.target.src = authors[tweet.author_id]?.avatar_url || ''"
    />
    
    <div class="tweet-body">
      <!-- 推文標題行 -->
      <div class="tweet-header">
        <div class="tweet-author-info">
          <span 
            class="tweet-name clickable" 
            @click.stop="filterByMember(tweet.author_id)"
            :style="authorNameStyle"
          >
            {{ authorDisplayName }}
          </span>
          <span 
            class="tweet-id clickable" 
            @click.stop="filterByMember(tweet.author_id)"
          >
            {{ tweet.twitter_id || authors[tweet.author_id]?.twitter_id || `@${tweet.author_id}` }}
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
      <div class="tweet-text" v-html="linkify(processedContent, searchTerm)" @click.stop="handleTweetTextClick"></div>
      
      <!-- 引用推文區域 (卡片內包卡片) -->
      <div 
        v-if="tweet.quote_id" 
        class="quote-card" 
        @click.stop.prevent="handleQuoteClick"
      >
        <div class="quote-card-header">
          <div class="quote-card-author-left">
            <img 
              v-if="quoteAvatar"
              :src="quoteAvatar" 
              class="quote-card-avatar"
              @error="(e) => e.target.style.display = 'none'"
            />
            <div class="quote-card-info">
              <span class="quote-card-name" :style="quoteAuthorStyle">{{ quoteAuthorName }}</span>
              <span class="quote-card-id">@{{ tweet.quote_author_id }}</span>
            </div>
          </div>
          <!-- 原始推文按鈕 (僅限成員) -->
          <button 
            v-if="isQuoteAuthorMember" 
            class="jump-back-btn" 
            title="跳轉至原始推文"
            @click.stop.prevent="handleQuoteClick"
          >
            <span class="icon">arrow_outward</span>
            <span class="text">原始推文</span>
          </button>
        </div>
        <div class="quote-card-text" v-html="linkify(tweet.quote_text, searchTerm)"></div>
        
        <!-- 引用推文媒體 (圖片) -->
        <div v-if="tweet.quote_image_url" class="quote-card-media">
          <img :src="tweet.quote_image_url" class="quote-card-image" loading="lazy" />
        </div>
      </div>
      
      <!-- 推文媒體（如果有圖片，且不與引用推文圖片重複） -->
      <div v-if="shouldShowMainMedia && (tweet.image_url || tweet.media_urls)" class="tweet-media" @click.stop>
        <img 
          :src="tweet.image_url || tweet.media_urls" 
          :alt="'推文圖片'"
          class="tweet-image"
          loading="lazy"
          @click.stop="openMediaPreview"
          @error="(e) => e.target.closest('.tweet-media').style.display = 'none'"
        />
        <div v-if="tweet.media_type" class="media-badge">
          <span class="icon">{{ tweet.media_type === 'photo' ? 'image' : 'play_circle' }}</span>
        </div>
      </div>
      
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

        <!-- 被引用列表 (雙向關聯按鈕 - PREMIUM CENTERED PILL) -->
        <div v-if="tweet.quoted_by && tweet.quoted_by.length > 0" class="quoted-by-pill-container">
          <div class="quoted-by-pill">
            <span class="icon">format_quote</span>
            <span class="count">{{ tweet.quoted_by.length }} 引用</span>
            <div class="quoter-avatars-list">
              <img 
                v-for="(quoter, idx) in tweet.quoted_by" 
                :key="idx"
                :src="authors[quoter.author_id]?.avatar_url" 
                class="premium-quoter-avatar clickable"
                :title="authors[quoter.author_id]?.name_ja || quoter.author_id"
                @click.stop="emit('jumpToTweet', quoter.tweet_id, quoter.author_id)"
                @error="(e) => e.target.style.display = 'none'"
              />
            </div>
          </div>
        </div>

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
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { formatTime, linkify } from '../../utils/formatters.js';

// 定義 props - 從父組件接收的資料
const props = defineProps({
  tweet: Object,
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
  'handleTweetTextClick',
  'copyLink',
  'filterByMember',
  'jumpToTweet'
]);

// 日期格式狀態
const showFullTime = ref(false);



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

// 事件處理函數 - 按成員篩選
const filterByMember = (authorId) => emit('filterByMember', authorId);

// 翻譯函數
const t = (key) => {
  const translations = {
    'ja': {
      member_filter_tooltip: 'このメンバーの日誌を表示'
    }
  };
  return translations['ja']?.[key] || key;
};

// 事件處理函數 - 切換時間格式
const toggleTimeFormat = () => {
  showFullTime.value = !showFullTime.value;
};

// 檢查是否包含特定 hashtag
const hasProjectTag = computed(() => {
  return props.tweet.content && props.tweet.content.includes('#いきづらい部');
});

// 處理後的推文內容：移除特定 hashtag
const processedContent = computed(() => {
  if (!props.tweet.content) return '';
  // 移除 #いきづらい部，並清理可能留下的多餘空白
  return props.tweet.content.replace(/#いきづらい部\s*/g, '');
});

// 推文樣式：移除之前的卡片染色邏輯
// const tweetStyle = computed(...) -> Removed based on feedback

// 作者顯示名稱：根據是否有 hashtag 決定是否顯示 @いきづらい部！
const authorDisplayName = computed(() => {
  const baseName = props.tweet.name_ja || props.authors[props.tweet.author_id]?.name_ja || props.tweet.author_id;
  if (hasProjectTag.value) {
    return `${baseName}@いきづらい部！`;
  } else {
    return baseName;
  }
});

// 作者名稱樣式：如果有 hashtag，使用成員印象色
const authorNameStyle = computed(() => {
  if (hasProjectTag.value) {
    const authorColor = props.authors[props.tweet.author_id]?.color;
    if (authorColor) {
      return { color: authorColor };
    }
  }
  return {};
});

// 事件處理函數 - 開啟媒體預覽（開啟詳情模態框）
const openMediaPreview = () => {
  openDetail(props.tweet);
};

// 預設頭貼 (使用 Twitter 預設)
const defaultAvatar = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png';

// 檢查引用作者是否為成員
const isQuoteAuthorMember = computed(() => {
  return findMember(props.tweet.quote_author_id) !== null;
});

// 處理引用推文點擊
const handleQuoteClick = () => {
  if (!props.tweet.quote_id) return;
  
  // 1. 強效成員檢測
  const member = findMember(props.tweet.quote_author_id);

  // 如果找到成員，執行跳轉 (最高優先級)
  if (member) {
    console.log(`[JumpBack] Member detected: ${member.author_id} for quote ${props.tweet.quote_id}`);
    emit('jumpToTweet', props.tweet.quote_id, member.author_id);
    return;
  }
  
  // 2. 如果不是成員，顯示「詳情推文卡片」
  console.log(`[JumpBack] Non-member quote detected. Opening stub card for ${props.tweet.quote_author_id}`);
  const stubTweet = {
    id: props.tweet.quote_id,
    author_id: props.tweet.quote_author_id,
    name_ja: quoteAuthorName.value,
    content: props.tweet.quote_text,
    image_url: props.tweet.quote_image_url,
    created_at: props.tweet.created_at, 
    type: 'Tweet',
    _isQuoteStub: true,
    avatar_url: quoteAvatar.value,
    twitter_id: `@${props.tweet.quote_author_id}`,
    liked: false
  };
  emit('openDetail', stubTweet);
};

// 檢查是否應該顯示主推文媒體 (如果與引用推文媒體相同則隱藏，避免重複)
const shouldShowMainMedia = computed(() => {
  if (props.tweet.quote_id && props.tweet.quote_image_url && props.tweet.image_url) {
    return props.tweet.image_url !== props.tweet.quote_image_url;
  }
  return true;
});

// 輔助函數：查找成員 (不分大小寫)
const findMember = (authorId) => {
  if (!authorId || !props.authors) return null;
  const targetId = authorId.trim().toLowerCase();
  
  // 優先直接匹配 ID
  if (props.authors[authorId]) return props.authors[authorId];
  
  // 其次模糊匹配
  return Object.values(props.authors).find(m => {
    if (!m) return false;
    const mid = m.author_id?.toLowerCase();
    const mtid = m.twitter_id?.replace('@', '').toLowerCase();
    return mid === targetId || mtid === targetId;
  });
};

// 引用推文的頭像邏輯
const quoteAvatar = computed(() => {
  if (!props.tweet.quote_id) return '';
  const member = findMember(props.tweet.quote_author_id);
  // 優先使用成員頭像，否則使用 tweet.quote_avatar（已經移除 _mini）
  return member ? member.avatar_url : props.tweet.quote_avatar;
});

// 引用推文的作者顯示名稱
const quoteAuthorName = computed(() => {
  const member = findMember(props.tweet.quote_author_id);
  return member ? member.name_ja : props.tweet.quote_author_name;
});

// 引用推文的作者樣式
const quoteAuthorStyle = computed(() => {
  const member = findMember(props.tweet.quote_author_id);
  return member ? { color: member.color } : {};
});



// 生命週期管理
onMounted(() => {
  // 組件掛載完成
});

onBeforeUnmount(() => {
  // 組件卸載清理
});
</script>

<style scoped>
.tweet {
  display: flex;
  gap: calc(var(--spacing-unit) * 1.5);
  padding: calc(var(--spacing-unit) * 2);
  margin-bottom: var(--spacing-unit);     /* Card separation */
  margin-inline: var(--spacing-unit);     /* Side spacing */
  border: 1px solid var(--border-primary); /* Full border */
  border-radius: var(--radius-md);        /* Rounded corners */
  background-color: var(--bg-surface);    /* Explicit background */
  transition: var(--transition-fast);
  scroll-margin-top: 80px;
  cursor: pointer;
  animation: tweet-slide-in 0.4s ease-out;
  /* Optimization */
  transform: translateZ(0);
  backface-visibility: hidden;
  box-shadow: var(--shadow-1);
}

.tweet:hover {
  background-color: var(--bg-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-2);
  border-color: color-mix(in srgb, var(--brand-color) 30%, var(--border-primary));
}

.tweet.tweet-focused {
  background-color: color-mix(in srgb, var(--brand-color) 5%, var(--bg-surface));
  border: 2px solid var(--brand-color);
  transform: scale(1.02);
  box-shadow: var(--shadow-3);
  z-index: 5;
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

.tweet-avatar:hover {
  transform: translateZ(0) scale(1.08) rotate(2deg);
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

.tweet-text :deep(.search-highlight) {
  background-color: color-mix(in srgb, var(--brand-color) 30%, transparent);
  color: var(--text-primary);
  padding: 1px 2px;
  border-radius: 2px;
  font-weight: 600;
}

/* 引用推文樣式 */
.quote-container {
  margin-top: calc(var(--spacing-unit) * 0.5);
  margin-bottom: var(--spacing-unit);
  border: 1px solid var(--border-secondary);
  border-radius: var(--radius-sm);
  padding: var(--spacing-unit);
  cursor: pointer;
  transition: var(--transition-fast);
  background-color: transparent;
}

.quote-container:hover {
  background-color: var(--bg-hover);
  border-color: var(--border-outline);
}

.quote-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.quote-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  flex-shrink: 0;
}

.quote-media {
  margin-top: calc(var(--spacing-unit) * 0.5);
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 1px solid var(--border-secondary);
}

.quote-image {
  width: 100%;
  display: block;
  object-fit: cover;
  max-height: 200px;
}

.quote-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  object-fit: cover;
}

.quote-info {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.5);
  font-size: 0.9rem;
  overflow: hidden;
}

.quote-name {
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
}

.quote-id {
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.quote-text {
  font-size: 0.95rem;
  color: var(--text-primary);
  white-space: pre-wrap;
  word-break: break-word;
}

/* 推文媒體樣式 */
.tweet-media {
  position: relative;
  margin-top: var(--spacing-unit);
  margin-bottom: var(--spacing-unit);
  border-radius: var(--radius-md);
  overflow: hidden;
  max-width: 100%;
}

.tweet-image {
  width: 100%;
  height: auto;
  max-height: 500px;
  object-fit: cover;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-primary);
  cursor: zoom-in;
  transition: var(--transition-fast);
}

.tweet-image:hover {
  opacity: 0.95;
  transform: scale(1.01);
}

.media-badge {
  position: absolute;
  top: calc(var(--spacing-unit) * 0.5);
  right: calc(var(--spacing-unit) * 0.5);
  background-color: color-mix(in srgb, var(--bg-secondary) 90%, transparent);
  backdrop-filter: blur(8px);
  padding: calc(var(--spacing-unit) * 0.5);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.25);
  font-size: 0.85rem;
  color: var(--text-primary);
  pointer-events: none;
}

.media-badge .icon {
  font-family: 'Material Symbols Outlined';
  font-size: 18px;
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

.action-btn:active {
  animation: button-press 0.1s ease-out;
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

/* 引用推文卡片樣式 (卡片內包卡片) */
.quote-card {
  margin-top: calc(var(--spacing-unit) * 1);
  margin-bottom: var(--spacing-unit);
  border: 1px solid var(--border-secondary);
  border-radius: 12px;
  padding: var(--spacing-unit);
  background-color: var(--bg-secondary);
  transition: var(--transition-fast);
  overflow: hidden;
}

.quote-card:hover {
  background-color: var(--bg-hover);
  border-color: var(--brand-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-2);
}

.quote-card:active {
  transform: scale(0.98);
  background-color: color-mix(in srgb, var(--brand-color) 5%, var(--bg-hover));
}

.quote-card-header {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 1);
  margin-bottom: calc(var(--spacing-unit) * 0.75);
  justify-content: space-between;
}

.quote-card-author-left {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  width: auto;
}

.jump-back-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background-color: var(--brand-color);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 4px 10px;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.jump-back-btn:hover {
  filter: brightness(1.1);
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.jump-back-btn .icon {
  font-size: 14px;
}

.quote-card-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  object-fit: cover;
}

.quote-card-info {
  display: flex;
  align-items: center;
  gap: 4px;
}

.quote-card-name {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--text-primary);
}

.quote-card-id {
  color: var(--text-secondary);
  font-size: 0.8rem;
}

.quote-card-text {
  font-size: 0.95rem;
  color: var(--text-primary);
  line-height: 1.4;
  margin-bottom: calc(var(--spacing-unit) * 0.25);
}

.quote-card-media {
  margin-top: calc(var(--spacing-unit) * 0.5);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border-secondary);
}

.quote-card-image {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
}

/* 被引用列表 PILL 樣式 (PREMIUM FLOATING) */
.quoted-by-pill-container {
  display: flex;
  justify-content: center;
  flex: 1;
  margin: 0 16px;
  perspective: 1000px;
}

.quoted-by-pill {
  display: flex;
  align-items: center;
  gap: 12px;
  background-color: color-mix(in srgb, var(--bg-secondary) 80%, transparent);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-secondary);
  border-radius: 24px;
  padding: 6px 18px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  cursor: default;
  position: relative;
  z-index: 1;
}

.quoted-by-pill:hover {
  border-color: var(--brand-color);
  background-color: color-mix(in srgb, var(--brand-color) 6%, var(--bg-secondary));
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px) translateZ(10px);
}

.quoted-by-pill .icon {
  color: var(--brand-color);
  font-size: 20px;
  filter: drop-shadow(0 0 5px color-mix(in srgb, var(--brand-color) 30%, transparent));
}

.quoted-by-pill .count {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
  letter-spacing: 0.5px;
}

.quoter-avatars-list {
  display: flex;
  align-items: center;
  border-left: 1px solid var(--border-secondary);
  padding-left: 12px;
  margin-left: 8px;
  gap: 2px;
}

.premium-quoter-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid var(--bg-primary);
  margin-left: -14px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  object-fit: cover;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  position: relative;
}

.premium-quoter-avatar:hover {
  transform: scale(1.25) translateY(-4px);
  z-index: 10;
  border-color: var(--brand-color);
  box-shadow: 0 0 15px color-mix(in srgb, var(--brand-color) 40%, transparent);
}

.premium-quoter-avatar:first-child {
  margin-left: 0;
}

/* 跳轉高亮動畫: 強效版 */
@keyframes jump-highlight-pulse {
  0% { 
    box-shadow: 0 0 0 0 rgba(var(--brand-color-rgb), 0.5); 
    border-color: var(--brand-color);
    background-color: color-mix(in srgb, var(--brand-color) 15%, var(--bg-surface));
  }
  40% {
    box-shadow: 0 0 0 20px rgba(var(--brand-color-rgb), 0);
  }
  100% { 
    box-shadow: 0 0 0 0 rgba(var(--brand-color-rgb), 0);
    border-color: var(--border-primary);
    background-color: var(--bg-surface);
  }
}

:deep(.jump-highlight) {
  animation: jump-highlight-pulse 2.5s cubic-bezier(0.2, 0, 0.2, 1);
  border-width: 2px !important;
  z-index: 100;
  position: relative;
}

</style>

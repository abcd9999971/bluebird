<template>
  <div class="post-detail-view">
    <!-- 返回按鈕 -->
    <div class="back-button" @click="goBack">
      <span class="material-symbols-outlined">arrow_back</span>
      <span>{{ t('back_to_timeline') }}</span>
    </div>

    <!-- 推文詳情內容 -->
    <div v-if="post" class="post-detail-content">
      <!-- 推文作者資訊 -->
      <div class="post-author">
        <img 
          :src="getMemberAvatar(post.author_id)" 
          :alt="post.author_name"
          class="author-avatar"
        />
        <div class="author-info">
          <h3 class="author-name">{{ post.author_name }}</h3>
          <p class="author-id">@{{ post.author_id }}</p>
        </div>
      </div>

      <!-- 推文內容 -->
      <div class="post-content">
        <p class="post-text">{{ post.text }}</p>
        <p class="post-date">{{ formatDate(post.created_at) }}</p>
      </div>

      <!-- 推文互動 -->
      <div class="post-actions">
        <button 
          class="action-button like-button"
          :class="{ liked: post.liked }"
          @click="toggleLike"
        >
          <span class="material-symbols-outlined">
            {{ post.liked ? 'favorite' : 'favorite_border' }}
          </span>
          <span>{{ post.likes || 0 }}</span>
        </button>

        <button 
          class="action-button share-button"
          @click="sharePost"
        >
          <span class="material-symbols-outlined">share</span>
          <span>{{ t('share') }}</span>
        </button>
      </div>
    </div>

    <!-- 載入狀態 -->
    <div v-else-if="loading" class="loading-state">
      <Loader />
    </div>

    <!-- 錯誤狀態 -->
    <div v-else class="error-state">
      <p>{{ t('post_not_found') }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApi } from '../composables/useApi.js';
import { getMemberAvatar, formatDate } from '../utils/assets.js';
import { t } from '../i18n.js';
import Loader from '../components/ui/Loader.vue';

// 路由
const route = useRoute();
const router = useRouter();

// API
const { posts, loading, likePost, fetchPosts } = useApi();

// 計算屬性
const postId = computed(() => route.params.id);
const post = computed(() => {
  if (!posts.value) return null;
  return posts.value.find(p => p.id === postId.value);
});

// 方法
const goBack = () => {
  router.go(-1);
};

const toggleLike = () => {
  if (post.value) {
    likePost(post.value.id);
  }
};

const sharePost = () => {
  if (post.value) {
    sharePost(post.value.id);
  }
};

// 生命週期
onMounted(async () => {
  if (!posts.value) {
    await fetchPosts();
  }
});
</script>

<style scoped>
.post-detail-view {
  max-width: 600px;
  margin: 0 auto;
  padding: var(--spacing-lg);
  background: var(--bg-primary);
  min-height: 100vh;
}

.back-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: var(--transition-standard);
  color: var(--text-secondary);
}

.back-button:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.post-detail-content {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-2);
}

.post-author {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.author-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--border-color);
}

.author-info {
  flex: 1;
}

.author-name {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
}

.author-id {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.post-content {
  margin-bottom: var(--spacing-lg);
}

.post-text {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-md) 0;
  white-space: pre-wrap;
}

.post-date {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin: 0;
}

.post-actions {
  display: flex;
  gap: var(--spacing-lg);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.action-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-standard);
  font-size: 0.9rem;
}

.action-button:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.like-button.liked {
  color: var(--error-color);
}

.like-button.liked:hover {
  background: color-mix(in srgb, var(--error-color) 10%, transparent);
}

.loading-state,
.error-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .post-detail-view {
    padding: var(--spacing-md);
  }
  
  .post-detail-content {
    padding: var(--spacing-md);
  }
  
  .author-avatar {
    width: 50px;
    height: 50px;
  }
  
  .post-text {
    font-size: 1rem;
  }
}
</style>

<template>
  <div class="timeline-view">
    <!-- 成員橫幅 - 當選擇特定成員時顯示 -->
    <MemberHeader 
      v-if="filters.member"
      :member="selectedMember"
      :ui="ui"
      @openProfile="openProfile"
    />

    <!-- 推文列表容器 -->
    <PostList 
      :posts="filteredPosts"
      :ui="ui"
      :filters="filters"
      :loading="loading"
      @filterByMember="setMemberFilter"
      @openPostDetail="openPostDetail"
    />

    <!-- 推文詳情彈窗 -->
    <PostDetailModal 
      v-if="ui.showPostDetail"
      :ui="ui"
      :filters="filters"
      @close="closePostDetail"
      @filterByMember="setMemberFilter"
    />

    <!-- 個人資料彈窗 -->
    <ProfileModal 
      v-if="ui.showProfile"
      :member="selectedMember"
      :ui="ui"
      @close="closeProfile"
    />

    <!-- 生日提醒 -->
    <BirthdayReminder 
      v-if="ui.showBirthdayReminder"
      :member="birthdayMember"
      @close="closeBirthdayReminder"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount } from 'vue';
import { useAppState } from '../composables/useAppState.js';
import { useApi } from '../composables/useApi.js';
import { useImageLoader } from '../composables/useImageLoader.js';
import { useKeyboardShortcuts } from '../composables/useKeyboardShortcuts.js';
import { useSwipeGestures } from '../composables/useSwipeGestures.js';
import { usePullRefresh } from '../composables/usePullRefresh.js';

// 組件導入
import MemberHeader from '../components/posts/MemberHeader.vue';
import PostList from '../components/posts/PostList.vue';
import PostDetailModal from '../components/modals/PostDetailModal.vue';
import ProfileModal from '../components/modals/ProfileModal.vue';
import BirthdayReminder from '../components/ui/BirthdayReminder.vue';

// 使用組合式函數
const { 
  ui, 
  filters, 
  prefs, 
  authors, 
  characterOrder,
  resetFilters,
  setMemberFilter,
  toggleLikedFilter,
  toggleTheme,
  openPostDetail,
  closePostDetail,
  openProfile,
  closeProfile,
  closeBirthdayReminder
} = useAppState();

const { 
  posts, 
  loading, 
  fetchPosts, 
  likePost, 
  sharePost 
} = useApi();

const { preloadMemberImages } = useImageLoader();

// 計算屬性
const filteredPosts = computed(() => {
  if (!posts.value) return [];
  
  let filtered = [...posts.value];
  
  // 成員篩選
  if (filters.value.member) {
    filtered = filtered.filter(post => post.author_id === filters.value.member);
  }
  
  // 年份篩選
  if (filters.value.year) {
    filtered = filtered.filter(post => {
      const postYear = new Date(post.created_at).getFullYear();
      return postYear === filters.value.year;
    });
  }
  
  // 月份篩選
  if (filters.value.month) {
    filtered = filtered.filter(post => {
      const postMonth = new Date(post.created_at).getMonth() + 1;
      return postMonth === filters.value.month;
    });
  }
  
  // 搜尋篩選
  if (filters.value.search) {
    const searchTerm = filters.value.search.toLowerCase();
    filtered = filtered.filter(post => 
      post.text.toLowerCase().includes(searchTerm) ||
      post.author_name.toLowerCase().includes(searchTerm)
    );
  }
  
  // 喜歡篩選
  if (filters.value.liked) {
    filtered = filtered.filter(post => post.liked);
  }
  
  return filtered;
});

const selectedMember = computed(() => {
  if (!filters.value.member) return null;
  return authors.value.find(author => author.id === filters.value.member);
});

const birthdayMember = computed(() => {
  if (!ui.value.showBirthdayReminder) return null;
  return authors.value.find(author => author.id === ui.value.birthdayMemberId);
});

// 生命週期
onMounted(async () => {
  await fetchPosts();
  preloadMemberImages(authors.value);
});

// 鍵盤快捷鍵
useKeyboardShortcuts({
  onLike: () => {
    if (ui.value.selectedPost) {
      likePost(ui.value.selectedPost.id);
    }
  },
  onShare: () => {
    if (ui.value.selectedPost) {
      sharePost(ui.value.selectedPost.id);
    }
  },
  onClose: () => {
    if (ui.value.showPostDetail) closePostDetail();
    if (ui.value.showProfile) closeProfile();
  }
});

// 滑動手勢
useSwipeGestures({
  onSwipeLeft: () => {
    if (ui.value.selectedPost) {
      likePost(ui.value.selectedPost.id);
    }
  },
  onSwipeRight: () => {
    if (ui.value.selectedPost) {
      sharePost(ui.value.selectedPost.id);
    }
  }
});

// 下拉刷新
usePullRefresh({
  onRefresh: () => {
    fetchPosts();
  }
});
</script>

<style scoped>
.timeline-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}
</style>

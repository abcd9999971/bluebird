<template>
  <div id="app">
    <!-- 載入器 - 在資料載入完成前顯示 -->
    <Loader v-if="!ui.loaded" />
    
    <!-- 主要應用程式界面 -->
    <div v-else class="app-shell">
    <div class="app-container">
        <!-- 左側邊欄 - 包含導航、搜尋、篩選功能 -->
        <LeftSidebar 
          :filters="filters"
          :ui="ui"
          :prefs="prefs"
          :authors="authors"
          :characterOrder="characterOrder"
          @resetFilters="resetFilters"
          @focusSearch="focusSearch"
          @onSearchBlur="onSearchBlur"
          @toggleLikedFilter="toggleLikedFilter"
          @setMemberFilter="setMemberFilter"
          @toggleTheme="toggleTheme"
        />

        <!-- 主要時間軸區域 -->
        <main class="timeline">
          <!-- 時間軸標題列 - 包含手機版操作按鈕 -->
          <PostsHeader 
            :ui="ui"
            :filters="filters"
            :prefs="prefs"
            :headerTitle="headerTitle"
            @focusSearch="focusSearch"
            @toggleMobileSearch="toggleMobileSearch"
            @openDateNavModal="openDateNavModal"
            @onSearchBlur="onSearchBlur"
            @toggleTheme="toggleTheme"
          />
          
          <!-- 手機版導航列 - 橫向滾動的成員選擇 -->
          <MobileNav 
            :filters="filters"
            :authors="authors"
            :characterOrder="characterOrder"
            :projectInfo="projectInfo"
            @resetFilters="resetFilters"
            @toggleLikedFilter="toggleLikedFilter"
            @setMemberFilter="setMemberFilter"
          />

          <!-- 成員橫幅區域 - 顯示當前選擇的成員或主頁資訊 -->
          <MemberHeader 
            :filters="filters"
            :authors="authors"
            :projectInfo="projectInfo"
            @openProfileModal="openProfileModal"
          />

          <!-- 推文列表 - 顯示篩選後的推文或空狀態 -->
          <PostList 
            :filteredTweets="filteredTweets"
            :authors="authors"
            :ui="ui"
            @openDetail="openDetail"
            @toggleLike="toggleLike"
            @shareTweet="shareTweet"
            @handleTweetTextClick="handleTweetTextClick"
          />
        </main>

        <!-- 時間軸裝飾桿 -->
        <TimelineBar 
          :dateGroups="dateGroups"
          :activeDate="scroller.activeDate"
          :brandColor="brandColor"
        />

        <!-- 右側邊欄 - 日期導航器 -->
        <RightSidebar 
          :filters="filters"
          :availableYears="availableYears"
          :availableMonths="availableMonths"
          :dateGroups="dateGroups"
          :scroller="scroller"
          @setYear="(year) => filters.year = year"
          @setMonthFilter="setMonthFilter"
          @scrollToDate="scrollToDate"
        />
      </div>
    </div>

    <!-- 遮罩層 - 彈窗背景 -->
    <div class="overlay" :class="{ show: ui.overlay }" @click="closeAllModals"></div>

    <!-- 推文詳情彈窗 - 顯示單個推文的詳細內容 -->
    <PostDetailModal 
      :ui="ui"
      @closeModal="closeAllModals"
    />

    <!-- 個人資料彈窗 - 顯示成員或專案的詳細資訊 -->
    <ProfileModal 
      :ui="ui"
      @closeModal="closeAllModals"
    />
      
    <!-- 手機版日期導航彈窗 - 手機版的日期選擇器 -->
    <DateNavModal 
      :ui="ui"
      :filters="filters"
      :availableYears="availableYears"
      :availableMonths="availableMonths"
      :dateGroups="dateGroups"
      :scroller="scroller"
      @closeModal="closeAllModals"
      @setYear="(year) => filters.year = year"
      @setMonthFilter="setMonthFilter"
      @scrollToDate="scrollToDate"
    />

    <!-- 回到頂部按鈕 - 長頁面滾動時顯示 -->
    <ToTopButton :show="ui.showTop" />

    <!-- Toast 通知 - 顯示操作結果訊息 -->
    <ToastNotification :toast="toast" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';
import { useAppState } from './composables/useAppState.js';
import { useApi } from './composables/useApi.js';
import { useImageLoader } from './composables/useImageLoader.js';
import { shareTweetAsImage } from './utils/html2canvas-helper.js';
import { formatTime, linkify } from './utils/formatters.js';
import { processMemberData } from './utils/assets.js';
import fallbackTweetsData from './post.json';
import fallbackMembersData from './member.json';

// UI 組件引入
import Loader from './components/ui/Loader.vue';
import ToTopButton from './components/ui/ToTopButton.vue';
import ToastNotification from './components/ui/ToastNotification.vue';

// 佈局組件引入 
import LeftSidebar from './components/layout/LeftSidebar.vue';
import PostsHeader from './components/layout/PostsHeader.vue';
import MobileNav from './components/layout/MobileNav.vue';
import RightSidebar from './components/layout/RightSidebar.vue';

// 推文相關組件引入
import MemberHeader from './components/posts/MemberHeader.vue';
import PostList from './components/posts/PostList.vue';

// 彈窗組件引入
import PostDetailModal from './components/modals/PostDetailModal.vue';
import ProfileModal from './components/modals/ProfileModal.vue';
import DateNavModal from './components/modals/DateNavModal.vue';
import TimelineBar from './components/ui/TimelineBar.vue';

// === 使用 Composable 管理狀態 ===
const {
  // 狀態
  prefs,
  allTweets,
  authors,
  filters,
  ui,
  scroller,
  toast,
  
  // 計算屬性
  tweetsBeforeMonthFilter,
  availableYears,
  availableMonths,
  filteredTweets,
  dateGroups,
  brandColor,
  headerTitle,
  
  // 方法
  initializeState,
  loadMembers,
  loadTweets,
  persistLikes,
  applyTheme,
  
  // 常數
  CHARACTER_ORDER: characterOrder,
  PROJECT_INFO: projectInfo
} = useAppState();

// === 使用 API 管理 ===
const { fetchMembers, fetchTweets, toggleLike: apiToggleLike, withRetry } = useApi();

// === 使用圖片載入管理 ===
const { preloadMemberImages } = useImageLoader();

// === DOM 元素引用 ===
const searchInput = ref(null);       // 桌面版搜尋輸入框引用
const mobileSearchInput = ref(null); // 手機版搜尋輸入框引用

// === 國際化設定 ===
const { t } = useI18n(); // 使用 vue-i18n 的翻譯函數

// === 工具變數 ===
let intersectionObserver = null; // 推文可見性觀察器
let toastTimeout = null;         // Toast 自動隱藏計時器

// === 工具函數 ===

// === 計算屬性（已移至 useAppState） ===
// 當前橫幅樣式 - 根據選擇的成員或專案設定背景
const currentBannerStyle = computed(() => {
  const current = filters.member ? authors[filters.member] : projectInfo;
  return current?.banner_url ? { backgroundImage: `url(${current.banner_url})` } : { backgroundColor: current?.color || '#1d9bf0' };
});

// === 事件處理方法 ===

// 顯示名稱工具函數 - 取得作者的顯示名稱
const displayName = (author) => author?.name_ja || author?.id || '';

// 推文作者名稱格式化 - 將作者名稱格式化為推文顯示格式
const tweetAuthorName = (author) => `${displayName(author)}@いきづらい部！`;

// 頭像取得工具函數 - 取得作者頭像URL
const avatarOf = (author) => author?.avatar_url || '';

// 工具函數（已移至 formatters.js）

// 保存喜歡狀態到本地儲存 - 將用戶的喜歡記錄保存到localStorage（已移至 useAppState）

// 切換推文喜歡狀態 - 處理推文點讚/取消點讚功能
const toggleLike = async (tweet) => { 
  tweet.liked = !tweet.liked; 
  if (tweet.liked) tweet._pop = true; // 觸發點讚動畫
  
  // 嘗試同步到後端
  try {
    const userIp = '127.0.0.1'; // 簡化處理，實際應該獲取真實IP
    await apiToggleLike({
      tweetId: tweet.id,
      userIp,
      action: tweet.liked ? 'like' : 'unlike'
    });
  } catch (error) {
    console.warn('後端同步失敗，僅使用本地儲存:', error);
  }
  
  persistLikes(); 
};

// 篩選器控制方法
const setMemberFilter = (key) => { 
  filters.member = (filters.member === key) ? null : key; 
  scrollToTop(); 
};

const setMonthFilter = (month) => { 
  filters.month = (filters.month === month) ? null : month; 
};

const toggleLikedFilter = () => { 
  filters.onlyLiked = !filters.onlyLiked; 
};

// 重置所有篩選條件 - 回到主頁狀態
const resetFilters = () => { 
  filters.member = null; 
  filters.onlyLiked = false; 
  filters.search = ''; 
  if (availableYears.value.length > 0) filters.year = availableYears.value[0]; 
  filters.month = null; 
  scrollToTop(); 
};

// 遮罩層控制 - 控制彈窗背景遮罩的顯示
const toggleOverlay = (show) => { ui.overlay = !!show; };

// 開啟推文詳情彈窗 - 顯示單個推文的詳細內容
const openDetail = (tweet) => { 
  // 更新當前活動日期，用於日期導航器高亮
  scroller.activeDate = tweet.created_at.substring(0, 10);
  console.log('點擊推文，更新活動日期:', scroller.activeDate);
  
  ui.detailTweet = tweet; 
  ui.detail = true; 
  toggleOverlay(true); 
};

// 開啟個人資料彈窗 - 顯示成員或專案的詳細資訊
const openProfileModal = (author) => { 
  ui.profileModalAuthor = author; 
  toggleOverlay(true); 
};

// 開啟手機版日期導航彈窗 - 顯示手機版的日期選擇器
const openDateNavModal = () => { 
  ui.dateNavModal = true; 
  toggleOverlay(true); 
};

// 關閉所有彈窗 - 統一關閉所有打開的彈窗和遮罩
const closeAllModals = () => { 
  ui.detail = ui.dateNavModal = false; 
  ui.profileModalAuthor = null; 
  toggleOverlay(false); 
};

// 處理推文文字點擊事件 - 點擊hashtag時設定為搜尋條件
const handleTweetTextClick = (e) => { 
  const a = e.target.closest('a.hashtag'); 
  if (!a) return; 
  e.preventDefault(); 
  filters.search = a.textContent; 
  scrollToTop(); 
};

// 聚焦搜尋框 - 根據裝置類型顯示對應的搜尋輸入框
const focusSearch = () => { 
  if (window.innerWidth <= 768) { 
    ui.showMobileSearch = true; 
    nextTick(() => mobileSearchInput.value?.focus()); 
  } else { 
    ui.showSearchInput = true; 
    nextTick(() => searchInput.value?.focus()); 
  } 
};

// 切換手機版搜尋框 - 可以開啟或關閉搜尋框
const toggleMobileSearch = () => { 
  ui.showMobileSearch = !ui.showMobileSearch; 
  if (ui.showMobileSearch) {
    nextTick(() => mobileSearchInput.value?.focus()); 
  }
};

// 搜尋框失去焦點處理 - 當搜尋框為空時隱藏搜尋框
const onSearchBlur = () => { 
  if (filters.search === '') { 
    ui.showSearchInput = false; 
    ui.showMobileSearch = false; 
  } 
};

// 滾動到頂部 - 平滑滾動到頁面頂部
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const shareTweet = async (tweet) => {
  if (ui.isSharing) return;
  ui.isSharing = tweet.id;
  
  try {
    const author = authors[tweet.author_id];
    const success = await shareTweetAsImage(tweet, author, prefs.dark);
    
    if (success) {
      showToast(t('image_gen_success'), 'success');
    } else {
      showToast(t('image_gen_fail'), 'error');
    }
  } catch (error) {
    console.error('分享功能失敗:', error);
    showToast(t('image_gen_fail'), 'error');
  } finally {
    ui.isSharing = null;
  }
};

const setupIntersectionObserver = () => {
  if (intersectionObserver) intersectionObserver.disconnect();
  const options = { rootMargin: "-40% 0px -60% 0px" };
  intersectionObserver = new IntersectionObserver(entries => { 
    const i = entries.find(e => e.isIntersecting); 
    if (i) { 
      const tw = allTweets.find(t => t.id == i.target.dataset.tweetId); 
      if (tw) {
        scroller.activeDate = tw.created_at.substring(0, 10);
        console.log('當前活動日期:', scroller.activeDate);
      }
    } 
  }, options);
  document.querySelectorAll('.tweet[data-tweet-id]').forEach(el => intersectionObserver.observe(el));
};

const scrollToDate = (tweetId) => { 
  const el = document.querySelector(`.tweet[data-tweet-id="${tweetId}"]`); 
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    // 更新當前活動日期
    const tweet = allTweets.find(t => t.id == tweetId);
    if (tweet) {
      scroller.activeDate = tweet.created_at.substring(0, 10);
    }
  }
};

const handleScroll = () => { ui.showTop = window.scrollY > 400; };

const showToast = (message, type = 'success') => { 
  if (toastTimeout) clearTimeout(toastTimeout); 
  toast.message = message; 
  toast.type = type; 
  toast.show = true; 
  toastTimeout = setTimeout(() => { toast.show = false; }, 3000); 
};

// 應用主題（已移至 useAppState）

const toggleTheme = () => { 
  prefs.dark = !prefs.dark; 
  applyTheme(); 
};

// 初始化資料
const initData = async () => {
  console.log('開始初始化資料...');
  
  // 初始化狀態
  initializeState();
  
  // 嘗試從後端獲取資料
  try {
    // 獲取成員資料
    console.log('正在獲取成員資料...');
    const membersData = await withRetry(() => fetchMembers());
    console.log('成員資料:', membersData);
    
    // 載入成員資料
    loadMembers(membersData);
    
    // 獲取推文資料
    console.log('正在獲取推文資料...');
    const tweetsData = await withRetry(() => fetchTweets());
    console.log('推文資料:', tweetsData);
    
    // 載入推文資料
    loadTweets(tweetsData);
    
    console.log('後端資料載入成功！');
    console.log('成員數量:', Object.keys(authors).length);
    console.log('推文數量:', allTweets.length);
    
  } catch (backendError) {
    console.warn('後端連接失敗，使用備用資料:', backendError);
    showToast('後端連接失敗，使用範例資料', 'warning');
    
    // 載入備用成員資料
    const fallbackAuthors = processMemberData(fallbackMembersData);
    Object.assign(authors, fallbackAuthors);
    
          // 載入備用推文資料
          const processedFallbackTweets = fallbackTweetsData.map(tw => ({
            id: tw.id,
            author_id: tw.author_id,
            name_ja: authors[tw.author_id]?.name_ja || tw.author_id,
            twitter_id: authors[tw.author_id]?.twitter_id || `@${tw.author_id}`,
            color: authors[tw.author_id]?.color || '#1d9bf0',
            avatar_url: authors[tw.author_id]?.avatar_url || '',
            created_at: tw.created_at,
            content: tw.content,
            image_url: null,
            liked: false,
            _pop: false
          }));
    
    loadTweets(processedFallbackTweets);
    console.log('備用資料載入完成！');
    console.log('推文數量:', allTweets.length);
  }
  
  console.log('資料初始化完成！');
};

// 生命週期
onMounted(async () => { 
  applyTheme(); 
  
  try {
    await initData(); 
    console.log('資料初始化成功');
  } catch (error) {
    console.error('資料初始化失敗，但繼續載入界面:', error);
    // 即使資料載入失敗，也要顯示界面
  }

  ui.loaded = true;
  
    nextTick(() => {
    if (allTweets.length > 0) {
      setupIntersectionObserver();
    }
  });
  
  window.addEventListener('scroll', handleScroll, { passive: true }); 
});

onBeforeUnmount(() => { 
  window.removeEventListener('scroll', handleScroll); 
  if (intersectionObserver) intersectionObserver.disconnect(); 
});

// 監聽器
watch(brandColor, (newColor) => {
  document.documentElement.style.setProperty('--brand-color', newColor);
}, { immediate: true });

watch(filteredTweets, () => nextTick(setupIntersectionObserver));
watch(() => [filters.year, filters.member], () => { 
  if (!availableMonths.value.includes(filters.month)) { 
    filters.month = null; 
  } 
});
watch(() => filters.member, (memberKey) => { 
  document.documentElement.dataset.memberTheme = !!(memberKey && authors[memberKey]); 
});
watch(() => prefs.dark, applyTheme);
</script>

<style scoped>
/* 這裡會包含所有CSS樣式，但為了簡潔，我只列出關鍵的樣式 */
/* 完整的樣式會在下一個檔案中提供 */

.app-container {
  display: flex;
  width: 100%;
  max-width: var(--main-max-width);
}

.sidebar-left, .sidebar-right {
  backdrop-filter: blur(12px);
}

.sidebar-left {
  width: 300px;
  padding: var(--spacing-unit);
  position: sticky;
  top: 0;
  height: 100vh;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  }

  .timeline {
  width: 100%;
  max-width: var(--timeline-width);
  min-width: 0;
  border-left: 1px solid var(--border-primary);
  border-right: 1px solid var(--border-primary);
  background-color: color-mix(in srgb, var(--bg-secondary) 85%, transparent);
  min-height: 100vh;
  backdrop-filter: blur(12px);
}

.sidebar-right {
  width: var(--sidebar-width);
  padding: calc(var(--spacing-unit) * 2);
  position: sticky;
  top: 0;
  height: 100vh;
}

/* 其他樣式會在CSS檔案中定義 */
</style>
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
import { ref, reactive, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';
import { getMemberAvatar, getMemberBanner, processMemberData } from './utils/assets.js';
import { shareTweetAsImage } from './utils/html2canvas-helper.js';
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

// 專案資訊 - L高的基本資料
const projectInfo = reactive({ 
  key: 'project_home',
  name_ja: 'いきづらい部', 
  id: '@ikizulive_staff',
  avatar: '/assets/images/avatars/project-avatar.jpg',
  banner: '/assets/images/banners/project-banner.jpg',
  color: 'var(--brand-blue)',
  profile_btn_text: 'L高とは',
  profile: {
    description: 'Love学院高等学校。略してL高。\n全国にサテライト校を持つインターネット高校。\n生徒たちは自由にカリキュラムを組み、オンラインで学習できる。\nひとりひとりのライフスタイルに合わせて単位取得が可能。'
  }
});

// 國際化文本管理已移至 src/locales/ja.json

// 備用成員資料 - 當後端連接失敗時使用
const fallbackAuthors = processMemberData(fallbackMembersData);

// 備用推文資料 - 從 post.json 載入
const fallbackTweets = fallbackTweetsData;

// === 反應式資料狀態管理 ===

// 成員資料 - 存放所有成員的詳細資訊
const authors = reactive({...fallbackAuthors});
// 成員顯示順序 - 控制左側邊欄和手機版導航的排列
const characterOrder = ['polka','mai','akira','hanabi','miracle','noriko','yukuri','aurora','midori','shion'];

// 使用者偏好設定
const prefs = reactive({ dark: false }); // 深色模式切換

// 推文資料 - 存放從後端獲取的所有推文
const allTweets = reactive([]);

// 篩選條件 - 控制推文的顯示篩選
const filters = reactive({ 
  member: null,      // 選擇的成員ID
  onlyLiked: false,  // 是否只顯示喜歡的推文
  search: '',        // 搜尋關鍵字
  year: null,        // 選擇的年份
  month: null        // 選擇的月份
});

// UI 狀態管理 - 控制各種界面元素的顯示狀態
const ui = reactive({ 
  loaded: false,           // 資料是否載入完成
  overlay: false,          // 彈窗遮罩層是否顯示
  detail: false,           // 推文詳情彈窗是否顯示
  detailTweet: null,       // 當前查看的推文詳情
  showTop: false,          // 回到頂部按鈕是否顯示
  showSearchInput: false,  // 桌面版搜尋框是否顯示
  showMobileSearch: false, // 手機版搜尋框是否顯示
  isSharing: null,         // 正在分享的推文ID
  dateNavModal: false,     // 手機版日期導航彈窗是否顯示
  profileModalAuthor: null // 個人資料彈窗顯示的成員資料
});

// 滾動相關狀態 - 用於日期導航器的當前活動日期
const scroller = reactive({ activeDate: null });

// Toast 通知狀態 - 顯示操作結果訊息
const toast = reactive({ show: false, message: '', type: 'success' });

// === DOM 元素引用 ===
const searchInput = ref(null);       // 桌面版搜尋輸入框引用
const mobileSearchInput = ref(null); // 手機版搜尋輸入框引用

// === 國際化設定 ===
const { t } = useI18n(); // 使用 vue-i18n 的翻譯函數

// === 工具變數 ===
let intersectionObserver = null; // 推文可見性觀察器
let toastTimeout = null;         // Toast 自動隱藏計時器

// === 工具函數 ===

// === 計算屬性 ===
// 月份篩選前的推文資料 - 應用年份、成員、搜尋、喜歡等篩選條件
const tweetsBeforeMonthFilter = computed(() => {
  let result = [...allTweets];
  if (filters.year) result = result.filter(t => new Date(t.created_at).getFullYear() === filters.year);
  if (filters.onlyLiked) result = result.filter(t => t.liked);
  if (filters.member) result = result.filter(t => t.author_id === filters.member);
  if (filters.search) { 
    const query = filters.search.toLowerCase(); 
    result = result.filter(t => 
      t.content.toLowerCase().includes(query) || 
      (t.name_ja || authors[t.author_id]?.name_ja || '').toLowerCase().includes(query) || 
      (t.twitter_id || authors[t.author_id]?.id || '').toLowerCase().includes(query)
    ); 
  }
  return result;
});

// 可用年份清單 - 從所有推文中提取年份並排序（新到舊）
const availableYears = computed(() => [...new Set(allTweets.map(t => new Date(t.created_at).getFullYear()))].sort((a, b) => b - a));

// 可用月份清單 - 根據當前篩選條件計算該年份下有推文的月份
const availableMonths = computed(() => {
  if (!filters.year) return [];
  let filteredTweets = [...allTweets];
  if (filters.year) filteredTweets = filteredTweets.filter(t => new Date(t.created_at).getFullYear() === filters.year);
  if (filters.onlyLiked) filteredTweets = filteredTweets.filter(t => t.liked);
  if (filters.member) filteredTweets = filteredTweets.filter(t => t.author_id === filters.member);
  if (filters.search) { 
    const query = filters.search.toLowerCase(); 
    filteredTweets = filteredTweets.filter(t => 
      t.content.toLowerCase().includes(query) || 
      (t.name_ja || authors[t.author_id]?.name_ja || '').toLowerCase().includes(query) || 
      (t.twitter_id || authors[t.author_id]?.id || '').toLowerCase().includes(query)
    ); 
  }
  return [...new Set(filteredTweets.map(t => new Date(t.created_at).getMonth() + 1))];
});

// 最終篩選後的推文列表 - 應用所有篩選條件包括月份
const filteredTweets = computed(() => {
  if (!filters.month) return tweetsBeforeMonthFilter.value;
  return tweetsBeforeMonthFilter.value.filter(t => new Date(t.created_at).getMonth() + 1 === filters.month);
});

// 日期分組資料 - 將推文按日期分組並統計數量，用於右側日期導航器
const dateGroups = computed(() => {
  if (filteredTweets.value.length === 0) return [];
  const groups = filteredTweets.value.reduce((acc, tweet) => { 
    const date = tweet.created_at.substring(0, 10); 
    if (!acc[date]) { 
      acc[date] = { date, count: 0, firstTweetId: tweet.id }; 
    } 
    acc[date].count++; 
    return acc; 
  }, {});
  return Object.values(groups).sort((a, b) => new Date(b.date) - new Date(a.date));
});

// 當前品牌顏色 - 根據選擇的成員或專案顏色
const brandColor = computed(() => (filters.member && authors[filters.member]) ? authors[filters.member].color : (projectInfo?.color || '#1d9bf0'));

// 標題文字 - 根據當前篩選狀態顯示對應標題
const headerTitle = computed(() => { 
  if (filters.member) return authors[filters.member]?.name_ja || filters.member; 
  if (filters.onlyLiked) return t('filter_liked'); 
  return projectInfo?.name_ja || 'いきづらい部'; 
});

// 當前橫幅樣式 - 根據選擇的成員或專案設定背景
const currentBannerStyle = computed(() => {
  const current = filters.member ? authors[filters.member] : projectInfo;
  return current?.banner ? { backgroundImage: `url(${current.banner})` } : { backgroundColor: current?.color || '#1d9bf0' };
});

// === 事件處理方法 ===

// 顯示名稱工具函數 - 取得作者的顯示名稱
const displayName = (author) => author?.name_ja || author?.id || '';

// 推文作者名稱格式化 - 將作者名稱格式化為推文顯示格式
const tweetAuthorName = (author) => `${displayName(author)}@いきづらい部！`;

// 頭像取得工具函數 - 取得作者頭像URL
const avatarOf = (author) => author?.avatar_url || author?.avatar || '';

// 文字連結化處理 - 將hashtag轉換為可點擊連結
const linkify = (text) => (text || '').replace(/#([\w\u3000-\u9fff\u3040-\u30ff\uff00-\uffef!-]+)/g, '<a href="#" class="hashtag">#$1</a>');

// 時間格式化 - 將時間戳轉換為日文格式的易讀時間
const formatTime = (s) => new Intl.DateTimeFormat('ja-JP', { 
  year: 'numeric', 
  month: 'long', 
  day: 'numeric', 
  hour: '2-digit', 
  minute: '2-digit', 
  hour12: false 
}).format(new Date(s));

// 日期滾動器格式化 - 為右側日期導航器格式化日期顯示
const formatDateForScroller = (dateString) => new Intl.DateTimeFormat('ja-JP', { 
  month: 'long', 
  day: 'numeric' 
}).format(new Date(dateString));

// 保存喜歡狀態到本地儲存 - 將用戶的喜歡記錄保存到localStorage
const persistLikes = () => { 
  localStorage.setItem('bb_likes', JSON.stringify(allTweets.filter(t => t.liked).map(t => t.id))); 
};

// 切換推文喜歡狀態 - 處理推文點讚/取消點讚功能
const toggleLike = async (tweet) => { 
  tweet.liked = !tweet.liked; 
  if (tweet.liked) tweet._pop = true; // 觸發點讚動畫
  
  // 嘗試同步到後端
  try {
    const userIp = '127.0.0.1'; // 簡化處理，實際應該獲取真實IP
    await fetch('http://localhost:8787/api/likes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tweetId: tweet.id,
        userIp,
        action: tweet.liked ? 'like' : 'unlike'
      })
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

const applyTheme = () => { 
  document.documentElement.dataset.theme = prefs.dark ? 'dark' : 'light'; 
  localStorage.setItem('bb_theme', prefs.dark ? 'dark' : 'light'); 
};

const toggleTheme = () => { prefs.dark = !prefs.dark; };

// 初始化資料
const initData = async () => {
  prefs.dark = (localStorage.getItem('bb_theme') === 'dark');
  
  console.log('開始初始化資料...');
  
  // 嘗試從後端獲取資料
  try {
    // 獲取成員資料
    console.log('正在獲取成員資料...');
    const membersResponse = await fetch('http://localhost:8787/api/members');
    if (!membersResponse.ok) {
      throw new Error(`成員資料請求失敗: ${membersResponse.status} ${membersResponse.statusText}`);
    }
    const membersData = await membersResponse.json();
    console.log('成員資料:', membersData);
    
    // 清空現有資料並載入後端資料
    Object.keys(authors).forEach(key => delete authors[key]);
    membersData.forEach(member => {
      authors[member.id] = {
        ...member,
        avatar: getMemberAvatar(member.id), // 使用本地資源
        banner: getMemberBanner(member.id)  // 使用本地資源
      };
    });
    
    // 獲取推文資料
    console.log('正在獲取推文資料...');
    const tweetsResponse = await fetch('http://localhost:8787/api/tweets');
    if (!tweetsResponse.ok) {
      throw new Error(`推文資料請求失敗: ${tweetsResponse.status} ${tweetsResponse.statusText}`);
    }
    const tweetsData = await tweetsResponse.json();
    console.log('推文資料:', tweetsData);
    
    const processedTweets = tweetsData.map(tw => ({ 
      id: tw.id, 
      author_id: tw.author_id, 
      name_ja: tw.name_ja,
      twitter_id: tw.twitter_id,
      color: tw.color,
      avatar_url: getMemberAvatar(tw.author_id), // 使用本地資源
      created_at: tw.created_at, 
      content: tw.content, 
      image_url: tw.image_url || null, 
      liked: false, 
      _pop: false 
    })).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    // 清空現有推文並載入後端資料
    allTweets.length = 0;
    allTweets.push(...processedTweets);
    
    console.log('後端資料載入成功！');
    console.log('成員數量:', Object.keys(authors).length);
    console.log('推文數量:', allTweets.length);
    
  } catch (backendError) {
    console.warn('後端連接失敗，使用備用資料:', backendError);
    showToast('後端連接失敗，使用範例資料', 'warning');
    
    // 確保備用成員資料已載入
    if (Object.keys(authors).length === 0) {
      Object.assign(authors, fallbackAuthors);
      console.log('載入備用成員資料');
    }
    
    // 使用備用推文資料
    allTweets.length = 0;
    const processedFallbackTweets = fallbackTweets.map(tw => ({
      id: tw.id,
      author_id: tw.author_id,
      name_ja: authors[tw.author_id]?.name_ja || tw.author_id,
      twitter_id: authors[tw.author_id]?.id || `@${tw.author_id}`,
      color: authors[tw.author_id]?.color || '#1d9bf0',
      avatar_url: getMemberAvatar(tw.author_id), // 使用本地資源
      created_at: tw.created_at,
      content: tw.content,
      image_url: null,
      liked: false,
      _pop: false
    }));
    
    allTweets.push(...processedFallbackTweets);
    console.log('備用資料載入完成！');
    console.log('推文數量:', allTweets.length);
  }
  
  // 讀取本地喜歡狀態
  try { 
    const savedLikes = JSON.parse(localStorage.getItem('bb_likes') || '[]'); 
    const likeMap = new Set(savedLikes); 
    allTweets.forEach(tw => tw.liked = likeMap.has(tw.id)); 
  } catch (e) { 
    console.error("讀取 LocalStorage 中的 like 失敗", e); 
  }
  
  if (availableYears.value.length > 0) { filters.year = availableYears.value[0]; }
  
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
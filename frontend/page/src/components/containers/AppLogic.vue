<template>
  <!-- 此組件不包含模板，僅作為邏輯容器 -->
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';
import { useAppState } from '../../composables/useAppState.js';
import { useApi } from '../../composables/useApi.js';
import { useImageLoader } from '../../composables/useImageLoader.js';
import { usePullRefresh } from '../../composables/usePullRefresh.js';
import { shareTweetAsImage } from '../../utils/html2canvas-helper.js';
import { processMemberData } from '../../utils/assets.js';
import { useMemberTheme } from '../../composables/useMemberTheme.js';
import fallbackTweetsData from '../../data/tweets.json';
import fallbackMembersData from '../../data/member.json';

/**
 * 應用程式邏輯管理組件
 * 集中管理應用程式的核心業務邏輯，包括：
 * - 資料初始化與載入
 * - 事件處理方法
 * - 生命週期管理
 * - 狀態監聽器
 * 
 * 此組件作為邏輯容器，不包含任何 UI 元素，
 * 主要目的是將 App.vue 中的業務邏輯分離出來，
 * 提升程式碼的可維護性和可測試性。
 */

// === 使用 Composable 管理狀態 ===
const {
  // 狀態變數
  prefs,           // 使用者偏好設定（主題、語言等）
  allTweets,       // 所有推文資料
  authors,         // 所有成員資料
  filters,         // 篩選條件（成員、年份、月份、搜尋等）
  ui,              // UI 狀態（載入、彈窗、搜尋等）
  scroller,        // 滾動相關狀態
  toast,           // Toast 通知狀態
  
  // 計算屬性
  tweetsBeforeMonthFilter,  // 月份篩選前的推文
  availableYears,           // 可用的年份列表
  availableMonths,          // 可用的月份列表
  filteredTweets,           // 篩選後的推文
  dateGroups,               // 日期分組資料
  brandColor,               // 品牌顏色
  headerTitle,              // 標題文字
  
  // 方法
  initializeState,  // 初始化應用程式狀態
  loadMembers,      // 載入成員資料
  loadTweets,       // 載入推文資料
  persistLikes,     // 保存喜歡狀態
  applyTheme,       // 套用主題
  
  // 常數
  CHARACTER_ORDER: characterOrder,  // 成員順序
  PROJECT_INFO: projectInfo         // 專案資訊
} = useAppState();

// === 使用成員主題管理 ===
// 自動監聽 filters.member 變化並更新 CSS 變數
useMemberTheme(
  computed(() => filters.member), // 傳入 Ref 或 Computed
  authors,
  '#1d9bf0'
);

// === 使用 API 管理 ===
const { 
  fetchMembers,                    // 獲取成員資料
  fetchTweets,                     // 獲取推文資料
  toggleLike: apiToggleLike,       // API 點讚功能
  withRetry                        // 重試機制
} = useApi();

// === 使用圖片載入管理 ===
const { preloadMemberImages } = useImageLoader();

// === 使用下拉刷新管理 ===
const { 
  pullRefreshState,              // 下拉刷新狀態
  addPullRefreshListeners,       // 添加下拉刷新監聽器
  getPullProgress,               // 獲取下拉進度
  shouldShowRefreshIndicator     // 是否顯示刷新指示器
} = usePullRefresh();

// === DOM 元素引用 ===
const searchInput = ref(null);       // 桌面版搜尋輸入框引用
const mobileSearchInput = ref(null); // 手機版搜尋輸入框引用

// === 國際化設定 ===
const { t } = useI18n(); // 使用 vue-i18n 的翻譯函數

// === 工具變數 ===
let intersectionObserver = null; // 推文可見性觀察器
let toastTimeout = null;         // Toast 自動隱藏計時器

// === 計算屬性 ===
// 當前橫幅樣式 - 根據選擇的成員或專案設定背景
const currentBannerStyle = computed(() => {
  const current = filters.member ? authors[filters.member] : projectInfo;
  return current?.banner_url 
    ? { backgroundImage: `url(${current.banner_url})` } 
    : { backgroundColor: current?.color || '#1d9bf0' };
});

// === 工具函數 ===

/**
 * 顯示名稱工具函數
 * 取得作者的顯示名稱，優先使用日文名稱，其次使用 ID
 * @param {Object} author - 作者物件
 * @returns {string} 顯示名稱
 */
const displayName = (author) => author?.name_ja || author?.id || '';

/**
 * 推文作者名稱格式化
 * 將作者名稱格式化為推文顯示格式
 * @param {Object} author - 作者物件
 * @returns {string} 格式化後的名稱
 */
const tweetAuthorName = (author) => `${displayName(author)}@いきづらい部！`;

/**
 * 頭像取得工具函數
 * 取得作者頭像 URL
 * @param {Object} author - 作者物件
 * @returns {string} 頭像 URL
 */
const avatarOf = (author) => author?.avatar_url || '';

// === 事件處理方法 ===

/**
 * 切換推文喜歡狀態
 * 處理推文點讚/取消點讚功能，包含動畫效果和後端同步
 * @param {Object} tweet - 推文物件
 */
const toggleLike = async (tweet) => { 
  tweet.liked = !tweet.liked; 
  if (tweet.liked) tweet._pop = true; // 觸發點讚動畫
  
  // 嘗試同步到後端
  try {
    const userIp = '127.0.0.1'; // 簡化處理，實際應該獲取真實 IP
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

/**
 * 設定成員篩選
 * 切換成員篩選狀態，如果已選擇則取消選擇
 * @param {string} key - 成員 ID
 */
const setMemberFilter = (key) => { 
  filters.member = (filters.member === key) ? null : key; 
  scrollToTop(); 
};

/**
 * 設定月份篩選
 * 切換月份篩選狀態，如果已選擇則取消選擇
 * @param {string} month - 月份
 */
const setMonthFilter = (month) => { 
  filters.month = (filters.month === month) ? null : month; 
};

/**
 * 設定年份篩選
 * @param {string} year - 年份
 */
const setYear = (year) => {
  filters.year = year;
};

/**
 * 切換喜歡篩選
 * 切換是否只顯示已喜歡的推文
 */
const toggleLikedFilter = () => { 
  filters.onlyLiked = !filters.onlyLiked; 
};

/**
 * 重置所有篩選條件
 * 回到主頁狀態，清除所有篩選條件
 */
const resetFilters = () => { 
  filters.member = null; 
  filters.onlyLiked = false; 
  filters.search = ''; 
  if (availableYears.value.length > 0) filters.year = availableYears.value[0]; 
  filters.month = null; 
  scrollToTop(); 
};

/**
 * 遮罩層控制
 * 控制彈窗背景遮罩的顯示狀態
 * @param {boolean} show - 是否顯示遮罩
 */
const toggleOverlay = (show) => { ui.overlay = !!show; };

/**
 * 開啟推文詳情彈窗
 * 顯示單個推文的詳細內容，並更新活動日期
 * @param {Object} tweet - 推文物件
 */
const openDetail = (tweet) => { 
  // 更新當前活動日期，用於日期導航器高亮
  scroller.activeDate = tweet.created_at.substring(0, 10);
  console.log('點擊推文，更新活動日期:', scroller.activeDate);
  
  ui.detailTweet = tweet; 
  ui.detail = true; 
  toggleOverlay(true); 
};

/**
 * 開啟個人資料彈窗
 * 顯示成員或專案的詳細資訊
 * @param {Object} author - 作者物件
 */
const openProfileModal = (author) => { 
  ui.profileModalAuthor = author; 
  toggleOverlay(true); 
};

/**
 * 開啟手機版日期導航彈窗
 * 顯示手機版的日期選擇器
 */
const openDateNavigationModal = () => { 
  ui.dateNavModal = true; 
  toggleOverlay(true); 
};

/**
 * 關閉所有彈窗
 * 統一關閉所有打開的彈窗和遮罩
 */
const closeAllModals = () => { 
  ui.detail = ui.dateNavModal = false; 
  ui.profileModalAuthor = null; 
  toggleOverlay(false); 
};

/**
 * 處理推文文字點擊事件
 * 點擊 hashtag 時設定為搜尋條件
 * @param {Event} e - 點擊事件
 */
const handleTweetTextClick = (e) => { 
  const a = e.target.closest('a.hashtag'); 
  if (!a) return; 
  e.preventDefault(); 
  filters.search = a.textContent; 
  scrollToTop(); 
};

/**
 * 聚焦搜尋框
 * 根據裝置類型顯示對應的搜尋輸入框
 */
const focusSearch = () => { 
  if (window.innerWidth <= 768) { 
    ui.showMobileSearch = true; 
    nextTick(() => mobileSearchInput.value?.focus()); 
  } else { 
    ui.showSearchInput = true; 
    nextTick(() => searchInput.value?.focus()); 
  } 
};

/**
 * 切換手機版搜尋框
 * 可以開啟或關閉搜尋框
 */
const toggleMobileSearch = () => { 
  ui.showMobileSearch = !ui.showMobileSearch; 
  if (ui.showMobileSearch) {
    nextTick(() => mobileSearchInput.value?.focus()); 
  }
};

/**
 * 搜尋框失去焦點處理
 * 當搜尋框為空時隱藏搜尋框
 */
const onSearchBlur = () => { 
  if (filters.search === '') { 
    ui.showSearchInput = false; 
    ui.showMobileSearch = false; 
  } 
};

/**
 * 滾動到頂部
 * 平滑滾動到頁面頂部
 */
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

/**
 * 分享推文
 * 將推文轉換為圖片並下載
 * @param {Object} tweet - 推文物件
 */
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

/**
 * 設定交集觀察器
 * 監聽推文的可見性，用於更新活動日期
 */
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

/**
 * 滾動到指定日期
 * 滾動到指定推文的位置
 * @param {number} tweetId - 推文 ID
 */
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

/**
 * 處理滾動事件
 * 控制回到頂部按鈕的顯示
 */
const handleScroll = () => { 
  // 只有在滾動超過 400px 且不在頂部附近時才顯示回到頂部按鈕
  ui.showTop = window.scrollY > 400 && window.scrollY > 50; 
};

/**
 * 顯示 Toast 通知
 * 顯示操作結果訊息
 * @param {string} message - 訊息內容
 * @param {string} type - 訊息類型（success, error, warning）
 */
const showToast = (message, type = 'success') => { 
  if (toastTimeout) clearTimeout(toastTimeout); 
  toast.message = message; 
  toast.type = type; 
  toast.show = true; 
  toastTimeout = setTimeout(() => { toast.show = false; }, 3000); 
};

/**
 * 下拉刷新回調函數
 * 處理下拉刷新操作，重新載入推文資料
 */
const handlePullRefresh = async () => {
  try {
    // 重新載入推文資料
    const tweetsData = await withRetry(() => fetchTweets());
    loadTweets(tweetsData);
    showToast('推文已更新', 'success');
  } catch (error) {
    console.error('刷新失敗:', error);
    showToast('刷新失敗', 'error');
  }
};

/**
 * 切換主題
 * 在明暗主題之間切換
 */
const toggleTheme = () => { 
  prefs.dark = !prefs.dark; 
  applyTheme(); 
};

/**
 * 初始化資料
 * 載入應用程式所需的初始資料，包含後端資料和備用資料
 */
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
      tweet_id: tw.tweet_id || tw.id,
      author_id: tw.author_id,
      name_ja: authors[tw.author_id]?.name_ja || tw.author_id,
      twitter_id: authors[tw.author_id]?.twitter_id || `@${tw.author_id}`,
      color: authors[tw.author_id]?.color || '#1d9bf0',
      avatar_url: authors[tw.author_id]?.avatar_url || '',
      created_at: tw.created_at,
      content: tw.content,
      type: tw.type || 'Tweet',
      hashtags: tw.hashtags || null,
      urls: tw.urls || null,
      image_url: tw.image_url || null,
      media_type: tw.media_type || null,
      liked: false,
      _pop: false
    }));
    
    loadTweets(processedFallbackTweets);
    console.log('備用資料載入完成！');
    console.log('推文數量:', allTweets.length);
  }
  
  console.log('資料初始化完成！');
};

// === 生命週期管理 ===
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
  
  // 初始化下拉刷新監聽器（僅手機版）
  if (window.innerWidth <= 768) {
    addPullRefreshListeners(document.body, handlePullRefresh);
  }
});

onBeforeUnmount(() => { 
  window.removeEventListener('scroll', handleScroll); 
  if (intersectionObserver) intersectionObserver.disconnect(); 
});

// === 狀態監聽器 ===
// 監聽篩選後推文變化，重新設定交集觀察器
watch(filteredTweets, () => nextTick(setupIntersectionObserver));

// 監聽年份和成員篩選變化，重置月份篩選
watch(() => [filters.year, filters.member], () => { 
  if (!availableMonths.value.includes(filters.month)) { 
    filters.month = null; 
  } 
});

// 監聽主題變化，套用新主題
watch(() => prefs.dark, applyTheme);

// === 暴露給父組件的方法和狀態 ===
defineExpose({
  // 狀態
  prefs,
  allTweets,
  authors,
  filters,
  ui,
  scroller,
  toast,
  pullRefreshState,
  
  // 計算屬性
  availableYears,
  availableMonths,
  filteredTweets,
  dateGroups,
  brandColor,
  headerTitle,
  characterOrder,
  projectInfo,
  currentBannerStyle,
  
  // 方法
  setMemberFilter,
  setMonthFilter,
  setYear,
  toggleLikedFilter,
  resetFilters,
  openDetail,
  openProfileModal,
  openDateNavigationModal,
  closeAllModals,
  handleTweetTextClick,
  focusSearch,
  toggleMobileSearch,
  onSearchBlur,
  toggleLike,
  shareTweet,
  scrollToDate,
  toggleTheme,
  shouldShowRefreshIndicator,
  
  // 工具函數
  displayName,
  tweetAuthorName,
  avatarOf
});
</script>

/**
 * 應用程式狀態管理 Composable
 * 集中管理應用程式的全域狀態
 */

import { reactive, computed, watch } from 'vue';
import { STORAGE_KEYS, CHARACTER_ORDER, PROJECT_INFO, DEFAULT_BRAND_COLOR } from '../utils/constants.js';
import { processMemberData } from '../utils/assets.js';

/**
 * 全域狀態管理
 */
export function useAppState() {
  // 使用者偏好設定
  const prefs = reactive({ 
    dark: false // 深色模式切換
  });

  // 推文資料 - 存放從後端獲取的所有推文
  const allTweets = reactive([]);

  // 成員資料 - 存放所有成員的詳細資訊
  const authors = reactive({});

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

  // === 計算屬性 ===

  // 月份篩選前的推文資料 - 應用年份、成員、搜尋、喜歡等篩選條件
  const tweetsBeforeMonthFilter = computed(() => {
    let result = [...allTweets];
    
    if (filters.year) {
      result = result.filter(t => new Date(t.created_at).getFullYear() === filters.year);
    }
    
    if (filters.onlyLiked) {
      result = result.filter(t => t.liked);
    }
    
    if (filters.member) {
      result = result.filter(t => t.author_id === filters.member);
    }
    
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
  const availableYears = computed(() => 
    [...new Set(allTweets.map(t => new Date(t.created_at).getFullYear()))]
      .sort((a, b) => b - a)
  );

  // 可用月份清單 - 根據當前篩選條件計算該年份下有推文的月份
  const availableMonths = computed(() => {
    if (!filters.year) return [];
    
    return [...new Set(tweetsBeforeMonthFilter.value
      .filter(t => new Date(t.created_at).getFullYear() === filters.year)
      .map(t => new Date(t.created_at).getMonth() + 1)
    )];
  });

  // 最終篩選後的推文列表 - 應用所有篩選條件包括月份
  const filteredTweets = computed(() => {
    if (!filters.month) return tweetsBeforeMonthFilter.value;
    return tweetsBeforeMonthFilter.value.filter(t => 
      new Date(t.created_at).getMonth() + 1 === filters.month
    );
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
  const brandColor = computed(() => 
    (filters.member && authors[filters.member]) 
      ? authors[filters.member].color 
      : (PROJECT_INFO?.color || DEFAULT_BRAND_COLOR)
  );

  // 標題文字 - 根據當前篩選狀態顯示對應標題
  const headerTitle = computed(() => { 
    if (filters.member) return authors[filters.member]?.name_ja || filters.member; 
    if (filters.onlyLiked) return 'いいねした日誌'; 
    return PROJECT_INFO?.name_ja || 'いきづらい部'; 
  });

  // === 狀態管理方法 ===

  /**
   * 初始化狀態
   */
  const initializeState = () => {
    // 載入主題設定
    prefs.dark = (localStorage.getItem(STORAGE_KEYS.THEME) === 'dark');
    
    // 載入喜歡狀態
    try { 
      const savedLikes = JSON.parse(localStorage.getItem(STORAGE_KEYS.LIKES) || '[]'); 
      const likeMap = new Set(savedLikes); 
      allTweets.forEach(tw => tw.liked = likeMap.has(tw.id)); 
    } catch (e) { 
      console.error("讀取 LocalStorage 中的 like 失敗", e); 
    }
  };

  /**
   * 載入成員資料
   */
  const loadMembers = (membersData) => {
    Object.keys(authors).forEach(key => delete authors[key]);
    
    // 處理陣列格式的資料
    if (Array.isArray(membersData)) {
      membersData.forEach(member => {
        authors[member.id] = {
          ...member,
          avatar_url: member.avatar_url,
          banner_url: member.banner_url
        };
      });
    } else {
      // 處理物件格式的資料
      Object.entries(membersData).forEach(([memberId, member]) => {
        authors[memberId] = {
          ...member,
          avatar_url: member.avatar_url,
          banner_url: member.banner_url
        };
      });
    }
  };

  /**
   * 載入推文資料
   */
  const loadTweets = (tweetsData) => {
    allTweets.length = 0;
    const processedTweets = tweetsData.map(tw => ({ 
      id: tw.id, 
      author_id: tw.author_id, 
      name_ja: tw.name_ja || authors[tw.author_id]?.name_ja || tw.author_id,
      twitter_id: tw.twitter_id || authors[tw.author_id]?.twitter_id || `@${tw.author_id}`,
      color: tw.color || authors[tw.author_id]?.color || '#1d9bf0',
      avatar_url: tw.avatar_url || authors[tw.author_id]?.avatar_url || '',
      created_at: tw.created_at, 
      content: tw.content, 
      image_url: tw.image_url || null, 
      liked: false, 
      _pop: false 
    })).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    allTweets.push(...processedTweets);
    
    // 設定預設年份
    if (availableYears.value.length > 0 && !filters.year) { 
      filters.year = availableYears.value[0]; 
    }
  };

  /**
   * 保存喜歡狀態到本地儲存
   */
  const persistLikes = () => { 
    localStorage.setItem(STORAGE_KEYS.LIKES, 
      JSON.stringify(allTweets.filter(t => t.liked).map(t => t.id))
    ); 
  };

  /**
   * 應用主題
   */
  const applyTheme = () => { 
    document.documentElement.dataset.theme = prefs.dark ? 'dark' : 'light'; 
    localStorage.setItem(STORAGE_KEYS.THEME, prefs.dark ? 'dark' : 'light'); 
  };

  // === 監聽器 ===
  
  // 監聽主題變化
  watch(() => prefs.dark, applyTheme);
  
  // 監聽成員篩選變化，更新主題
  watch(() => filters.member, (memberKey) => { 
    document.documentElement.dataset.memberTheme = !!(memberKey && authors[memberKey]); 
  });
  
  // 監聽年份和成員變化，重置月份篩選
  watch(() => [filters.year, filters.member], () => { 
    if (!availableMonths.value.includes(filters.month)) { 
      filters.month = null; 
    } 
  });

  return {
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
    CHARACTER_ORDER,
    PROJECT_INFO
  };
}

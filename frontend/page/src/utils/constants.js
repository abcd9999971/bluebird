/**
 * 統一的常數管理模組
 * 集中管理應用程式中的所有常數
 */

/**
 * 成員印象色配置 - 各成員專屬的品牌色彩
 */
export const MEMBER_COLORS = {
  'polka': '#ccb12e',   // 高橋ポルカ - 金黃色
  'mai': '#009fdf',     // 麻布麻衣 - 藍色  
  'akira': '#88d66e',   // 五桐玲 - 綠色
  'hanabi': '#ff2021',  // 駒形花火 - 紅色
  'miracle': '#ffb7f1', // 金澤奇跡 - 粉色
  'noriko': '#ae62ff',  // 調布のりこ - 紫色
  'yukuri': '#5ecbd1',  // 春宮ゆかり - 青綠色
  'aurora': '#fd589e',  // 此花輝夜 - 玫瑰色
  'midori': '#16b500',  // 山田真緑 - 深綠色
  'shion': '#9b9b9b'    // 佐々木翔音 - 灰色
};

/**
 * 成員顯示順序 - 控制左側邊欄和手機版導航的排列
 */
export const CHARACTER_ORDER = [
  'polka', 'mai', 'akira', 'hanabi', 'miracle', 
  'noriko', 'yukuri', 'aurora', 'midori', 'shion'
];

/**
 * 預設品牌顏色
 */
export const DEFAULT_BRAND_COLOR = '#1d9bf0';

/**
 * 專案資訊 - L高的基本資料
 */
export const PROJECT_INFO = {
  key: 'project_home',
  name_ja: 'いきづらい部', 
  id: '@ikizulive_staff',
  avatar_url: '/assets/images/avatars/project-avatar.jpg',
  banner_url: '/assets/images/banners/project-banner.jpg',
  color: 'var(--brand-blue)',
  profile_btn_text: 'L高とは',
  profile: {
    description: 'Love学院高等学校。略してL高。\n全国にサテライト校を持つインターネット高校。\n生徒たちは自由にカリキュラムを組み、オンラインで学習できる。\nひとりひとりのライフスタイルに合わせて単位取得が可能。'
  }
};

/**
 * API 端點配置
 */
export const API_ENDPOINTS = {
  MEMBERS: '/api/members',
  TWEETS: '/api/tweets',
  STATS: '/api/stats',
  LIKES: '/api/likes',
  LIKES_STATUS: '/api/likes/status'
};

/**
 * 本地儲存鍵值
 */
export const STORAGE_KEYS = {
  THEME: 'bb_theme',
  LIKES: 'bb_likes'
};

/**
 * 響應式斷點
 */
export const BREAKPOINTS = {
  MOBILE: 768,
  TABLET: 1024,
  DESKTOP: 1200,
  LARGE_DESKTOP: 1440
};

/**
 * 動畫持續時間
 */
export const ANIMATION_DURATION = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500
};

/**
 * 分頁配置
 */
export const PAGINATION = {
  DEFAULT_LIMIT: 50,
  MAX_LIMIT: 100
};

/**
 * 圖片載入配置
 */
export const IMAGE_CONFIG = {
  TIMEOUT: 15000,
  RETRY_ATTEMPTS: 3,
  LAZY_LOAD_OFFSET: 100
};

/**
 * 統一的格式化工具函數模組
 * 提供時間、文字、數字等格式化功能
 */

/**
 * 時間格式化 - 將時間戳轉換為日文格式的易讀時間
 * @param {string|Date} dateInput - 時間戳或日期物件
 * @returns {string} 格式化後的時間字串
 */
export function formatTime(dateInput) {
  const date = new Date(dateInput);
  return new Intl.DateTimeFormat('ja-JP', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric', 
    hour: '2-digit', 
    minute: '2-digit', 
    hour12: false 
  }).format(date);
}

/**
 * 日期滾動器格式化 - 為右側日期導航器格式化日期顯示
 * @param {string|Date} dateInput - 日期字串或日期物件
 * @returns {string} 格式化後的日期字串
 */
export function formatDateForScroller(dateInput) {
  const date = new Date(dateInput);
  return new Intl.DateTimeFormat('ja-JP', { 
    month: 'long', 
    day: 'numeric' 
  }).format(date);
}

/**
 * 文字連結化處理 - 將hashtag轉換為可點擊連結
 * @param {string} text - 原始文字
 * @returns {string} 包含連結的HTML字串
 */
export function linkify(text, searchTerm = '') {
  if (!text) return '';
  
  let processedText = text;
  
  // 如果有搜尋關鍵字，先高亮顯示
  if (searchTerm && searchTerm.trim()) {
    const regex = new RegExp(`(${searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    processedText = processedText.replace(regex, '<mark class="search-highlight">$1</mark>');
  }
  
  // 處理 hashtag
  return processedText.replace(/#([\w\u3000-\u9fff\u3040-\u30ff\uff00-\uffef!-]+)/g, 
    '<a href="#" class="hashtag">#$1</a>'
  );
}

/**
 * 顯示名稱工具函數 - 取得作者的顯示名稱
 * @param {Object} author - 作者物件
 * @returns {string} 顯示名稱
 */
export function getDisplayName(author) {
  return author?.name_ja || author?.id || '';
}

/**
 * 推文作者名稱格式化 - 將作者名稱格式化為推文顯示格式
 * @param {Object} author - 作者物件
 * @returns {string} 格式化後的作者名稱
 */
export function formatTweetAuthorName(author) {
  return `${getDisplayName(author)}@いきづらい部！`;
}

/**
 * 頭像取得工具函數 - 取得作者頭像URL
 * @param {Object} author - 作者物件
 * @returns {string} 頭像URL
 */
export function getAvatarUrl(author) {
  return author?.avatar_url || '';
}

/**
 * 數字格式化 - 將數字格式化為易讀格式
 * @param {number} num - 數字
 * @returns {string} 格式化後的數字字串
 */
export function formatNumber(num) {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
}

/**
 * 相對時間格式化 - 將時間轉換為相對時間（如「2小時前」）
 * @param {string|Date} dateInput - 時間戳或日期物件
 * @returns {string} 相對時間字串
 */
export function formatRelativeTime(dateInput) {
  const date = new Date(dateInput);
  const now = new Date();
  const diffInSeconds = Math.floor((now - date) / 1000);
  
  if (diffInSeconds < 60) {
    return '剛剛';
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `${minutes}分鐘前`;
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `${hours}小時前`;
  } else if (diffInSeconds < 2592000) {
    const days = Math.floor(diffInSeconds / 86400);
    return `${days}天前`;
  } else {
    return formatTime(dateInput);
  }
}

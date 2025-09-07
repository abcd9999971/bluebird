/**
 * 鍵盤快捷鍵管理 Composable
 * 提供統一的鍵盤快捷鍵處理功能
 */

import { ref, onMounted, onBeforeUnmount } from 'vue';

export function useKeyboardShortcuts() {
  // 當前焦點的推文索引
  const focusedTweetIndex = ref(-1);
  const tweetElements = ref([]);

  /**
   * 更新推文元素列表
   * @param {Array} elements - 推文 DOM 元素陣列
   */
  const updateTweetElements = (elements) => {
    tweetElements.value = elements;
  };

  /**
   * 處理鍵盤事件
   * @param {KeyboardEvent} event - 鍵盤事件
   * @param {Object} callbacks - 回調函數物件
   */
  const handleKeydown = (event, callbacks = {}) => {
    // 如果正在輸入文字，不處理快捷鍵
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA' || event.target.contentEditable === 'true') {
      return;
    }

    const { 
      onTweetNavigate, 
      onTweetLike, 
      onTweetShare, 
      onModalClose,
      onSearchFocus 
    } = callbacks;

    switch (event.key.toLowerCase()) {
      case 'j':
        // 向下瀏覽推文
        event.preventDefault();
        if (onTweetNavigate) {
          onTweetNavigate('down');
        }
        break;

      case 'k':
        // 向上瀏覽推文
        event.preventDefault();
        if (onTweetNavigate) {
          onTweetNavigate('up');
        }
        break;

      case 'l':
        // 點讚當前推文
        event.preventDefault();
        if (onTweetLike) {
          onTweetLike();
        }
        break;

      case 'r':
        // 分享推文
        event.preventDefault();
        if (onTweetShare) {
          onTweetShare();
        }
        break;

      case 'escape':
        // 關閉彈窗
        event.preventDefault();
        if (onModalClose) {
          onModalClose();
        }
        break;

      case '/':
        // 聚焦搜尋框
        event.preventDefault();
        if (onSearchFocus) {
          onSearchFocus();
        }
        break;
    }
  };

  /**
   * 導航到指定推文
   * @param {string} direction - 方向 ('up' 或 'down')
   * @param {Array} tweets - 推文陣列
   */
  const navigateToTweet = (direction, tweets) => {
    if (tweets.length === 0) return;

    const currentIndex = focusedTweetIndex.value;
    let newIndex;

    if (direction === 'down') {
      newIndex = currentIndex < tweets.length - 1 ? currentIndex + 1 : 0;
    } else {
      newIndex = currentIndex > 0 ? currentIndex - 1 : tweets.length - 1;
    }

    focusedTweetIndex.value = newIndex;
    
    // 滾動到焦點推文
    const tweetElement = tweetElements.value[newIndex];
    if (tweetElement) {
      tweetElement.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'center' 
      });
      
      // 添加焦點樣式
      tweetElement.classList.add('tweet-focused');
      setTimeout(() => {
        tweetElement.classList.remove('tweet-focused');
      }, 2000);
    }
  };

  /**
   * 獲取當前焦點的推文
   * @param {Array} tweets - 推文陣列
   * @returns {Object|null} 當前焦點的推文
   */
  const getFocusedTweet = (tweets) => {
    if (focusedTweetIndex.value >= 0 && focusedTweetIndex.value < tweets.length) {
      return tweets[focusedTweetIndex.value];
    }
    return null;
  };

  /**
   * 重置焦點
   */
  const resetFocus = () => {
    focusedTweetIndex.value = -1;
  };

  /**
   * 初始化鍵盤監聽器
   * @param {Object} callbacks - 回調函數
   */
  const initKeyboardListeners = (callbacks) => {
    const keydownHandler = (event) => handleKeydown(event, callbacks);
    
    onMounted(() => {
      document.addEventListener('keydown', keydownHandler);
    });

    onBeforeUnmount(() => {
      document.removeEventListener('keydown', keydownHandler);
    });
  };

  return {
    focusedTweetIndex,
    updateTweetElements,
    handleKeydown,
    navigateToTweet,
    getFocusedTweet,
    resetFocus,
    initKeyboardListeners
  };
}

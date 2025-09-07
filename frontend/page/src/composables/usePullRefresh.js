/**
 * 下拉刷新管理 Composable
 * 提供下拉刷新推文的功能
 */

import { ref, onMounted, onBeforeUnmount } from 'vue';

export function usePullRefresh() {
  // 下拉刷新狀態
  const pullRefreshState = ref({
    isPulling: false,
    startY: 0,
    currentY: 0,
    pullDistance: 0,
    isRefreshing: false
  });

  // 下拉刷新配置
  const PULL_THRESHOLD = 80; // 觸發刷新的距離
  const MAX_PULL_DISTANCE = 120; // 最大下拉距離

  /**
   * 處理觸控開始事件
   * @param {TouchEvent} event - 觸控事件
   */
  const handleTouchStart = (event) => {
    // 只有在頁面頂部時才允許下拉刷新
    if (window.scrollY > 0) return;

    const touch = event.touches[0];
    pullRefreshState.value = {
      ...pullRefreshState.value,
      startY: touch.clientY,
      currentY: touch.clientY,
      isPulling: true
    };
  };

  /**
   * 處理觸控移動事件
   * @param {TouchEvent} event - 觸控事件
   */
  const handleTouchMove = (event) => {
    if (!pullRefreshState.value.isPulling) return;

    const touch = event.touches[0];
    const deltaY = touch.clientY - pullRefreshState.value.startY;

    // 只有向下拉動時才處理
    if (deltaY > 0) {
      pullRefreshState.value.currentY = touch.clientY;
      pullRefreshState.value.pullDistance = Math.min(deltaY, MAX_PULL_DISTANCE);
      
      // 防止頁面滾動
      if (pullRefreshState.value.pullDistance > 0) {
        event.preventDefault();
      }
    }
  };

  /**
   * 處理觸控結束事件
   * @param {TouchEvent} event - 觸控事件
   * @param {Function} onRefresh - 刷新回調函數
   */
  const handleTouchEnd = (event, onRefresh) => {
    if (!pullRefreshState.value.isPulling) return;

    const { pullDistance } = pullRefreshState.value;

    if (pullDistance >= PULL_THRESHOLD && onRefresh) {
      pullRefreshState.value.isRefreshing = true;
      onRefresh().finally(() => {
        pullRefreshState.value.isRefreshing = false;
      });
    }

    // 重置狀態
    pullRefreshState.value = {
      isPulling: false,
      startY: 0,
      currentY: 0,
      pullDistance: 0,
      isRefreshing: false
    };
  };

  /**
   * 為元素添加下拉刷新監聽器
   * @param {HTMLElement} element - 目標元素
   * @param {Function} onRefresh - 刷新回調函數
   */
  const addPullRefreshListeners = (element, onRefresh) => {
    if (!element) return;

    const touchStartHandler = (event) => handleTouchStart(event);
    const touchMoveHandler = (event) => handleTouchMove(event);
    const touchEndHandler = (event) => handleTouchEnd(event, onRefresh);

    element.addEventListener('touchstart', touchStartHandler, { passive: false });
    element.addEventListener('touchmove', touchMoveHandler, { passive: false });
    element.addEventListener('touchend', touchEndHandler, { passive: true });

    // 返回清理函數
    return () => {
      element.removeEventListener('touchstart', touchStartHandler);
      element.removeEventListener('touchmove', touchMoveHandler);
      element.removeEventListener('touchend', touchEndHandler);
    };
  };

  /**
   * 獲取下拉刷新的進度百分比
   * @returns {number} 進度百分比 (0-1)
   */
  const getPullProgress = () => {
    return Math.min(pullRefreshState.value.pullDistance / PULL_THRESHOLD, 1);
  };

  /**
   * 檢查是否應該顯示刷新指示器
   * @returns {boolean} 是否顯示指示器
   */
  const shouldShowRefreshIndicator = () => {
    return pullRefreshState.value.pullDistance > 0 || pullRefreshState.value.isRefreshing;
  };

  return {
    pullRefreshState,
    addPullRefreshListeners,
    getPullProgress,
    shouldShowRefreshIndicator
  };
}

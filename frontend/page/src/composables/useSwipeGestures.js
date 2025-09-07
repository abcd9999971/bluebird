/**
 * 滑動手勢管理 Composable
 * 提供左滑點讚、右滑分享等手勢操作功能
 */

import { ref, onMounted, onBeforeUnmount } from 'vue';

export function useSwipeGestures() {
  // 滑動狀態
  const swipeState = ref({
    startX: 0,
    startY: 0,
    currentX: 0,
    currentY: 0,
    isSwipeActive: false,
    swipeDirection: null
  });

  // 滑動閾值
  const SWIPE_THRESHOLD = 50; // 最小滑動距離
  const SWIPE_ANGLE_THRESHOLD = 30; // 最大角度偏差

  /**
   * 處理觸控開始事件
   * @param {TouchEvent} event - 觸控事件
   */
  const handleTouchStart = (event) => {
    const touch = event.touches[0];
    swipeState.value = {
      startX: touch.clientX,
      startY: touch.clientY,
      currentX: touch.clientX,
      currentY: touch.clientY,
      isSwipeActive: true,
      swipeDirection: null
    };
  };

  /**
   * 處理觸控移動事件
   * @param {TouchEvent} event - 觸控事件
   */
  const handleTouchMove = (event) => {
    if (!swipeState.value.isSwipeActive) return;

    const touch = event.touches[0];
    swipeState.value.currentX = touch.clientX;
    swipeState.value.currentY = touch.clientY;

    const deltaX = swipeState.value.currentX - swipeState.value.startX;
    const deltaY = swipeState.value.currentY - swipeState.value.startY;

    // 計算滑動角度
    const angle = Math.abs(Math.atan2(deltaY, deltaX) * 180 / Math.PI);

    // 判斷滑動方向
    if (Math.abs(deltaX) > SWIPE_THRESHOLD && angle < SWIPE_ANGLE_THRESHOLD) {
      if (deltaX > 0) {
        swipeState.value.swipeDirection = 'right';
      } else {
        swipeState.value.swipeDirection = 'left';
      }
    }
  };

  /**
   * 處理觸控結束事件
   * @param {TouchEvent} event - 觸控事件
   * @param {Object} callbacks - 回調函數
   */
  const handleTouchEnd = (event, callbacks = {}) => {
    if (!swipeState.value.isSwipeActive) return;

    const deltaX = swipeState.value.currentX - swipeState.value.startX;
    const deltaY = swipeState.value.currentY - swipeState.value.startY;

    // 檢查是否為有效的滑動
    if (Math.abs(deltaX) > SWIPE_THRESHOLD && Math.abs(deltaY) < SWIPE_THRESHOLD) {
      const { onSwipeLeft, onSwipeRight } = callbacks;

      if (swipeState.value.swipeDirection === 'left' && onSwipeLeft) {
        onSwipeLeft();
      } else if (swipeState.value.swipeDirection === 'right' && onSwipeRight) {
        onSwipeRight();
      }
    }

    // 重置滑動狀態
    swipeState.value.isSwipeActive = false;
    swipeState.value.swipeDirection = null;
  };

  /**
   * 為元素添加滑動手勢監聽器
   * @param {HTMLElement} element - 目標元素
   * @param {Object} callbacks - 回調函數
   */
  const addSwipeListeners = (element, callbacks) => {
    if (!element) return;

    const touchStartHandler = (event) => handleTouchStart(event);
    const touchMoveHandler = (event) => handleTouchMove(event);
    const touchEndHandler = (event) => handleTouchEnd(event, callbacks);

    element.addEventListener('touchstart', touchStartHandler, { passive: true });
    element.addEventListener('touchmove', touchMoveHandler, { passive: true });
    element.addEventListener('touchend', touchEndHandler, { passive: true });

    // 返回清理函數
    return () => {
      element.removeEventListener('touchstart', touchStartHandler);
      element.removeEventListener('touchmove', touchMoveHandler);
      element.removeEventListener('touchend', touchEndHandler);
    };
  };

  /**
   * 為多個元素添加滑動手勢監聽器
   * @param {NodeList|Array} elements - 元素列表
   * @param {Object} callbacks - 回調函數
   */
  const addSwipeListenersToElements = (elements, callbacks) => {
    const cleanupFunctions = [];

    elements.forEach(element => {
      const cleanup = addSwipeListeners(element, callbacks);
      if (cleanup) {
        cleanupFunctions.push(cleanup);
      }
    });

    // 返回清理函數
    return () => {
      cleanupFunctions.forEach(cleanup => cleanup());
    };
  };

  return {
    swipeState,
    addSwipeListeners,
    addSwipeListenersToElements
  };
}

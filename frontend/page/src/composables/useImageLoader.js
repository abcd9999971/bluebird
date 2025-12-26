/**
 * 圖片載入管理 Composable
 * 提供圖片預載入和快取功能
 */

import { ref, reactive } from 'vue';
import { IMAGE_CONFIG } from '../utils/constants.js';

/**
 * 圖片載入狀態管理
 */
export function useImageLoader() {
  // 圖片載入狀態
  const imageStates = reactive(new Map());
  
  // 載入佇列
  const loadingQueue = ref([]);
  
  // 是否正在載入
  const isLoading = ref(false);

  /**
   * 載入單張圖片
   * @param {string} src - 圖片來源
   * @param {Object} options - 載入選項
   * @returns {Promise<boolean>} 載入是否成功
   */
  const loadImage = (src, options = {}) => {
    return new Promise((resolve) => {
      // 如果已經載入過，直接返回
      if (imageStates.has(src)) {
        resolve(imageStates.get(src).loaded);
        return;
      }

      const img = new Image();
      const timeout = options.timeout || IMAGE_CONFIG.TIMEOUT;
      
      // 設定載入狀態
      imageStates.set(src, {
        loaded: false,
        loading: true,
        error: false,
        retryCount: 0
      });

      // 載入成功
      img.onload = () => {
        imageStates.set(src, {
          loaded: true,
          loading: false,
          error: false,
          retryCount: 0
        });
        resolve(true);
      };

      // 載入失敗
      img.onerror = () => {
        const currentState = imageStates.get(src);
        const retryCount = currentState.retryCount + 1;
        
        if (retryCount < IMAGE_CONFIG.RETRY_ATTEMPTS) {
          // 重試載入
          setTimeout(() => {
            imageStates.set(src, {
              loaded: false,
              loading: true,
              error: false,
              retryCount
            });
            img.src = src;
          }, 1000 * retryCount);
        } else {
          // 載入失敗
          imageStates.set(src, {
            loaded: false,
            loading: false,
            error: true,
            retryCount
          });
          resolve(false);
        }
      };

      // 設定超時
      setTimeout(() => {
        if (!imageStates.get(src)?.loaded) {
          img.onerror();
        }
      }, timeout);

      img.src = src;
    });
  };

  /**
   * 批量載入圖片
   * @param {string[]} sources - 圖片來源陣列
   * @param {Object} options - 載入選項
   * @returns {Promise<boolean[]>} 載入結果陣列
   */
  const loadImages = async (sources, options = {}) => {
    const promises = sources.map(src => loadImage(src, options));
    return Promise.all(promises);
  };

  /**
   * 預載入關鍵圖片
   * @param {string[]} criticalImages - 關鍵圖片陣列
   * @returns {Promise<void>}
   */
  const preloadCriticalImages = async (criticalImages) => {
    isLoading.value = true;
    
    try {
      await loadImages(criticalImages, { timeout: 10000 });
    } finally {
      isLoading.value = false;
    }
  };


  /**
   * 取得圖片載入狀態
   * @param {string} src - 圖片來源
   * @returns {Object} 載入狀態
   */
  const getImageState = (src) => {
    return imageStates.get(src) || {
      loaded: false,
      loading: false,
      error: false,
      retryCount: 0
    };
  };

  /**
   * 清除圖片快取
   * @param {string[]} sources - 要清除的圖片來源陣列（可選）
   */
  const clearImageCache = (sources = null) => {
    if (sources) {
      sources.forEach(src => imageStates.delete(src));
    } else {
      imageStates.clear();
    }
  };

  /**
   * 預載入所有成員圖片
   * @param {Object} members - 成員資料
   * @returns {Promise<void>}
   */
  const preloadMemberImages = async (members) => {
    const avatarSources = Object.values(members).map(member => member.avatar_url);
    const bannerSources = Object.values(members).map(member => member.banner_url);
    
    await preloadCriticalImages([...avatarSources, ...bannerSources]);
  };

  return {
    // 狀態
    imageStates,
    isLoading,
    
    // 方法
    loadImage,
    loadImages,
    preloadCriticalImages,
    getImageState,
    clearImageCache,
    preloadMemberImages
  };
}

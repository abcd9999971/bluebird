/**
 * API 管理 Composable
 * 統一管理所有 API 請求和錯誤處理
 */

import { ref } from 'vue';
import { API_ENDPOINTS } from '../utils/constants.js';

/**
 * API 請求管理
 */
export function useApi() {
  // 載入狀態
  const isLoading = ref(false);
  const error = ref(null);

  /**
   * 基礎 API 請求函數
   * @param {string} url - 請求 URL
   * @param {Object} options - 請求選項
   * @returns {Promise<any>} 回應資料
   */
  const apiRequest = async (url, options = {}) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });

      if (!response.ok) {
        throw new Error(`API 請求失敗: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (err) {
      error.value = err.message;
      console.error('API 請求錯誤:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * 獲取成員資料
   * @param {string} baseUrl - API 基礎 URL
   * @returns {Promise<Array>} 成員資料陣列
   */
  const fetchMembers = async (baseUrl = 'http://localhost:8787') => {
    return apiRequest(`${baseUrl}${API_ENDPOINTS.MEMBERS}`);
  };

  /**
   * 獲取推文資料
   * @param {Object} params - 查詢參數
   * @param {string} baseUrl - API 基礎 URL
   * @returns {Promise<Array>} 推文資料陣列
   */
  const fetchTweets = async (params = {}, baseUrl = 'http://localhost:8787') => {
    const searchParams = new URLSearchParams();
    
    Object.entries(params).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        searchParams.append(key, value);
      }
    });

    const url = `${baseUrl}${API_ENDPOINTS.TWEETS}${searchParams.toString() ? `?${searchParams}` : ''}`;
    return apiRequest(url);
  };

  /**
   * 獲取統計資料
   * @param {string} baseUrl - API 基礎 URL
   * @returns {Promise<Object>} 統計資料物件
   */
  const fetchStats = async (baseUrl = 'http://localhost:8787') => {
    return apiRequest(`${baseUrl}${API_ENDPOINTS.STATS}`);
  };

  /**
   * 處理喜歡/取消喜歡
   * @param {Object} likeData - 喜歡資料
   * @param {string} baseUrl - API 基礎 URL
   * @returns {Promise<Object>} 回應資料
   */
  const toggleLike = async (likeData, baseUrl = 'http://localhost:8787') => {
    return apiRequest(`${baseUrl}${API_ENDPOINTS.LIKES}`, {
      method: 'POST',
      body: JSON.stringify(likeData)
    });
  };

  /**
   * 獲取喜歡狀態
   * @param {Object} params - 查詢參數
   * @param {string} baseUrl - API 基礎 URL
   * @returns {Promise<Object>} 喜歡狀態資料
   */
  const fetchLikesStatus = async (params, baseUrl = 'http://localhost:8787') => {
    const searchParams = new URLSearchParams(params);
    const url = `${baseUrl}${API_ENDPOINTS.LIKES_STATUS}?${searchParams}`;
    return apiRequest(url);
  };

  /**
   * 新增推文
   * @param {Object} tweetData - 推文資料
   * @param {string} baseUrl - API 基礎 URL
   * @returns {Promise<Object>} 新增的推文資料
   */
  const createTweet = async (tweetData, baseUrl = 'http://localhost:8787') => {
    return apiRequest(`${baseUrl}${API_ENDPOINTS.TWEETS}`, {
      method: 'POST',
      body: JSON.stringify(tweetData)
    });
  };

  /**
   * 檢查 API 連線狀態
   * @param {string} baseUrl - API 基礎 URL
   * @returns {Promise<boolean>} 連線是否正常
   */
  const checkApiHealth = async (baseUrl = 'http://localhost:8787') => {
    try {
      await apiRequest(`${baseUrl}/api/health`);
      return true;
    } catch {
      return false;
    }
  };

  /**
   * 重試機制
   * @param {Function} fn - 要重試的函數
   * @param {number} maxRetries - 最大重試次數
   * @param {number} delay - 重試延遲（毫秒）
   * @returns {Promise<any>} 函數執行結果
   */
  const withRetry = async (fn, maxRetries = 3, delay = 1000) => {
    let lastError;
    
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await fn();
      } catch (err) {
        lastError = err;
        if (i < maxRetries - 1) {
          await new Promise(resolve => setTimeout(resolve, delay * (i + 1)));
        }
      }
    }
    
    throw lastError;
  };

  return {
    // 狀態
    isLoading,
    error,
    
    // 方法
    apiRequest,
    fetchMembers,
    fetchTweets,
    fetchStats,
    toggleLike,
    fetchLikesStatus,
    createTweet,
    checkApiHealth,
    withRetry
  };
}

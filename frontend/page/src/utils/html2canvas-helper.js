import html2canvas from 'html2canvas';
import { preloadImages, getMemberAvatar } from './assets.js';

// 優化的 html2canvas 配置
const DEFAULT_OPTIONS = {
  scale: 2,
  useCORS: true,
  allowTaint: false,
  backgroundColor: null,
  imageTimeout: 15000,
  logging: false,
  removeContainer: true,
  foreignObjectRendering: false,
  // 確保圖片完全載入
  onclone: (clonedDoc) => {
    // 在克隆的文檔中預載入所有圖片
    const images = clonedDoc.querySelectorAll('img');
    return Promise.all(
      Array.from(images).map(img => {
        if (img.complete) return Promise.resolve();
        return new Promise((resolve) => {
          img.onload = resolve;
          img.onerror = resolve; // 即使載入失敗也繼續
        });
      })
    );
  }
};

// 等待圖片載入的輔助函數
async function waitForImages(container) {
  const images = container.querySelectorAll('img');
  const imagePromises = Array.from(images).map(img => {
    if (img.complete && img.naturalWidth > 0) {
      return Promise.resolve();
    }
    return new Promise((resolve) => {
      img.onload = resolve;
      img.onerror = resolve; // 即使載入失敗也繼續
      // 設置超時
      setTimeout(resolve, 5000);
    });
  });
  
  await Promise.all(imagePromises);
}

// 創建推文截圖容器
export function createTweetCaptureContainer(tweet, author, isDarkMode = false) {
  const container = document.createElement('div');
  
  // 設置容器樣式
  Object.assign(container.style, {
    position: 'absolute',
    top: '-9999px',
    left: '0',
    width: '580px',
    padding: '16px 20px',
    background: isDarkMode ? '#16181c' : '#ffffff',
    fontFamily: 'Noto Sans JP, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    display: 'flex',
    gap: '12px',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
  });
  
  // 獲取本地頭貼路徑
  const avatarSrc = getMemberAvatar(tweet.author_id);
  
  // 設置截圖內容
  container.innerHTML = `
    <img src="${avatarSrc}" style="width:48px; height:48px; border-radius:50%; flex-shrink:0; object-fit:cover;">
    <div style="flex:1; min-width:0;">
      <div style="display:flex; align-items:center; gap:4px; flex-wrap:wrap; margin-bottom:4px;">
        <span style="font-weight:700; color:${isDarkMode ? '#e7e9ea' : '#0f1419'}; font-size:15px;">${tweet.name_ja || author?.name_ja || tweet.author_id}@いきづらい部！</span>
        <span style="color:${isDarkMode ? '#8b98a5' : '#536471'}; font-size:14px;">${author?.id || `@${tweet.author_id}`}</span>
        <span style="color:${isDarkMode ? '#8b98a5' : '#536471'}; font-size:14px;">· ${formatTime(tweet.created_at)}</span>
      </div>
      <p style="white-space:pre-wrap; word-break:break-word; font-size:15px; line-height:1.65; margin:0; color:${isDarkMode ? '#e7e9ea' : '#0f1419'}; font-family:inherit;">${formatContent(tweet.content, isDarkMode)}</p>
    </div>
  `;
  
  return container;
}

// 格式化時間（使用原始資料）
function formatTime(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('ja-JP', { 
    year: 'numeric',
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
}

// 格式化內容，處理 hashtag 顏色
function formatContent(content, isDarkMode = false) {
  return content.replace(/#([\w\u3000-\u9fff\u3040-\u30ff\uff00-\uffef!-]+)/g, 
    `<span style="color: ${isDarkMode ? '#2d9bf0' : '#1d9bf0'}; font-weight: 500;">#$1</span>`
  );
}

// 主要的截圖函數
export async function captureTweetAsImage(tweet, author, isDarkMode = false) {
  try {
    // 預載入所有圖片資源
    await preloadImages();
    
    // 創建截圖容器
    const captureContainer = createTweetCaptureContainer(tweet, author, isDarkMode);
    document.body.appendChild(captureContainer);
    
    // 等待圖片載入
    await waitForImages(captureContainer);
    
    // 生成截圖
    const canvas = await html2canvas(captureContainer, DEFAULT_OPTIONS);
    
    // 清理容器
    if (captureContainer.parentNode) {
      captureContainer.parentNode.removeChild(captureContainer);
    }
    
    return canvas;
  } catch (error) {
    console.error('截圖生成失敗:', error);
    throw error;
  }
}

// 下載截圖
export function downloadCanvasAsImage(canvas, filename) {
  const link = document.createElement('a');
  link.download = filename;
  link.href = canvas.toDataURL('image/png');
  link.click();
}

// 完整的推文分享流程
export async function shareTweetAsImage(tweet, author, isDarkMode = false) {
  try {
    const canvas = await captureTweetAsImage(tweet, author, isDarkMode);
    const filename = `ikidurai-bu-log-${tweet.id}.png`;
    downloadCanvasAsImage(canvas, filename);
    return true;
  } catch (error) {
    console.error('推文分享失敗:', error);
    return false;
  }
}

<template>
  <!-- 載入器組件 - 應用程式初始化時顯示 -->
  <div class="loader">
    <div class="loader-content">
      <!-- L高標誌 -->
      <img src="/assets/images/logos/emblem.png" alt="載入中..." class="loader-image">
      <!-- 動態載入點 -->
      <div class="loader-dots">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
      </div>
    </div>  
  </div>
</template>

<script setup>
/**
 * 載入器組件
 * 在應用程式資料載入完成前顯示的載入動畫
 * 包含 L高標誌和動態載入點效果
 */
</script>

<style scoped>
/* 樣式已還原為能穩定運作的扁平結構 */
.loader {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--bg-primary);
  z-index: 9999;
}

.loader-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.loader-image {
  width: 80px;
}

.loader-dots {
  display: flex;
  gap: 12px;
}

.loader-dots .dot {
  width: 16px;
  height: 16px;
  background-color: var(--brand-color);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loader-dots .dot:nth-child(1) { 
  animation-delay: -0.32s; 
}

.loader-dots .dot:nth-child(2) { 
  animation-delay: -0.16s; 
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.5); opacity: 0.5; }
  40% { transform: scale(1.0); opacity: 1; }
}

</style>
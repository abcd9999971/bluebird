<template>
  <Transition name="fade">
    <button 
      v-if="show"
      class="to-top-btn" 
      @click="scrollToTop"
      title="回到頂部"
    >
      <span class="icon">keyboard_arrow_up</span>
    </button>
  </Transition>
</template>

<script setup>
// 這個組件接收一個名為 'show' 的 prop 來控制其顯示與否
defineProps({
  show: {
    type: Boolean,
    required: true
  }
});

// 按鈕自己的點擊邏輯
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};
</script>

<style scoped>
/* 淡入淡出動畫 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 從 assets/styles.css 搬移過來的樣式 */
.to-top-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  border: none;
  border-radius: 50%;
  background: var(--brand-color);
  color: var(--text-on-brand);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  z-index: 100;
  cursor: pointer;
}

.to-top-btn:hover {
  transform: scale(1.1);
  box-shadow: var(--shadow-lg);
}

/* 手機版位置微調 */
@media (max-width: 768px) {
  .to-top-btn { 
    bottom: 80px; 
  }
}

/* 更小螢幕位置微調 */
@media (max-width: 480px) {
  .to-top-btn { 
    bottom: 110px; 
  }
}
</style>
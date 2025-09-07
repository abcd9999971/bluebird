<template>
  <!-- Toast 通知 -->
  <div v-if="toast.show" class="toast" :class="toast.type">
    {{ toast.message }}
  </div>
</template>

<script setup>
// 定義 props - 從父組件接收的資料
const props = defineProps({
  toast: Object
});
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--bg-secondary);
  color: var(--text-primary);
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  z-index: 1000;
  border: 1px solid var(--border-primary);
}

.toast.success {
  border-color: var(--share-green);
  background-color: color-mix(in srgb, var(--share-green) 10%, var(--bg-secondary));
}

.toast.error {
  border-color: var(--accent-pink);
  background-color: color-mix(in srgb, var(--accent-pink) 10%, var(--bg-secondary));
}

.toast.warning {
  border-color: #f39c12;
  background-color: color-mix(in srgb, #f39c12 10%, var(--bg-secondary));
}

/* 手機版樣式 */
@media (max-width: 768px) {
  .toast {
    bottom: 80px;
    left: 10px;
    right: 10px;
    transform: none;
    max-width: none;
  }
}
</style>

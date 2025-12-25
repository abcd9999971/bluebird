<template>
  <!-- 時間軸標題 -->
  <header class="timeline-header">
    <!-- 標題文字 -->
    <h1>{{ headerTitle }}</h1>
  </header>
</template>

<script setup>
// 定義 props - 從父組件接收的資料
const props = defineProps({
  headerTitle: String
});
</script>

<style scoped>
.timeline-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 58px;
  backdrop-filter: blur(12px);
}

h1 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  flex: 1;
  text-align: center;
}

/* 桌面版樣式 */
@media (min-width: 769px) {
  h1 {
    text-align: left;
  }
}

/* 手機版樣式 */
@media (max-width: 768px) {
  .timeline-header {
    padding: calc(var(--spacing-unit) * 0.75);
  }
  
  h1 {
    font-size: 1.1rem;
  }
}
</style>

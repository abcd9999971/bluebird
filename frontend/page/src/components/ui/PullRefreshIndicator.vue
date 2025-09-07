<template>
  <!-- 下拉刷新指示器 -->
  <div 
    v-if="visible" 
    class="pull-refresh-indicator"
    :style="{ 
      transform: `translateY(${pullDistance}px)`,
      opacity: Math.min(pullDistance / 80, 1)
    }"
  >
    <div class="pull-refresh-content">
      <div class="pull-refresh-icon" :class="{ spinning: isRefreshing }">
        <span class="icon">{{ isRefreshing ? 'refresh' : 'keyboard_arrow_down' }}</span>
      </div>
      <div class="pull-refresh-text">
        {{ isRefreshing ? '正在刷新...' : (pullDistance >= 80 ? '釋放以刷新' : '下拉刷新') }}
      </div>
    </div>
  </div>
</template>

<script setup>
// 定義 props
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  pullDistance: {
    type: Number,
    default: 0
  },
  isRefreshing: {
    type: Boolean,
    default: false
  }
});
</script>

<style scoped>
.pull-refresh-indicator {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  transition: all 0.2s ease-out;
  transform-origin: top;
}

.pull-refresh-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-unit) 0;
  gap: calc(var(--spacing-unit) / 2);
}

.pull-refresh-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: var(--bg-tertiary);
  transition: transform 0.2s ease-out;
}

.pull-refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

.pull-refresh-icon .icon {
  font-size: 20px;
  color: var(--text-secondary);
}

.pull-refresh-text {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* 手機版專用 */
@media (min-width: 769px) {
  .pull-refresh-indicator {
    display: none;
  }
}
</style>

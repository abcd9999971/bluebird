<template>
  <!-- 時間軸標題 -->
  <header class="timeline-header">
    <div class="header-top">
      <h1>{{ headerTitle }}</h1>
    </div>
    
    <!-- View Switcher Tabs -->
    <div class="header-tabs">
      <button 
        class="tab-btn" 
        :class="{ active: viewMode === 'list' }"
        @click="$emit('update:viewMode', 'list')"
      >
        <span>Tweets</span>
        <div class="tab-indicator"></div>
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: viewMode === 'media' }"
        @click="$emit('update:viewMode', 'media')"
      >
        <span>Media</span>
        <div class="tab-indicator"></div>
      </button>
    </div>
  </header>
</template>

<script setup>
const props = defineProps({
  headerTitle: String,
  viewMode: {
    type: String,
    default: 'list'
  }
});

const emit = defineEmits(['update:viewMode', 'focusSearch', 'toggleMobileSearch', 'openDateNavigationModal', 'onSearchBlur', 'toggleTheme']);
</script>

<style scoped>
.timeline-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--glass-bg);
  border-bottom: var(--glass-border);
  display: flex;
  flex-direction: column;
  backdrop-filter: var(--glass-backdrop);
  padding: 0;
}

.header-top {
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

h1 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.header-tabs {
  display: flex;
  width: 100%;
}

.tab-btn {
  flex: 1;
  background: transparent;
  border: none;
  padding: var(--spacing-unit) 0;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  position: relative;
  transition: color 0.2s;
}

.tab-btn:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.tab-btn.active {
  color: var(--text-primary);
}

.tab-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 4px;
  background-color: var(--brand-color);
  border-radius: 4px 4px 0 0;
  opacity: 0;
  transition: opacity 0.2s;
}

.tab-btn.active .tab-indicator {
  opacity: 1;
}

/* 桌面版樣式 */
@media (min-width: 769px) {
  .header-top {
    justify-content: flex-start;
  }
}

/* 手機版樣式 */
@media (max-width: 768px) {
  h1 {
    font-size: 1.1rem;
  }
}
</style>

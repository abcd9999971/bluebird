<template>
  <!-- 右側邊欄 -->
  <aside class="sidebar-right">
    <div class="date-navigator">
      <!-- 日期導航器標題 -->
      <div class="date-navigator-header">
        <h3>{{ t('quick_scroll_title') }}</h3>
      </div>
      
      <div class="date-navigator-controls">
        <!-- 年份選擇器 -->
        <div class="year-scroller">
          <div class="switcher-row">
            <button 
              v-for="year in availableYears" 
              :key="year"
              class="switcher-btn" 
              :class="{ active: filters.year === year }"
              @click="setYear(year)"
            >
              {{ year }}
            </button>
          </div>
        </div>

        <!-- 月份選擇器 -->
        <div v-if="filters.year" class="month-grid">
          <button 
            v-for="month in 12" 
            :key="month"
            class="switcher-btn" 
            :class="{ active: filters.month === month }"
            @click="setMonthFilter(month)"
            :disabled="!availableMonths.includes(month)"
          >
            {{ month }}{{ t('month_unit') }}
          </button>
        </div>

        <!-- 日期列表 -->
        <div class="date-list">
          <div 
            v-for="dateGroup in dateGroups" 
            :key="dateGroup.date"
            class="date-list-item"
            :class="{ active: scroller.activeDate === dateGroup.date }"
            @click="scrollToDate(dateGroup.firstTweetId)"
          >
            <span>{{ formatDateForScroller(dateGroup.date) }}</span>
            <span class="date-count">{{ dateGroup.count }}</span>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
// 定義 props - 從父組件接收的資料
const props = defineProps({
  filters: Object,
  availableYears: Array,
  availableMonths: Array,
  dateGroups: Array,
  scroller: Object
});

// 定義 emits - 向父組件發送的事件
const emit = defineEmits([
  'setYear',
  'setMonthFilter',
  'scrollToDate'
]);

// 翻譯函數 - 獲取多語言文字
const t = (key) => {
  const translations = {
    'ja': { 
      quick_scroll_title: '日付で移動',
      month_unit: '月'
    }
  };
  return translations['ja']?.[key] || key;
};

// 日期格式化 - 為日期滾動器格式化日期
const formatDateForScroller = (dateString) => new Intl.DateTimeFormat('ja-JP', { 
  month: 'long', 
  day: 'numeric' 
}).format(new Date(dateString));

// 事件處理函數 - 設定年份
const setYear = (year) => emit('setYear', year);

// 事件處理函數 - 設定月份篩選
const setMonthFilter = (month) => emit('setMonthFilter', month);

// 事件處理函數 - 滾動到指定日期
const scrollToDate = (tweetId) => emit('scrollToDate', tweetId);
</script>

<style scoped>
.sidebar-right {
  width: var(--sidebar-width);
  padding: calc(var(--spacing-unit) * 2);
  position: sticky;
  top: 0;
  height: 100vh;
  backdrop-filter: blur(12px);
}

.date-navigator {
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.date-navigator-header {
  padding: var(--spacing-unit);
  border-bottom: 1px solid var(--border-primary);
  background-color: var(--bg-primary);
}

.date-navigator-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.date-navigator-controls {
  padding: var(--spacing-unit);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.year-scroller {
  margin-bottom: var(--spacing-unit);
}

.switcher-row {
  display: flex;
  flex-wrap: wrap;
  gap: calc(var(--spacing-unit) / 4);
}

.switcher-btn {
  padding: calc(var(--spacing-unit) * 0.4) calc(var(--spacing-unit) * 0.6);
  border: 1px solid var(--border-primary);
  border-radius: calc(var(--border-radius) / 2);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-duration) ease;
  font-size: 0.9rem;
  min-width: 44px;
  text-align: center;
}

.switcher-btn:hover {
  background-color: var(--bg-hover);
}

.switcher-btn.active {
  background-color: var(--brand-color);
  color: white;
  border-color: var(--brand-color);
}

.switcher-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  background-color: var(--bg-secondary);
}

.month-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: calc(var(--spacing-unit) / 4);
  margin-bottom: var(--spacing-unit);
}

.date-list {
  flex: 1;
  overflow-y: auto;
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  min-height: 0;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.date-list::-webkit-scrollbar {
  display: none;
}

.date-list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: calc(var(--spacing-unit) * 0.5) calc(var(--spacing-unit) * 0.75);
  cursor: pointer;
  transition: background-color var(--transition-duration) ease;
  border-bottom: 1px solid var(--border-primary);
  font-size: 0.9rem;
}

.date-list-item:last-child {
  border-bottom: none;
}

.date-list-item:hover {
  background-color: var(--bg-hover);
}

.date-list-item.active {
  background-color: color-mix(in srgb, var(--brand-color) 10%, transparent);
  color: var(--brand-color);
}

.date-count {
  background-color: var(--bg-secondary);
  color: var(--text-secondary);
  padding: calc(var(--spacing-unit) * 0.2) calc(var(--spacing-unit) * 0.4);
  border-radius: calc(var(--border-radius) / 2);
  font-size: 0.8rem;
  min-width: 20px;
  text-align: center;
}

.date-list-item.active .date-count {
  background-color: var(--brand-color);
  color: white;
}

/* 平板版隱藏 */
@media (max-width: 1024px) {
  .sidebar-right {
    display: none;
  }
}
</style>

<template>
  <!-- 手機版日期導航 Modal -->
  <div v-if="ui.dateNavModal" class="modal" :class="{ show: ui.dateNavModal }">
    <div class="modal-header">
      <h3>{{ t('quick_scroll_title') }}</h3>
      <button class="modal-close-btn" @click="closeModal">&times;</button>
    </div>
    <div class="modal-content">
      <div class="date-navigator">
        <div class="date-navigator-controls">
          <!-- 年份選擇器 -->
          <div class="year-scroller">
            <div class="switcher-row">
              <button 
                v-for="year in availableYears" 
                :key="year" 
                class="switcher-btn" 
                :class="{ active: year === filters.year }" 
                @click="setYear(year)"
              >
                {{ year }}
              </button>
            </div>
          </div>
          
          <!-- 月份選擇器 -->
          <div class="month-grid">
            <button 
              v-for="month in 12" 
              :key="month" 
              class="switcher-btn" 
              :class="{ active: month === filters.month }" 
              @click="setMonthFilter(month)" 
              :disabled="!availableMonths.includes(month)"
            >
              {{ month }}{{ t('month_unit') }}
            </button>
          </div>
        </div>
        
        <!-- 日期列表 -->
        <div class="date-list">
          <div v-if="dateGroups.length > 0">
            <div 
              v-for="group in dateGroups" 
              :key="group.date" 
              class="date-list-item" 
              :class="{ active: group.date === scroller.activeDate }" 
              @click="scrollToDateAndClose(group.firstTweetId)"
            >
              <span>{{ formatDateForScroller(group.date) }}</span>
              <span class="date-count">{{ group.count }}</span>
            </div>
          </div>
          <div v-else class="empty-state">
            {{ t('no_tweets_for_year') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 定義 props - 從父組件接收的資料
const props = defineProps({
  ui: Object,
  filters: Object,
  availableYears: Array,
  availableMonths: Array,
  dateGroups: Array,
  scroller: Object
});

// 定義 emits - 向父組件發送的事件
const emit = defineEmits([
  'closeModal',
  'setYear',
  'setMonthFilter',
  'scrollToDate'
]);

// 翻譯函數 - 獲取多語言文字
const t = (key) => {
  const translations = {
    'ja': { 
      quick_scroll_title: '日付で移動',
      month_unit: '月',
      no_tweets_for_year: 'その期間には日誌がありません'
    }
  };
  return translations['ja']?.[key] || key;
};

// 日期格式化 - 為日期滾動器格式化日期
const formatDateForScroller = (dateString) => new Intl.DateTimeFormat('ja-JP', { 
  month: 'long', 
  day: 'numeric' 
}).format(new Date(dateString));

// 事件處理函數 - 關閉彈窗
const closeModal = () => emit('closeModal');

// 事件處理函數 - 設定年份
const setYear = (year) => emit('setYear', year);

// 事件處理函數 - 設定月份篩選
const setMonthFilter = (month) => emit('setMonthFilter', month);

// 事件處理函數 - 滾動到日期並關閉彈窗
const scrollToDateAndClose = (tweetId) => {
  emit('scrollToDate', tweetId);
  emit('closeModal');
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--border-radius);
  max-width: 500px;
  width: 90vw;
  max-height: 80vh;
  overflow: hidden;
  z-index: 1001;
  opacity: 0;
  transition: opacity var(--transition-duration) ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal.show {
  opacity: 1;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-unit);
  border-bottom: 1px solid var(--border-primary);
  background-color: var(--bg-secondary);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
}

.modal-close-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  background-color: var(--bg-hover);
  color: var(--text-primary);
  cursor: pointer;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color var(--transition-duration) ease;
}

.modal-close-btn:hover {
  background-color: color-mix(in srgb, var(--text-primary) 10%, transparent);
}

.modal-content {
  padding: var(--spacing-unit);
  overflow-y: auto;
  max-height: calc(80vh - 80px);
}

.date-navigator {
  border: none;
  border-radius: 0;
  height: auto;
}

.date-navigator-controls {
  margin-bottom: var(--spacing-unit);
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
}

.date-list {
  max-height: 50vh;
  overflow-y: auto;
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
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

.empty-state {
  padding: var(--spacing-unit);
  text-align: center;
  color: var(--text-secondary);
}

/* 手機版樣式 */
@media (max-width: 768px) {
  .modal {
    width: 95vw;
    max-height: 90vh;
  }
  
  .modal-header {
    padding: calc(var(--spacing-unit) * 0.75);
  }
  
  .modal-header h3 {
    font-size: 1.1rem;
  }
  
  .modal-content {
    padding: calc(var(--spacing-unit) * 0.75);
  }
}

/* 桌面版隱藏 */
@media (min-width: 769px) {
  .modal {
    display: none;
  }
}
</style>

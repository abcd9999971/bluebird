<template>
  <!-- 時間軸裝飾桿 -->
  <div class="timeline-bar" :style="{ '--timeline-bar-color': brandColor }">
    <div class="timeline-bar-line"></div>
    <div class="timeline-bar-nodes">
      <!-- 根據推文密度動態分佈的節點 -->
      <div 
        v-for="node in nodesWithPosition" 
        :key="node.date" 
        class="timeline-bar-node"
        :class="{ active: isActive(node.date) }"
        :style="{ top: node.position }"
      >
        <div class="node-dot" :style="{ transform: `scale(${node.scale})` }"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

/**
 * Props 定義 - 從父組件接收的資料
 */
const props = defineProps({
  dateGroups: {           // 日期分組資料，包含日期和推文數量
    type: Array,
    default: () => []
  },
  activeDate: {           // 當前活動日期，用於高亮顯示
    type: String,
    default: null
  },
  brandColor: {           // 當前品牌顏色，根據選擇的成員動態變化
    type: String,
    default: 'var(--brand-blue)'
  }
});

/**
 * 檢查日期是否為當前活動日期
 * @param {string} date - 要檢查的日期
 * @returns {boolean} 是否為活動日期
 */
const isActive = (date) => {
  if (!props.activeDate) return false;
  
  // 如果是月份分組模式，檢查活動日期是否屬於該月份
  if (date.includes('-') && date.length === 7) { // 月份格式：YYYY-MM
    const activeDate = new Date(props.activeDate);
    const nodeDate = new Date(date + '-01'); // 轉換為月份第一天
    
    return activeDate.getFullYear() === nodeDate.getFullYear() && 
           activeDate.getMonth() === nodeDate.getMonth();
  }
  
  // 一般日期比較
  return props.activeDate === date;
};

/**
 * 根據節點壅擠度動態計算節點位置和大小的計算屬性
 * 
 * 核心演算法：
 * 1. 當節點數量過多造成壅擠時，自動切換為月份顯示模式
 * 2. 推文數量多的日期會佔據更多垂直空間，形成密集區域
 * 3. 推文數量少的日期會被擠壓，形成稀疏區域
 * 4. 節點大小與推文數量成正比，提供視覺層次感
 * 5. 時間軸順序：新日期在上方，舊日期在下方
 * 6. 月份分組時，節點會亮起對應的月份範圍
 */
const nodesWithPosition = computed(() => {
  if (!props.dateGroups.length) return [];
  
  // 按日期從新到舊排序（最新的推文顯示在時間軸頂部）
  const sortedGroups = [...props.dateGroups].sort((a, b) => new Date(b.date) - new Date(a.date));
  
  // 計算總推文數量，用於比例分配
  const totalTweets = sortedGroups.reduce((sum, group) => sum + group.count, 0);
  if (totalTweets === 0) return [];
  
  // 節點壅擠度計算：基於時間軸高度和節點密度的動態閾值
  const containerHeight = 90; // 容器可用高度百分比
  const minNodeSpacing = 2; // 最小節點間距百分比
  const maxNodesForContainer = Math.floor(containerHeight / minNodeSpacing);
  
  // 當節點數量超過容器容量時，切換為月份顯示
  const shouldGroupByMonth = sortedGroups.length > maxNodesForContainer;
  
  let processedGroups;
  
  if (shouldGroupByMonth) {
    // 按月份分組
    const monthGroups = {};
    sortedGroups.forEach(group => {
      const date = new Date(group.date);
      const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
      
      if (!monthGroups[monthKey]) {
        monthGroups[monthKey] = {
          date: monthKey,
          count: 0,
          displayDate: `${date.getFullYear()}年${date.getMonth() + 1}月`,
          originalDates: [] // 儲存該月份的所有原始日期
        };
      }
      monthGroups[monthKey].count += group.count;
      monthGroups[monthKey].originalDates.push(group.date);
    });
    
    processedGroups = Object.values(monthGroups).sort((a, b) => new Date(b.date) - new Date(a.date));
  } else {
    processedGroups = sortedGroups;
  }
  
  // 累積高度追蹤器
  let accumulatedHeight = 0;
  
  return processedGroups.map((group) => {
    // 基於推文數量計算該日期在時間軸上應佔的高度比例
    const heightRatio = group.count / totalTweets;
    const segmentHeight = heightRatio * containerHeight;
    
    // 節點定位在該段的垂直中心點
    const position = `${accumulatedHeight + segmentHeight / 2 + 5}%`; // 5% 頂部邊距
    
    // 動態節點縮放：根據該日期的推文數量相對於最大推文數量的比例
    const maxCount = Math.max(...processedGroups.map(g => g.count));
    const scale = Math.max(0.8, Math.min(1.5, 0.8 + (group.count / maxCount) * 0.7));
    
    // 更新累積高度，為下一個節點做準備
    accumulatedHeight += segmentHeight;
    
    return {
      ...group,
      position,
      scale,
      isMonthGroup: shouldGroupByMonth
    };
  });
});
</script>

<style scoped>
/* 時間軸裝飾桿樣式 */
.timeline-bar {
  width: 80px; /* 裝飾桿寬度 */
  height: 100vh; /* 佔滿整個視窗高度 */
  position: sticky;
  top: 0;
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  padding: var(--spacing-lg) 0;
  --timeline-bar-color: var(--brand-blue); /* 預設顏色 */
}

/* 中心線 - 加粗並增加漸層效果 */
.timeline-bar-line {
  width: 6px;
  height: 100%;
  background: linear-gradient(180deg, 
    transparent 0%, 
    color-mix(in srgb, var(--timeline-bar-color) 30%, transparent) 10%,
    var(--timeline-bar-color) 50%,
    color-mix(in srgb, var(--timeline-bar-color) 30%, transparent) 90%,
    transparent 100%
  );
  border-radius: var(--radius-full);
  box-shadow: 0 0 8px color-mix(in srgb, var(--timeline-bar-color) 20%, transparent);
}

/* 節點容器 */
.timeline-bar-nodes {
  position: absolute;
  top: var(--spacing-lg);
  left: 50%;
  transform: translateX(-50%);
  height: calc(100% - calc(var(--spacing-lg) * 2));
  width: 100%;
}

/* 單一節點 - 使用絕對定位實現動態密度分佈 */
.timeline-bar-node {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  transition: var(--transition-standard);
  opacity: 0.7;
}

/* 節點圓點 - 美化並增大 */
.node-dot {
  width: 16px;
  height: 16px;
  background-color: var(--bg-secondary);
  border: 4px solid var(--timeline-bar-color);
  border-radius: 50%;
  transition: var(--transition-standard);
  box-shadow: var(--shadow-2);
  cursor: pointer;
}

/* 滑鼠懸停在節點上時的樣式 */
.timeline-bar-node:hover {
  opacity: 1;
  transform: translateX(-50%) translateY(-2px);
}

.timeline-bar-node:hover .node-dot {
  transform: scale(1.2);
  box-shadow: var(--shadow-3);
}

/* 當前活動節點的樣式 */
.timeline-bar-node.active {
  opacity: 1;
  transform: translateX(-50%) translateY(-2px);
}

.timeline-bar-node.active .node-dot {
  background-color: var(--timeline-bar-color);
  border-color: var(--timeline-bar-color);
  box-shadow: 0 0 12px 3px color-mix(in srgb, var(--timeline-bar-color) 40%, transparent);
  transform: scale(1.3);
}

/* 手機版隱藏時間軸 */
@media (max-width: 1200px) {
  .timeline-bar {
    display: none;
  }
}
</style>
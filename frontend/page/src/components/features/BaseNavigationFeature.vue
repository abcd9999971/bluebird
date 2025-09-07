<template>
  <div class="navigation-feature">
    <!-- 主題切換按鈕 -->
    <button 
      class="theme-toggle"
      :class="{ 'active': isDark }"
      :title="toggleTitle"
      @click="toggleTheme"
    >
      <span class="icon">{{ currentIcon }}</span>
      <span v-if="showLabel" class="label">{{ currentLabel }}</span>
    </button>

    <!-- 重置篩選按鈕 -->
    <button 
      class="reset-filters-btn"
      :title="t('reset_all_filters')"
      @click="resetFilters"
    >
      <span class="icon">refresh</span>
      <span v-if="showLabel" class="label">{{ t('reset') }}</span>
    </button>

    <!-- 日期導航按鈕（手機版） -->
    <button 
      v-if="isMobile"
      class="date-nav-btn"
      :title="t('date_navigation')"
      @click="openDateNavigation"
    >
      <span class="icon">calendar_month</span>
      <span v-if="showLabel" class="label">{{ t('date_nav') }}</span>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

/**
 * 導航功能組件
 * 統一的導航功能，包含主題切換、重置篩選、日期導航等
 * 支援桌面版和手機版不同顯示
 */

// Props 定義
const props = defineProps({
  isDark: {
    type: Boolean,
    default: false
  },
  isMobile: {
    type: Boolean,
    default: false
  },
  showLabel: {
    type: Boolean,
    default: false
  },
  size: {
    type: String,
    default: 'medium', // small, medium, large
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
});

// Emits 定義
const emit = defineEmits(['toggle-theme', 'reset-filters', 'open-date-nav']);

// 國際化
const { t } = useI18n();

// 計算屬性
const currentIcon = computed(() => 
  props.isDark ? 'light_mode' : 'dark_mode'
);

const currentLabel = computed(() => 
  props.isDark ? t('light_theme') : t('dark_theme')
);

const toggleTitle = computed(() => 
  props.isDark ? t('switch_to_light') : t('switch_to_dark')
);

// 方法
const toggleTheme = () => {
  emit('toggle-theme');
};

const resetFilters = () => {
  emit('reset-filters');
};

const openDateNavigation = () => {
  emit('open-date-nav');
};
</script>

<style scoped>
.navigation-feature {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing-unit) * 0.5);
}

/* 主題切換按鈕 */
.theme-toggle {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.5);
  padding: calc(var(--spacing-unit) * 0.75);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition-fast);
  font-family: inherit;
  font-size: 0.9rem;
  width: 100%;
  justify-content: flex-start;
}

.theme-toggle:hover {
  background-color: var(--bg-hover);
  border-color: var(--brand-color);
}

.theme-toggle.active {
  background-color: color-mix(in srgb, var(--brand-color) 10%, var(--bg-primary));
  border-color: var(--brand-color);
  color: var(--brand-color);
}

.theme-toggle .icon {
  font-family: 'Material Symbols Outlined';
  font-size: 18px;
  line-height: 1;
  transition: var(--transition-fast);
}

.theme-toggle .label {
  font-weight: 500;
}

/* 重置篩選按鈕 */
.reset-filters-btn {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.5);
  padding: calc(var(--spacing-unit) * 0.75);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition-fast);
  font-family: inherit;
  font-size: 0.9rem;
  width: 100%;
  justify-content: flex-start;
}

.reset-filters-btn:hover {
  background-color: var(--bg-hover);
  border-color: var(--brand-color);
}

.reset-filters-btn .icon {
  font-family: 'Material Symbols Outlined';
  font-size: 18px;
  line-height: 1;
}

.reset-filters-btn .label {
  font-weight: 500;
}

/* 日期導航按鈕 */
.date-nav-btn {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 0.5);
  padding: calc(var(--spacing-unit) * 0.75);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition-fast);
  font-family: inherit;
  font-size: 0.9rem;
  width: 100%;
  justify-content: flex-start;
}

.date-nav-btn:hover {
  background-color: var(--bg-hover);
  border-color: var(--brand-color);
}

.date-nav-btn .icon {
  font-family: 'Material Symbols Outlined';
  font-size: 18px;
  line-height: 1;
}

.date-nav-btn .label {
  font-weight: 500;
}

/* 尺寸變體 */
.navigation-feature.size-small button {
  padding: calc(var(--spacing-unit) * 0.5);
  font-size: 0.8rem;
}

.navigation-feature.size-small .icon {
  font-size: 16px;
}

.navigation-feature.size-large button {
  padding: var(--spacing-unit);
  font-size: 1rem;
}

.navigation-feature.size-large .icon {
  font-size: 20px;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .navigation-feature {
    flex-direction: row;
    gap: var(--spacing-unit);
  }
  
  .navigation-feature button {
    flex: 1;
    justify-content: center;
  }
  
  .navigation-feature .label {
    display: none;
  }
}

/* 橫向布局（桌面版） */
@media (min-width: 769px) {
  .navigation-feature.horizontal {
    flex-direction: row;
    gap: var(--spacing-unit);
  }
  
  .navigation-feature.horizontal button {
    flex: 1;
    justify-content: center;
  }
}
</style>

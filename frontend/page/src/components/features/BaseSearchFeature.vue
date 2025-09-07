<template>
  <div class="search-feature">
    <!-- 桌面版搜尋 -->
    <div v-if="!isMobile" class="desktop-search">
      <div class="search-container">
        <input
          ref="desktopSearchInput"
          v-model="searchValue"
          type="text"
          :placeholder="t('search_placeholder')"
          class="search-input"
          @blur="handleBlur"
          @keyup.enter="handleSubmit"
          @input="handleInput"
        />
        <button 
          v-if="searchValue"
          class="search-clear-btn"
          @click="clearSearch"
        >
          <span class="icon">clear</span>
        </button>
      </div>
    </div>

    <!-- 手機版搜尋 -->
    <div v-else class="mobile-search">
      <div v-if="showMobileSearch" class="mobile-search-container">
        <div class="mobile-search-box">
          <input
            ref="mobileSearchInput"
            v-model="searchValue"
            type="text"
            :placeholder="t('search_placeholder')"
            class="mobile-search-input"
            @blur="handleBlur"
            @keyup.enter="handleSubmit"
            @input="handleInput"
          />
          <button 
            class="mobile-search-close"
            @click="closeMobileSearch"
          >
            <span class="icon">close</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';

/**
 * 搜尋功能組件
 * 統一的搜尋功能，支援桌面版和手機版
 * 整合搜尋輸入、清除、提交等所有搜尋相關功能
 */

// Props 定義
const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  isMobile: {
    type: Boolean,
    default: false
  },
  showMobileSearch: {
    type: Boolean,
    default: false
  }
});

// Emits 定義
const emit = defineEmits([
  'update:modelValue',
  'submit',
  'blur',
  'clear',
  'input',
  'toggle-mobile-search'
]);

// 響應式變數
const desktopSearchInput = ref(null);
const mobileSearchInput = ref(null);

// 計算屬性
const searchValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

// 國際化
const { t } = useI18n();

// 方法
const handleBlur = () => {
  emit('blur');
};

const handleSubmit = () => {
  emit('submit', searchValue.value);
  emit('blur');
};

const handleInput = () => {
  emit('input', searchValue.value);
};

const clearSearch = () => {
  searchValue.value = '';
  emit('clear');
  nextTick(() => {
    desktopSearchInput.value?.focus();
  });
};

const closeMobileSearch = () => {
  emit('toggle-mobile-search');
};

const focusSearch = () => {
  if (props.isMobile) {
    emit('toggle-mobile-search');
    nextTick(() => {
      mobileSearchInput.value?.focus();
    });
  } else {
    nextTick(() => {
      desktopSearchInput.value?.focus();
    });
  }
};

// 暴露方法給父組件
defineExpose({
  focusSearch
});
</script>

<style scoped>
.search-feature {
  width: 100%;
}

/* 桌面版搜尋樣式 */
.desktop-search {
  width: 100%;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: calc(var(--spacing-unit) * 0.75);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-size: 1rem;
  font-family: inherit;
  outline: none;
  transition: var(--transition-fast);
}

.search-input:focus {
  border-color: var(--brand-color);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--brand-color) 20%, transparent);
}

.search-input::placeholder {
  color: var(--text-secondary);
}

.search-clear-btn {
  position: absolute;
  right: calc(var(--spacing-unit) * 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 50%;
  transition: var(--transition-fast);
}

.search-clear-btn:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.search-clear-btn .icon {
  font-family: 'Material Symbols Outlined';
  font-size: 16px;
  line-height: 1;
}

/* 手機版搜尋樣式 */
.mobile-search {
  width: 100%;
}

.mobile-search-container {
  position: sticky;
  top: 58px;
  z-index: 9;
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  padding: var(--spacing-unit);
  backdrop-filter: blur(12px);
}

.mobile-search-box {
  display: flex;
  align-items: center;
  gap: var(--spacing-unit);
  background-color: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  padding: calc(var(--spacing-unit) * 0.5);
  transition: var(--transition-fast);
}

.mobile-search-box:focus-within {
  border-color: var(--brand-color);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--brand-color) 20%, transparent);
}

.mobile-search-input {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 1rem;
  padding: calc(var(--spacing-unit) * 0.5);
  outline: none;
  font-family: inherit;
}

.mobile-search-input::placeholder {
  color: var(--text-secondary);
}

.mobile-search-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 50%;
  transition: var(--transition-fast);
}

.mobile-search-close:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.mobile-search-close .icon {
  font-family: 'Material Symbols Outlined';
  font-size: 20px;
  line-height: 1;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .desktop-search {
    display: none;
  }
}

@media (min-width: 769px) {
  .mobile-search {
    display: none;
  }
}
</style>

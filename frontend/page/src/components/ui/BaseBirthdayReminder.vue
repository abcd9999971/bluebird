<template>
  <!-- 生日提醒橫幅 -->
  <div v-if="showReminder" class="birthday-reminder">
    <div class="birthday-content">
      <div class="birthday-icon">
        <span class="icon">cake</span>
      </div>
      <div class="birthday-text">
        <div class="birthday-title">{{ t('birthday_title') }}</div>
        <div class="birthday-message">
          {{ t('birthday_message', { name: birthdayMember.name_ja }) }}
        </div>
      </div>
      <button class="birthday-close" @click="closeReminder">
        <span class="icon">close</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue';

// 定義 props
const props = defineProps({
  authors: {
    type: Object,
    default: () => ({})
  }
});

// 定義 emits
const emit = defineEmits(['close']);

// 響應式變數
const showReminder = ref(false);
const dismissedMembers = ref(new Set());

// 翻譯函數
const t = (key, params = {}) => {
  const translations = {
    'ja': {
      birthday_title: '🎉 お誕生日おめでとう！',
      birthday_message: '{name} さんのお誕生日です！'
    }
  };
  
  let message = translations['ja']?.[key] || key;
  
  // 替換參數
  Object.keys(params).forEach(param => {
    message = message.replace(`{${param}}`, params[param]);
  });
  
  return message;
};

// 檢查今天是否有成員生日
const birthdayMember = computed(() => {
  const today = new Date();
  const currentMonth = today.getMonth() + 1; // getMonth() 返回 0-11
  const currentDay = today.getDate();
  
  // 格式化為 "M月D日" 格式
  const todayString = `${currentMonth}月${currentDay}日`;
  
  // 查找今天生日的成員
  for (const [memberId, member] of Object.entries(props.authors)) {
    if (member.birthday === todayString && !dismissedMembers.value.has(memberId)) {
      return member;
    }
  }
  
  return null;
});

// 檢查是否應該顯示提醒
const shouldShowReminder = () => {
  return birthdayMember.value !== null && !showReminder.value;
};

// 關閉提醒
const closeReminder = () => {
  if (birthdayMember.value) {
    dismissedMembers.value.add(birthdayMember.value.id);
  }
  showReminder.value = false;
  emit('close');
};

// 檢查並顯示生日提醒
const checkBirthday = () => {
  if (shouldShowReminder()) {
    showReminder.value = true;
    
    // 5秒後自動關閉
    setTimeout(() => {
      closeReminder();
    }, 5000);
  }
};

// 生命週期
onMounted(() => {
  // 延遲檢查，確保資料已載入
  setTimeout(checkBirthday, 1000);
});

// 監聽成員資料變化
watch(() => props.authors, () => {
  if (Object.keys(props.authors).length > 0) {
    checkBirthday();
  }
}, { deep: true });
</script>

<style scoped>
.birthday-reminder {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 200;
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  animation: birthday-slide-down 0.5s ease-out;
}

.birthday-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-unit);
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
  max-width: var(--main-max-width);
  margin: 0 auto;
}

.birthday-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  flex-shrink: 0;
}

.birthday-icon .icon {
  font-size: 24px;
  color: white;
}

.birthday-text {
  flex: 1;
  min-width: 0;
}

.birthday-title {
  font-weight: 700;
  font-size: 1rem;
  margin-bottom: 2px;
}

.birthday-message {
  font-size: 0.9rem;
  opacity: 0.9;
}

.birthday-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  color: white;
  cursor: pointer;
  transition: var(--transition-fast);
  flex-shrink: 0;
}

.birthday-close:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.birthday-close .icon {
  font-size: 18px;
}

/* 動畫 */
@keyframes birthday-slide-down {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* 手機版樣式 */
@media (max-width: 768px) {
  .birthday-content {
    padding: calc(var(--spacing-unit) * 0.75) var(--spacing-unit);
  }
  
  .birthday-icon {
    width: 32px;
    height: 32px;
  }
  
  .birthday-icon .icon {
    font-size: 20px;
  }
  
  .birthday-title {
    font-size: 0.9rem;
  }
  
  .birthday-message {
    font-size: 0.8rem;
  }
  
  .birthday-close {
    width: 28px;
    height: 28px;
  }
  
  .birthday-close .icon {
    font-size: 16px;
  }
}

/* 橫屏模式調整 */
@media (max-width: 768px) and (orientation: landscape) {
  .birthday-reminder {
    position: relative;
  }
  
  .birthday-content {
    padding: calc(var(--spacing-unit) * 0.5) var(--spacing-unit);
  }
  
  .birthday-icon {
    width: 28px;
    height: 28px;
  }
  
  .birthday-icon .icon {
    font-size: 18px;
  }
  
  .birthday-title {
    font-size: 0.8rem;
  }
  
  .birthday-message {
    font-size: 0.75rem;
  }
}
</style>

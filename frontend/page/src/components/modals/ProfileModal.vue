<template>
  <!-- 個人資料彈窗 -->
  <div v-if="ui.profileModalAuthor" class="modal profile-modal" :class="{ show: ui.profileModalAuthor }">
    <div class="modal-header">
      <h3>{{ ui.profileModalAuthor.key === 'project_home' ? t('project_profile_title') : t('profile_description') }}</h3>
      <button class="modal-close-btn" @click="closeModal">&times;</button>
    </div>
    <div class="modal-content">
      <!-- 主頁 L高介紹 -->
      <template v-if="ui.profileModalAuthor.key === 'project_home'">
        <div class="profile-desc">{{ ui.profileModalAuthor.profile.description }}</div>
        <div class="satellite-image-container">
          <img src="/assets/images/project/satellite.png" alt="L高サテライト紹介" />
          <span class="satellite-image-caption">L高のサテライト紹介</span>
        </div>
      </template>
      
      <!-- 成員自我介紹 -->
      <template v-else>
        <div class="profile-desc">{{ ui.profileModalAuthor.description }}</div>
        <div class="profile-details">
          <div class="profile-item">
            <span class="profile-label">{{ t('profile_grade') }}</span>
            <span class="profile-content">{{ ui.profileModalAuthor.grade }}</span>
          </div>
          <div class="profile-item">
            <span class="profile-label">{{ t('profile_birthday') }}</span>
            <span class="profile-content">{{ ui.profileModalAuthor.birthday }}</span>
          </div>
          <div class="profile-item">
            <span class="profile-label">{{ t('profile_bloodType') }}</span>
            <span class="profile-content">{{ ui.profileModalAuthor.blood_type }}</span>
          </div>
          <div class="profile-item">
            <span class="profile-label">{{ t('profile_height') }}</span>
            <span class="profile-content">{{ ui.profileModalAuthor.height }}</span>
          </div>
          <div class="profile-item">
            <span class="profile-label">{{ t('profile_hobby') }}</span>
            <span class="profile-content">{{ ui.profileModalAuthor.hobby }}</span>
          </div>
          <div class="profile-item">
            <span class="profile-label">{{ t('profile_skill') }}</span>
            <span class="profile-content">{{ ui.profileModalAuthor.skill }}</span>
          </div>
          <div class="profile-item">
            <span class="profile-label">{{ t('profile_likes') }}</span>
            <span class="profile-content">{{ ui.profileModalAuthor.likes }}</span>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
// 定義 props - 從父組件接收的資料
const props = defineProps({
  ui: Object
});

// 定義 emits - 向父組件發送的事件
const emit = defineEmits(['closeModal']);

// 翻譯函數 - 獲取多語言文字
const t = (key) => {
  const translations = {
    'ja': { 
      project_profile_title: 'L高とは',
      profile_description: '自己紹介',
      profile_grade: '学年',
      profile_birthday: '誕生日',
      profile_bloodType: '血液型',
      profile_height: '身長',
      profile_hobby: '趣味',
      profile_skill: '特技',
      profile_likes: '好物'
    }
  };
  return translations['ja']?.[key] || key;
};

// 事件處理函數 - 關閉彈窗
const closeModal = () => emit('closeModal');
</script>

<style scoped>
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: var(--bg-secondary);
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
  backdrop-filter: blur(12px);
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
  background-color: var(--bg-tertiary);
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

.profile-desc {
  color: var(--text-primary);
  line-height: 1.6;
  margin-bottom: calc(var(--spacing-unit) * 1.5);
  white-space: pre-wrap;
  font-size: 1rem;
  text-align: left;
  padding: 0;
  margin-left: 0;
  margin-right: 0;
  /* 讓介紹文本與標籤文字對齊 */
  padding-left: calc(60px + var(--spacing-unit) * 2);
}

.satellite-image-container {
  text-align: center;
  margin-top: calc(var(--spacing-unit) * 1.5);
}

.satellite-image-container img {
  max-width: 100%;
  height: auto;
  border-radius: var(--border-radius);
  margin-bottom: calc(var(--spacing-unit) * 0.5);
}

.satellite-image-caption {
  display: inline-block;
  font-size: 0.9rem;
  font-style: normal;
  margin-top: var(--spacing-unit);
  padding: var(--spacing-xs) var(--spacing-sm);
  background-color: var(--bg-secondary);
  color: var(--brand-blue);
  border: 1px solid var(--brand-blue);
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-1);
}

/* 個人資料詳細資訊容器 - 使用 Flexbox 垂直排列各項目 */
.profile-details {
  margin: 0;
  font-size: 0.85rem;
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing-unit) * 0.5);
  width: 100%;
}

/* 個人資料項目容器 - 每個項目獨立一行，使用 Flexbox 水平排列標籤和內容 */
.profile-item {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 2); /* 增加標籤和內容之間的間距 */
  padding: calc(var(--spacing-unit) * 0.4) calc(var(--spacing-unit) * 0.6);
  background-color: var(--bg-tertiary);
  border-radius: var(--radius-sm);
  border-left: 3px solid var(--brand-color);
  border-right: 3px solid var(--brand-color);
  min-height: calc(var(--spacing-unit) * 2.2);
  box-sizing: border-box;
  width: 100%;
  flex-shrink: 0;
}

/* 個人資料標籤 - 固定寬度，分散對齊，確保整齊排列 */
.profile-label {
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.85rem;
  white-space: nowrap;
  min-width: 60px;
  max-width: 60px;
  text-align: justify;
  text-align-last: justify; /* 確保最後一行也分散對齊 */
  flex-shrink: 0;
  display: inline-block;
}

/* 個人資料內容 - 填充剩餘空間，左對齊，確保每個項目獨立一行 */
.profile-content {
  color: var(--text-primary);
  line-height: 1.4;
  font-size: 0.85rem;
  flex: 1;
  text-align: left;
  word-break: break-word;
  display: inline-block;
  min-width: 0;
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
  
  .profile-desc {
    font-size: 0.95rem;
    /* 手機版也讓介紹文本與標籤文字對齊 */
    padding-left: calc(50px + var(--spacing-unit) * 1.5);
  }
  
  .profile-item {
    padding: calc(var(--spacing-unit) * 0.4);
    gap: calc(var(--spacing-unit) * 1.5); /* 手機版也增加間距，但稍微小一點 */
  }
  
  .profile-label {
    font-size: 0.9rem;
    min-width: 50px;
    max-width: 50px;
    text-align: justify;
    text-align-last: justify; /* 手機版也使用分散對齊 */
  }
  
  .profile-content {
    font-size: 0.9rem;
  }
}
</style>

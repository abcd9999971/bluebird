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
        <div class="profile-desc">{{ ui.profileModalAuthor.profile.description }}</div>
        <dl class="profile-details">
          <dt>{{ t('profile_grade') }}</dt>
          <dd>{{ ui.profileModalAuthor.profile.details.grade }}</dd>
          <dt>{{ t('profile_birthday') }}</dt>
          <dd>{{ ui.profileModalAuthor.profile.details.birthday }}</dd>
          <dt>{{ t('profile_bloodType') }}</dt>
          <dd>{{ ui.profileModalAuthor.profile.details.bloodType }}</dd>
          <dt>{{ t('profile_height') }}</dt>
          <dd>{{ ui.profileModalAuthor.profile.details.height }}</dd>
          <dt>{{ t('profile_hobby') }}</dt>
          <dd>{{ ui.profileModalAuthor.profile.details.hobby }}</dd>
          <dt>{{ t('profile_skill') }}</dt>
          <dd>{{ ui.profileModalAuthor.profile.details.skill }}</dd>
          <dt>{{ t('profile_likes') }}</dt>
          <dd>{{ ui.profileModalAuthor.profile.details.likes }}</dd>
        </dl>
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

.profile-desc {
  color: var(--text-primary);
  line-height: 1.6;
  margin-bottom: calc(var(--spacing-unit) * 1.5);
  white-space: pre-wrap;
  font-size: 1rem;
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

.profile-details {
  margin: 0;
  font-size: 0.85rem;
}

.profile-details dt {
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.85rem;
  text-align: left;
  padding: 0;
  margin: 0 4px 0 0;
  white-space: nowrap;
  float: left;
  clear: left;
}

.profile-details dd {
  margin: 0 0 calc(var(--spacing-unit) * 0.5) 0;
  color: var(--text-primary);
  line-height: 1.4;
  font-size: 0.85rem;
  background-color: var(--bg-tertiary);
  padding: calc(var(--spacing-unit) * 0.4) calc(var(--spacing-unit) * 0.6);
  border-radius: var(--radius-sm);
  border-left: 3px solid var(--brand-color);
  min-height: calc(var(--spacing-unit) * 2.2);
  display: flex;
  align-items: center;
  box-sizing: border-box;
  overflow: hidden;
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
  }
  
  .profile-details dt {
    font-size: 0.9rem;
  }
  
  .profile-details dd {
    font-size: 0.9rem;
    padding: calc(var(--spacing-unit) * 0.4);
  }
}
</style>

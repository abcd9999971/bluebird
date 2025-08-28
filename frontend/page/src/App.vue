<template>
  <div class="app-container">
    <div class="container">
      <h1>生きづらい部 部員日誌</h1>
      
      <div v-if="loading" class="loading">
        ⏳ 載入中...
      </div>
      
      <div v-else-if="error" class="error">
        ❌ 載入失敗: {{ error }}
      </div>
      
      <div v-else class="timeline">
        <div v-for="(article, index) in sortedArticles" 
             :key="index" 
             class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-date">{{ formatDate(article.created_at) }}</div>
          <div class="article-card">
            <div class="article-header">
              <div class="author">👤 作者 {{ article.author_id }}</div>
            </div>
            <div class="article-text">{{ article.text }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const articles = ref([]);
const loading = ref(true);
const error = ref(null);

// 計算排序後的文章（按時間倒序）
const sortedArticles = computed(() => {
  return articles.value.sort((a, b) => {
    const dateA = new Date(a.created_at.replace(/\//g, '-'));
    const dateB = new Date(b.created_at.replace(/\//g, '-'));
    return dateB - dateA; // 倒序排列（最新的在前）
  });
});

// 格式化日期顯示
const formatDate = (dateStr) => {
  const date = new Date(dateStr.replace(/\//g, '-'));
  const today = new Date();
  const diffTime = Math.abs(today - date);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays === 1) {
    return '今天';
  } else if (diffDays === 2) {
    return '昨天';
  } else if (diffDays <= 7) {
    return `${diffDays - 1} 天前`;
  } else {
    return dateStr;
  }
};

onMounted(async () => {
  try {

    // 如果要使用實際 API，取消下面這行的註釋並註釋掉上面的 mockData
    const response = await fetch('http://localhost:8787');
    if (!response.ok) {
        throw new Error(`HTTP 錯誤! 狀態碼: ${response.status}`);
    }
    const data = await response.json();
    articles.value = data;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.app-container {
  font-family: 'Arial', sans-serif;
  background: linear-gradient(135deg, #ffa200 0%, #552e7c 100%);
  min-height: 100vh;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  text-align: center;
  color: white;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.loading, .error {
  text-align: center;
  font-size: 1.2rem;
  padding: 2rem;
  color: white;
  background: rgba(255,255,255,0.1);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  margin: 2rem 0;
}

.error {
  background: rgba(255,0,0,0.2);
}

.timeline {
  position: relative;
  padding-left: 3rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 1rem;
  top: 0;
  height: 100%;
  width: 4px;
  background: linear-gradient(to bottom, #fff, rgba(255,255,255,0.3));
  border-radius: 2px;
}

.timeline-item {
  position: relative;
  margin-bottom: 3rem;
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
  transform: translateY(30px);
}

.timeline-item:nth-child(1) { animation-delay: 0.1s; }
.timeline-item:nth-child(2) { animation-delay: 0.2s; }
.timeline-item:nth-child(3) { animation-delay: 0.3s; }
.timeline-item:nth-child(4) { animation-delay: 0.4s; }
.timeline-item:nth-child(n+5) { animation-delay: 0.5s; }

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.timeline-dot {
  position: absolute;
  left: -2.7rem;
  top: 1rem;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  border: 4px solid white;
  border-radius: 50%;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  z-index: 2;
}

.timeline-date {
  position: absolute;
  left: -12rem;
  top: 1rem;
  background: rgba(255,255,255,0.9);
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.9rem;
  font-weight: bold;
  color: #555;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  white-space: nowrap;
  transform: translateY(-10%);
}

.article-card {
  background: rgba(255,255,255,0.95);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255,255,255,0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.article-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #ff6b6b, #ee5a24, #ffa726, #42a5f5);
  background-size: 300% 100%;
  animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0,0,0,0.3);
}

.article-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.author {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.article-text {
  font-size: 1.1rem;
  line-height: 1.8;
  white-space: pre-line;
  color: #444;
}

@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 2rem;
  }

  .timeline {
    padding-left: 2rem;
  }

  .timeline-date {
    position: static;
    display: inline-block;
    margin-bottom: 1rem;
    left: auto;
    top: auto;
  }

  .timeline-dot {
    left: -1.5rem;
  }

  .article-card {
    padding: 1.5rem;
  }

  .author {
    text-align: center;
  }
}
</style>
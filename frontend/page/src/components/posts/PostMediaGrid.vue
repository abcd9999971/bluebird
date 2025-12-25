<template>
  <div class="media-grid">
    <div 
      v-for="tweet in mediaTweets" 
      :key="tweet.id" 
      class="media-item"
      @click="$emit('openDetail', tweet)"
    >
      <img 
        :src="tweet.image_url" 
        loading="lazy" 
        class="media-img"
        @error="handleImageError"
      />
      <div class="media-overlay">
        <span class="icon">favorite</span> {{ tweet.likes || 0 }}
      </div>
    </div>
    
    <div v-if="mediaTweets.length === 0" class="empty-state">
      <span class="icon">image_not_supported</span>
      <p>No media found</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  tweets: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['openDetail']);

// Filter only tweets with images
const mediaTweets = computed(() => {
  return props.tweets.filter(t => t.image_url);
});

const handleImageError = (e) => {
  e.target.style.display = 'none';
};
</script>

<style scoped>
.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: var(--spacing-unit);
  padding: var(--spacing-unit);
}

.media-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
  background-color: var(--bg-tertiary);
}

.media-item:hover {
  transform: scale(1.02);
  box-shadow: var(--shadow-2);
}

.media-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.3s;
}

.media-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 8px;
  background: linear-gradient(to top, rgba(0,0,0,0.6), transparent);
  color: white;
  opacity: 0;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.8rem;
}

.media-item:hover .media-overlay {
  opacity: 1;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px;
  color: var(--text-secondary);
}
</style>

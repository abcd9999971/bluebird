<template>
  <div class="loader">
    <div class="loader-content">
      <img src="/assets/images/logos/emblem.png" alt="Loading..." class="loader-image">
        <div class="loader-dots">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
    </div>  
  </div>
</template>

<script setup>
</script>

<style scoped>
/* 樣式已還原為扁平結構 */
.loader { 
  position: fixed; 
  inset: 0; 
  background: var(--bg-primary); 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  justify-content: center; 
  z-index: 100; 
  transition: opacity .4s ease-in-out, visibility .4s; 
  visibility: visible; 
  opacity: 1; 
}

.loader.hide { 
  opacity: 0; 
  visibility: hidden; 
}

.loader-content { 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  gap: calc(var(--spacing-unit) * 4); 
}

.loader-image { 
  max-width: 80px; 
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.5); opacity: 0.5; }
  40% { transform: scale(1.0); opacity: 1; }
}

.loader-dots { 
  display: flex; 
  gap: 12px; 
}

.loader-dots .dot {
  width: 16px;
  height: 16px;
  background-color: var(--brand-color);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loader-dots .dot:nth-child(1) { animation-delay: -0.32s; }
.loader-dots .dot:nth-child(2) { animation-delay: -0.16s; }

</style>

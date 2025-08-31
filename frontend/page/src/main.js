import { createApp } from 'vue'
import App from './App.vue'
import './assets/styles.css'

// 移除全局 html2canvas 導入，改為按需導入
// 這樣可以避免不必要的全局污染，並提高性能

createApp(App).mount('#app')
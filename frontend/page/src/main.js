import { createApp } from 'vue'
import App from './App.vue'
import './assets/styles.css'
import i18n from './i18n.js'

// 移除全局 html2canvas 導入，改為按需導入
// 這樣可以避免不必要的全局污染，並提高性能

createApp(App).use(i18n).mount('#app')
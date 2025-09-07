/**
 * 應用程式入口檔案
 * 初始化 Vue 應用程式並掛載到 DOM
 */

import { createApp } from 'vue'
import App from './App.vue'
import './assets/styles.css'
import i18n from './i18n.js'

// 移除全域 html2canvas 導入，改為按需導入
// 這樣可以避免不必要的全域污染，並提高效能

// 創建並掛載 Vue 應用程式
createApp(App).use(i18n).mount('#app')
import { createApp } from 'vue'
import App from './App.vue'
import './assets/styles.css'

// 引入 html2canvas
import html2canvas from 'html2canvas'
window.html2canvas = html2canvas

// 引入 Material Symbols 字體
const link = document.createElement('link');
link.rel = 'stylesheet';
link.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200';
document.head.appendChild(link);

// 引入 Noto Sans JP 字體
const fontLink = document.createElement('link');
fontLink.rel = 'stylesheet';
fontLink.href = 'https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap';
document.head.appendChild(fontLink);

createApp(App).mount('#app')

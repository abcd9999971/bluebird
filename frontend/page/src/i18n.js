/**
 * 國際化配置檔案
 * 使用 vue-i18n 管理應用程式中的多語言文本內容
 */

import { createI18n } from 'vue-i18n';
import ja from './locales/ja.json';

// 語言包配置
const messages = {
  ja // 日文語言包
};

// 創建 i18n 實例
const i18n = createI18n({
  locale: 'ja', // 預設語言設為日文
  fallbackLocale: 'ja', // 備用語言
  messages,
  legacy: false, // 使用 Composition API 模式
  globalInjection: true // 全域注入 $t 函數
});

export default i18n;

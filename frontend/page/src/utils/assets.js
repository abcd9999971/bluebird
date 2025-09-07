// 本地資源管理模組
// 統一管理所有本地圖片資源的路徑

const ASSETS_BASE_PATH = '/assets/images';

// 資源路徑配置
export const ASSETS = {
  // 成員頭貼
  AVATARS: {
    POLKA: `${ASSETS_BASE_PATH}/avatars/polka.png`,
    MAI: `${ASSETS_BASE_PATH}/avatars/mai.png`,
    AKIRA: `${ASSETS_BASE_PATH}/avatars/akira.png`,
    HANABI: `${ASSETS_BASE_PATH}/avatars/hanabi.png`,
    MIRACLE: `${ASSETS_BASE_PATH}/avatars/miracle.png`,
    NORIKO: `${ASSETS_BASE_PATH}/avatars/noriko.png`,
    YUKURI: `${ASSETS_BASE_PATH}/avatars/yukuri.png`,
    AURORA: `${ASSETS_BASE_PATH}/avatars/aurora.png`,
    MIDORI: `${ASSETS_BASE_PATH}/avatars/midori.png`,
    SHION: `${ASSETS_BASE_PATH}/avatars/shion.png`,
    PROJECT: `${ASSETS_BASE_PATH}/avatars/project-avatar.jpg`
  },
  
  // 橫幅圖片
  BANNERS: {
    POLKA: `${ASSETS_BASE_PATH}/banners/polka-banner.jpg`,
    MAI: `${ASSETS_BASE_PATH}/banners/mai-banner.jpg`,
    AKIRA: `${ASSETS_BASE_PATH}/banners/akira-banner.jpg`,
    HANABI: `${ASSETS_BASE_PATH}/banners/hanabi-banner.jpg`,
    MIRACLE: `${ASSETS_BASE_PATH}/banners/miracle-banner.jpg`,
    NORIKO: `${ASSETS_BASE_PATH}/banners/noriko-banner.jpg`,
    YUKURI: `${ASSETS_BASE_PATH}/banners/yukuri-banner.jpg`,
    AURORA: `${ASSETS_BASE_PATH}/banners/aurora-banner.jpg`,
    MIDORI: `${ASSETS_BASE_PATH}/banners/midori-banner.jpg`,
    SHION: `${ASSETS_BASE_PATH}/banners/shion-banner.jpg`,
    PROJECT: `${ASSETS_BASE_PATH}/banners/project-banner.jpg`
  },
  
  // Logo 和標誌
  LOGOS: {
    EMBLEM: `${ASSETS_BASE_PATH}/logos/emblem.png`,
    LOGO3: `${ASSETS_BASE_PATH}/logos/logo3.svg`
  },
  
  // 專案相關圖片
  PROJECT: {
    SATELLITE: `${ASSETS_BASE_PATH}/project/satellite.png`
  }
};

// 成員 ID 到頭貼的映射
export const MEMBER_AVATARS = {
  'polka': ASSETS.AVATARS.POLKA,
  'mai': ASSETS.AVATARS.MAI,
  'akira': ASSETS.AVATARS.AKIRA,
  'hanabi': ASSETS.AVATARS.HANABI,
  'miracle': ASSETS.AVATARS.MIRACLE,
  'noriko': ASSETS.AVATARS.NORIKO,
  'yukuri': ASSETS.AVATARS.YUKURI,
  'aurora': ASSETS.AVATARS.AURORA,
  'midori': ASSETS.AVATARS.MIDORI,
  'shion': ASSETS.AVATARS.SHION,
  'project_home': ASSETS.AVATARS.PROJECT
};

// 成員 ID 到橫幅的映射
export const MEMBER_BANNERS = {
  'polka': ASSETS.BANNERS.POLKA,
  'mai': ASSETS.BANNERS.MAI,
  'akira': ASSETS.BANNERS.AKIRA,
  'hanabi': ASSETS.BANNERS.HANABI,
  'miracle': ASSETS.BANNERS.MIRACLE,
  'noriko': ASSETS.BANNERS.NORIKO,
  'yukuri': ASSETS.BANNERS.YUKURI,
  'aurora': ASSETS.BANNERS.AURORA,
  'midori': ASSETS.BANNERS.MIDORI,
  'shion': ASSETS.BANNERS.SHION,
  'project_home': ASSETS.BANNERS.PROJECT
};

// 獲取成員頭貼
export function getMemberAvatar(memberId) {
  return MEMBER_AVATARS[memberId] || ASSETS.AVATARS.PROJECT;
}

// 獲取成員橫幅
export function getMemberBanner(memberId) {
  return MEMBER_BANNERS[memberId] || ASSETS.BANNERS.PROJECT;
}

// 預載入圖片資源（用於 html2canvas）
export function preloadImages() {
  const allImages = [
    ...Object.values(ASSETS.AVATARS),
    ...Object.values(ASSETS.BANNERS),
    ...Object.values(ASSETS.LOGOS),
    ...Object.values(ASSETS.PROJECT)
  ];
  
  return Promise.all(
    allImages.map(src => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = reject;
        img.src = src;
      });
    })
  );
}

// 檢查圖片是否已載入
export function isImageLoaded(src) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => resolve(true);
    img.onerror = () => resolve(false);
    img.src = src;
  });
}

/**
 * 處理從 JSON 載入的成員資料，添加動態的 avatar 和 banner 屬性
 * @param {Object} memberData - 從 member.json 載入的成員資料
 * @returns {Object} 包含完整成員資訊的物件
 */
export function processMemberData(memberData) {
  const processedMembers = {};
  
  for (const [memberId, memberInfo] of Object.entries(memberData)) {
    processedMembers[memberId] = {
      ...memberInfo,
      avatar: getMemberAvatar(memberId),
      banner: getMemberBanner(memberId)
    };
  }
  
  return processedMembers;
}

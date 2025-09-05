<template>
  <div id="app">
    <Loader  v-if="!ui.loaded" />
    <div v-else class="app-shell">
    <div class="app-container">
        <!-- 左側邊欄 -->
        <aside class="sidebar-left">
          <div class="main-nav">
            <button class="nav-btn" :class="{ active: !filters.member && !filters.onlyLiked }" @click="resetFilters">
              <span class="icon">home</span>
              {{ t('home_button_text') }}
            </button>
            
            <div v-if="ui.showSearchInput" class="search-container">
              <input 
                ref="searchInput"
                v-model="filters.search"
                type="text" 
                class="search-input" 
                :placeholder="t('search_placeholder')"
                @blur="onSearchBlur"
              >
            </div>
            <button v-else class="nav-btn" @click="focusSearch">
              <span class="icon">search</span>
              {{ t('search_placeholder') }}
            </button>
            
            <button class="nav-btn" :class="{ active: filters.onlyLiked }" @click="toggleLikedFilter">
              <span class="icon">favorite</span>
              {{ t('filter_liked') }}
            </button>
          </div>

          <!-- 成員篩選 -->
          <div class="filters-nav">
            <button 
              v-for="memberId in characterOrder" 
              :key="memberId"
              class="nav-btn" 
              :class="{ active: filters.member === memberId }"
              @click="setMemberFilter(memberId)"
            >
              <img :src="authors[memberId]?.avatar || ''" :alt="authors[memberId]?.name_ja || memberId" class="filter-avatar">
              {{ authors[memberId]?.name_ja || memberId }}
            </button>
          </div>

          <!-- 說明小卡 -->
          <div class="info-card">
            <img src="/assets/images/logos/logo3.svg" alt="Logo">
            <div v-html="t('unofficial_site_notice')"></div>
          </div>
          
          <!-- 主題切換 -->
          <div class="settings-btn-container">
            <button class="nav-btn" @click="toggleTheme">
              <span class="icon">{{ prefs.dark ? 'light_mode' : 'dark_mode' }}</span>
              {{ t('dark_mode_label') }}
            </button>
          </div>
        </aside>

        <!-- 主要時間軸 -->
        <main class="timeline">
          <!-- 時間軸標題 -->
          <header class="timeline-header">
            <div class="mobile-header">
              <button class="action-btn" @click="focusSearch" :title="t('search_placeholder')">
                <span class="icon">search</span>
              </button>
              <button class="action-btn" @click="openDateNavModal" :title="t('quick_scroll_title')">
                <span class="icon">calendar_month</span>
              </button>
              <input 
                v-if="ui.showMobileSearch" 
                ref="mobileSearchInput" 
                type="text" 
                class="search-input mobile-search-input" 
                :placeholder="t('search_placeholder')" 
                v-model.trim="filters.search" 
                @blur="onSearchBlur" 
              />
            </div>
            <h1 v-if="!ui.showMobileSearch">{{ headerTitle }}</h1>
            <div class="mobile-header" v-if="!ui.showMobileSearch">
              <button class="action-btn" @click="toggleTheme" :title="t('dark_mode_label')">
                <span class="icon">{{ prefs.dark ? 'dark_mode' : 'light_mode' }}</span>
              </button>
            </div>
          </header>
          
          <!-- 手機版導航 -->
          <nav class="mobile-nav">
            <!-- 手機版：新增主頁按鈕 -->
            <img 
              :src="projectInfo?.avatar || '/assets/images/avatars/project-avatar.jpg'" 
              :alt="projectInfo?.name_ja || 'いきづらい部'" 
              class="mobile-avatar" 
              :class="{'active': !filters.member && !filters.onlyLiked}" 
              @click="resetFilters"
            />
            <!-- 手機版：いいねした日誌按鈕 -->
            <button 
              class="mobile-filter-btn"
              :class="{'active': filters.onlyLiked}"
              @click="toggleLikedFilter"
              :title="t('filter_liked')"
            >
              <span class="icon">favorite</span>
            </button>
            <!-- 手機版：成員列表 -->
            <img 
              v-for="key in characterOrder" 
              :key="'m-'+key" 
              :src="authors[key]?.avatar || ''" 
              :alt="authors[key]?.name_ja || key" 
              class="mobile-avatar" 
              :class="{'active': filters.member===key}" 
              @click="setMemberFilter(key)"
            />
          </nav>

          <!-- 成員橫幅 -->
          <div v-if="filters.member || (!filters.member && !filters.onlyLiked)" class="member-header">
            <div class="member-banner" :style="currentBannerStyle"></div>
            <img 
              v-if="filters.member" 
              :src="authors[filters.member]?.avatar || ''" 
              :alt="authors[filters.member]?.name_ja || filters.member" 
              class="member-avatar"
            >
            <img 
              v-else 
              :src="projectInfo?.avatar || '/assets/images/avatars/project-avatar.jpg'" 
              :alt="projectInfo?.name_ja || 'いきづらい部'" 
              class="member-avatar"
            >
            <div v-if="filters.member" class="member-meta-top">
              <button class="profile-btn" @click="openProfileModal(authors[filters.member])">
                {{ t('profile_button') }}
              </button>
            </div>
            <div v-if="filters.member" class="member-name">{{ authors[filters.member]?.name_ja || filters.member }}</div>
            <div v-if="filters.member" class="member-id">{{ authors[filters.member]?.id || `@${filters.member}` }}</div>
            <div v-else-if="!filters.member" class="member-name">{{ projectInfo?.name_ja || 'いきづらい部' }}</div>
            <div v-else-if="!filters.member" class="member-id">{{ projectInfo?.id || '@ikizulive_staff' }}</div>
            
            <!-- 主頁自我介紹按鈕 -->
            <div v-if="!filters.member" class="member-meta-top">
              <button class="profile-btn" @click="openProfileModal(projectInfo)">
                {{ projectInfo?.profile_btn_text || 'L高とは' }}
              </button>
            </div>
          </div>

          <!-- 推文列表 -->
          <div v-if="filteredTweets.length > 0">
            <article 
              v-for="tweet in filteredTweets" 
              :key="tweet.id"
              class="tweet"
              :data-tweet-id="tweet.id"
              @click="openDetail(tweet)"
            >
              <img :src="tweet.avatar_url || authors[tweet.author_id]?.avatar || ''" :alt="tweet.name_ja || authors[tweet.author_id]?.name_ja || tweet.author_id" class="tweet-avatar">
                              <div class="tweet-body">
                  <div class="tweet-header">
                    <span class="tweet-name">{{ tweet.name_ja || authors[tweet.author_id]?.name_ja || tweet.author_id }}@いきづらい部！</span>
                    <span class="tweet-id">{{ tweet.twitter_id || authors[tweet.author_id]?.id || `@${tweet.author_id}` }}</span>
                    <span class="tweet-time">{{ formatTime(tweet.created_at) }}</span>
                  </div>
                <div class="tweet-text" v-html="linkify(tweet.content)" @click="handleTweetTextClick"></div>
                <div class="tweet-actions">
                  <button 
                    class="action-btn like" 
                    :class="{ 'is-liked': tweet.liked, pop: tweet._pop }"
                    @click.stop="toggleLike(tweet)"
                  >
                    <span class="icon">favorite</span>
                  </button>
                  <button 
                    class="action-btn share" 
                    :class="{ 'is-sharing': ui.isSharing === tweet.id }"
                    @click.stop="shareTweet(tweet)"
                  >
                    <span class="icon">share</span>
                  </button>
                </div>
              </div>
            </article>
          </div>

          <!-- 空狀態 -->
          <div v-else class="empty-state">
            <span class="icon">sentiment_dissatisfied</span>
            <p>{{ t('empty_state_text') }}</p>
          </div>
        </main>

        <!-- 右側邊欄 -->
        <aside class="sidebar-right">
          <div class="date-navigator">
            <div class="date-navigator-header">
              <h3>{{ t('quick_scroll_title') }}</h3>
            </div>
            
            <div class="date-navigator-controls">
              <!-- 年份選擇器 -->
              <div class="year-scroller">
                <div class="switcher-row">
                  <button 
                    v-for="year in availableYears" 
                    :key="year"
                    class="switcher-btn" 
                    :class="{ active: filters.year === year }"
                    @click="filters.year = year"
                  >
                    {{ year }}
                  </button>
                </div>
              </div>

              <!-- 月份選擇器 -->
              <div v-if="filters.year" class="month-grid">
                <button 
                  v-for="month in 12" 
                  :key="month"
                  class="switcher-btn" 
                  :class="{ active: filters.month === month }"
                  @click="setMonthFilter(month)"
                  :disabled="!availableMonths.includes(month)"
                >
                  {{ month }}{{ t('month_unit') }}
                </button>
              </div>

              <!-- 日期列表 -->
              <div class="date-list">
                <div 
                  v-for="dateGroup in dateGroups" 
                  :key="dateGroup.date"
                  class="date-list-item"
                  :class="{ active: scroller.activeDate === dateGroup.date }"
                  @click="scrollToDate(dateGroup.firstTweetId)"
                >
                  <span>{{ formatDateForScroller(dateGroup.date) }}</span>
                  <span class="date-count">{{ dateGroup.count }}</span>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>

    <!-- 遮罩層 -->
    <div class="overlay" :class="{ show: ui.overlay }" @click="closeAllModals"></div>

    <!-- 推文詳情彈窗 -->
    <div v-if="ui.detail" class="modal" :class="{ show: ui.detail }">
      <div class="modal-header">
        <h3>{{ t('tweet_detail_header') }}</h3>
        <button class="modal-close-btn" @click="closeAllModals">&times;</button>
      </div>
      <div class="modal-content">
        <article v-if="ui.detailTweet" class="tweet">
          <img :src="ui.detailTweet.avatar_url" :alt="ui.detailTweet.name_ja" class="tweet-avatar">
                      <div class="tweet-body">
              <div class="tweet-header">
                <span class="tweet-name">{{ ui.detailTweet.name_ja }}@いきづらい部！</span>
                <span class="tweet-id">{{ ui.detailTweet.twitter_id }}</span>
                <span class="tweet-time">{{ formatTime(ui.detailTweet.created_at) }}</span>
              </div>
            <div class="tweet-text" v-html="linkify(ui.detailTweet.content)"></div>
          </div>
        </article>
      </div>
    </div>

    <!-- 個人資料彈窗 -->
    <div v-if="ui.profileModalAuthor" class="modal profile-modal" :class="{ show: ui.profileModalAuthor }">
      <div class="modal-header">
        <h3>{{ t('profile_description') }}</h3>
        <button class="modal-close-btn" @click="closeAllModals">&times;</button>
        </div>
      <div class="modal-content">
        <!-- 主頁 L高とは 介紹 -->
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
      
    <!-- 手機版日期導覽 Modal -->
    <div v-if="ui.dateNavModal" class="modal" :class="{ show: ui.dateNavModal }">
      <div class="modal-header">
        <h3>{{ t('quick_scroll_title') }}</h3>
        <button class="modal-close-btn" @click="closeAllModals">&times;</button>
      </div>
      <div class="modal-content">
        <div class="date-navigator" style="border:none; border-radius:0; height: auto;">
          <div class="date-navigator-controls">
            <div class="year-scroller">
              <div class="switcher-row">
                <button 
                  v-for="year in availableYears" 
                  :key="year" 
                  class="switcher-btn" 
                  :class="{ active: year === filters.year }" 
                  @click="filters.year = year"
                >
                  {{ year }}
                </button>
              </div>
            </div>
            <div class="month-grid">
              <button 
                v-for="month in 12" 
                :key="month" 
                class="switcher-btn" 
                :class="{ active: month === filters.month }" 
                @click="setMonthFilter(month)" 
                :disabled="!availableMonths.includes(month)"
              >
                {{ month }}{{ t('month_unit') }}
              </button>
            </div>
          </div>
          <div class="date-list" style="max-height: 40vh;">
            <div v-if="dateGroups.length > 0">
              <div 
                v-for="group in dateGroups" 
                :key="group.date" 
                class="date-list-item" 
                :class="{ active: group.date === scroller.activeDate }" 
                @click="scrollToDate(group.firstTweetId); closeAllModals()"
              >
                <span>{{ formatDateForScroller(group.date) }}</span>
                <span class="date-count">{{ group.count }}</span>
              </div>
            </div>
            <div v-else class="empty-state" style="padding:1rem;">
              {{ t('no_tweets_for_year') }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 回到頂部按鈕 -->
    <ToTopButton :show="ui.showTop" />



    <!-- Toast 通知 -->
    <div v-if="toast.show" class="toast" :class="toast.type">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { getMemberAvatar, getMemberBanner } from './utils/assets.js';
import { shareTweetAsImage } from './utils/html2canvas-helper.js';
import Loader from './components/ui/Loader.vue';
import ToTopButton from './components/ui/ToTopButton.vue';

// 專案資訊
const projectInfo = reactive({ 
  key: 'project_home',
  name_ja: 'いきづらい部', 
  id: '@ikizulive_staff',
  avatar: '/assets/images/avatars/project-avatar.jpg',
  banner: '/assets/images/banners/project-banner.jpg',
  color: 'var(--brand-blue)',
  profile_btn_text: 'L高とは',
  profile: {
    description: 'Love学院高等学校。略してL高。\n全国にサテライト校を持つインターネット高校。\n生徒たちは自由にカリキュラムを組み、オンラインで学習できる。\nひとりひとりのライフスタイルに合わせて単位取得が可能。'
  }
});

// 翻譯
const translations = {
  'ja': { 
    main_header: '部員日誌', 
    filter_liked: 'いいねした日誌', 
    dark_mode_label: 'テーマ切り替え', 
    empty_state_text: '該当する日誌はありません。', 
    search_placeholder: '日誌を検索', 
    tweet_detail_header: '日誌詳細', 
    share_button_title: '画像として保存', 
    home_button_text: 'ホーム', 
    quick_scroll_title: '日付で移動', 
    no_tweets_for_year: 'その期間には日誌がありません', 
    image_gen_success: '画像が正常にダウンロードされました。', 
    image_gen_fail: '画像の生成に失敗しました。', 
    unofficial_site_notice: 'いきづらい部！<br>の非公式メンバー日誌サイト', 
    month_unit: '月', 
    follow_button: 'フォロー中', 
    profile_button: '自己紹介', 
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

// 從原始HTML中提取的範例資料作為備用
const fallbackAuthors = {
  polka: { key:'polka', name_ja:'高橋ポルカ', id:'@polka_lion', color:'#ccb12e', avatar: getMemberAvatar('polka'), banner: getMemberBanner('polka'), profile: { description: 'L高 浅草サテライトの1年生。\n明るく元気な性格で、嬉しくなると足が勝手に踊りだす。\n小さい頃から数学が大の苦手で、高校受験に失敗。\nネット高校であるL高に入学し、スクールアイドルを見つけた。', details: { grade: '1年生', birthday: '8月18日', bloodType: '不明', height: '157cm', hobby: '昼寝', skill: 'どこでも寝れる。街頭インタビューでよく声をかけられる。クジを当てる。', likes: '麺類全般、特にうどん。チョコレート' }}},
  mai: { key:'mai', name_ja:'麻布麻衣', id:'@My_Mai_Eld', color:'#009fdf', avatar: getMemberAvatar('mai'), banner: getMemberBanner('mai'), profile: { description: 'L高 浅草サテライトの1年生。\nプログラムとトロンのPC、論理的思考力を愛し、誰も見たことがない美しいプログラムを作るのが夢。\n合理的な性格で、人とコミュニケーションを取るのが苦手。\n本人は不本意だが、いつもポルカのペースに飲まれがち。', details: { grade: '1年生', birthday: '2月13日', bloodType: 'B型', height: '154cm', hobby: 'プログラミング、データマイニング、マイクラ', skill: 'はんだごて、DIY', likes: '果物、特にメロンとブドウ。ハンバーガー' }}},
  akira: { key:'akira', name_ja:'五桐玲', id:'@G_Akky304250', color:'#88d66e', avatar: getMemberAvatar('akira'), banner: getMemberBanner('akira'), profile: { description: 'L高 浅草サテライトの1年生。\nクライミングでプロのアスリートを目指しており、練習やトレーニングの時間を確保するためL高に入学した。\n誰かと一緒にいる時間より、一人で身体を動かす時間を好む。\n自立しているが意外に抜けているところがある。', details: { grade: '1年生', birthday: '7月9日', bloodType: 'O型', height: '164cm', hobby: 'スポーツ（クライミング、自転車）、筋トレ', skill: '逆立ち、回転、フードアスリートマイスター、ラッピング、ハンドメイド', likes: 'ケールとナッツのサラダ、ドライフルーツ、グラノラバー、牛乳' }}},
  hanabi: { key:'hanabi', name_ja:'駒形花火', id:'@hanabistarmine',color:'#ff2021', avatar: getMemberAvatar('hanabi'), banner: getMemberBanner('hanabi'), profile: { description: 'L高 浅草サテライトの1年生。\n浅草にある呉服屋の一人娘。\n将来は跡を継ぎ、事業を拡大させ、着物文化を世界に広めたいという野望を持っている。\n頭の中はいつも着物のことでいっぱい。\n仲見世のアイドルで、しっかり者の商売人気質。', details: { grade: '1年生', birthday: '6月11日', bloodType: 'A型', height: '160cm', hobby: '着物、読書', skill: '着付け、習字、レンジ料理', likes: '抹茶のお菓子、パスタ、もち' }}},
  miracle: { key:'miracle', name_ja:'金澤奇跡', id:'@MiracleGoldSP', color:'#ffb7f1', avatar: getMemberAvatar('miracle'), banner: getMemberBanner('miracle'), profile: { description: 'L高 福井サテライトの2年生。\nお菓子作りが趣味で、将来の夢はパティシエとして独立開業し世界中にお店を出すこと。\n製菓学校で習うセオリー通りのやり方に疑問を持ち、個人で修行する時間を確保するためL高に入学した。\n言いたいことをはっきりと言うタイプ。', details: { grade: '2年生', birthday: '3月2日', bloodType: 'AB型', height: '152cm', hobby: 'お菓子作り', skill: 'お菓子作り、料理、徹夜', likes: '寿司（特にウニ、いくら）、あんきも、からすみ' }}},
  noriko: { key:'noriko', name_ja:'調布のりこ', id:'@Noricco_U', color:'#ae62ff', avatar: getMemberAvatar('noriko'), banner: getMemberBanner('noriko'), profile: { description: 'L高 福井サテライトの1年生。\n自分のことをなんの取り柄もない「量産型」だと思っている。\n将来の夢は声優で、中学3年の時に思い切って応募したオーディションでなんとか事務所に所属できたが、まだ仕事はない。', details: { grade: '1年生', birthday: '4月4日', bloodType: 'B型', height: '153cm', hobby: 'アニメ、漫画、ラノベ', skill: '歌（絶対音感）、掃除、バレーボールのセッターが得意。', likes: '甘いもの全般、菓子パンも好き。プリンとシュークリーム、カスタード系。' }}},
  yukuri: { key:'yukuri', name_ja:'春宮ゆかり', id:'@Yukuri_talk', color:'#5ecbd1', avatar: getMemberAvatar('yukuri'), banner: getMemberBanner('yukuri'), profile: { description: 'L高 梅田サテライトの1年生。\n穏やかで、品のあるお嬢様。\n幼い頃からバレエを習っており、ミュージカルが大好き。\nかつては自分も歌劇団に入りたいと思っていた。\nポルカのことを助けたいと思っている。', details: { grade: '1年生', birthday: '9月22日', bloodType: 'B型', height: '165cm', hobby: '観劇', skill: 'バレエ', likes: 'そうめん、ゼリー、グラタン、ハム、ハンバーグ、バウムクーヘン、漬物' }}},
  aurora: { key:'aurora', name_ja:'此花輝夜', id:'@Rollie_twinkle',color:'#fd589e', avatar: getMemberAvatar('aurora'), banner: getMemberBanner('aurora'), profile: { description: 'L高 梅田サテライトの2年生。\nメイクと美容が大好きで、美容情報をSNSで発信している。\n親の仕事の都合でLAからの帰国子女。「愛は正義」がモットーで、みんなに愛を与えられる優しい心の持ち主。', details: { grade: '2年生', birthday: '1月3日', bloodType: 'O型', height: '162cm', hobby: 'ファッション、美容', skill: 'メイク、コーヒー、縁結び、サッカー', likes: 'コーヒー、ベイクドビーンズ、目玉焼き、カリカリの薄いトースト' }}},
  midori: { key:'midori', name_ja:'山田真緑', id:'@LittlegreenCom',color:'#16b500', avatar: getMemberAvatar('midori'), banner: getMemberBanner('midori'), profile: { description: 'L高 梅田サテライトの1年生。\n環境問題に強い危機感を持っている。\n地球を守るため、環境保護活動をしながら通えるＬ高に入学した。\nHPやSNSを使って環境保護を呼びかけている。\nとても真面目で一生懸命だが、少しずれているところがある。', details: { grade: '1年生', birthday: '5月7日', bloodType: 'A型', height: '155cm', hobby: 'キャンプ', skill: 'パズル、植物標本、虫取り、釣り、星座観察、けん玉', likes: 'スモア、ワッフル、クリームシチュー、いちご' }}},
  shion: { key:'shion', name_ja:'佐々木翔音', id:'@ShaunTheBunny', color:'#9b9b9b', avatar: getMemberAvatar('shion'), banner: getMemberBanner('shion'), profile: { description: 'L高 仙台サテライトの1年生。\n制服コーデが大好きで、自宅で動画配信をしている。\n些細なことで学校に行けない日も多く、部屋に引きこもりがち。\n配信では饒舌だが、人とうまくコミュニケーションが取れない部分も。\nかつて存在したスクールアイドルμ\'sの園田海未のファン。', details: { grade: '1年生', birthday: '11月11日', bloodType: '？', height: '？', hobby: 'SNS配信、読書、パズル、プラモデル', skill: 'バイオリン、ピアノ', likes: '完全食、フライドポテト、ラーメン、辛い物' }}}
};

// 從原始HTML中提取的完整範例推文
const fallbackTweets = [
  { id: 1, author_id: 'yukuri', content: 'あ\nそろそろ着いたかな？\n#いきづらい部', created_at: '2025-08-13 10:39:00' },
  { id: 2, author_id: 'yukuri', content: '幕が上がった瞬間に🪄\n絢爛な舞台との出会いに胸をときめかせる客席と\n期待に胸が高鳴る観客の視線に背筋を伸ばす舞台の上🎩✨\n出会うっていう意味ではどちらも同じなのかもしれないね🎁\n#いきづらい部', created_at: '2025-08-13 10:36:00' },
  { id: 3, author_id: 'yukuri', content: 'これって少しだけ\nステージの幕が上がる前の心境に似てる気がする🥰\nステージの分厚い緞帳の向こう側にいてもこっち側にいても\nきっと同じようにドキドキしてる💘✨\n#いきづらい部', created_at: '2025-08-13 10:33:00' },
  { id: 4, author_id: 'yukuri', content: '人を待つ時間が意外と好きだなっていうことに今日気が付いた🎩✨\n待っている間はドキドキとワクワクと\nほんの少しのソワソワと💝✨\nでもやっぱり待っているその先に必ずいいことがあるって分かっているから…\nやっぱり楽しい🎩🪄\n#いきづらい部', created_at: '2025-08-13 10:30:00' },
  { id: 5, author_id: 'akira', content: '・ヒップヒンジ１０回×３セット\n・スプリットスクワット１５回×３セット\n・スクワット１５回×３セット\n・ワイドスクワット１５回×３セット\n・ルーマニアンデッドリフト１０回×３セット\n\nやっぱりテンション上がると下半身に行きがち🚵\nダンベルフライとロウ でストレッチも追加だな🌊\n#いきづらい部', created_at: '2025-08-12 15:46:00' },
  { id: 6, author_id: 'akira', content: 'そうか！\n考えてみたら\nしばらく筋トレもあんまりできなくなるかも？！\n\n今のうちにやり貯めしておこうかな\nっていうわけにはなかなかいかないのが\n筋トレなんだけど🏔\n#いきづらい部', created_at: '2025-08-12 15:41:00' },
  { id: 7, author_id: 'akira', content: 'まぁイベントが本番だしね！\nみんなにリアルで会えるのが楽しみ🏔\n\nただ新幹線で２時間半座ってるのが\n長いなって思うから\n狭い座席でもできるストレッチを\n考えておこうと思う🌊\n#いきづらい部', created_at: '2025-08-12 15:38:00' },
  { id: 8, author_id: 'akira', content: '私もこんな人になりたいって思った🚵\nみんなに会ったら\n沼津のいろんな話を\nしようと思う\n#いきづらい部', created_at: '2025-08-04 20:35:00' },
  { id: 9, author_id: 'akira', content: '水族館の帰りに通りがかった小さな海水浴場で\n見つけた海の家のかき氷🍧\n\n食べながら弟が海に飛ばしてしまった帽子を\n拾ってくれたジェットスキーのお姉さんが\n「お祭り楽しかった？」\nって聞いてくれた笑顔がかっこよくて\n#いきづらい部', created_at: '2025-08-04 20:32:00' },
  { id: 10, author_id: 'akira', content: 'でもたぶんそれがどっちでも\n2人とも前に進む🚵\n#いきづらい部', created_at: '2025-08-04 20:29:00' },
  { id: 11, author_id: 'akira', content: '「次はいつ来る？」\nってじっと私の目を覗き込む\n小さな弟の手を握りしめながら\n\n残していく方と残される方の\nどっちがつらいか考える\n#いきづらい部', created_at: '2025-08-04 20:26:00' },
  { id: 12, author_id: 'akira', content: '歩いてみれば\n沼津のあちこちに現れた\nスクールアイドルの足跡\n\n花火大会で流れてたあの歌も\n#いきづらい部', created_at: '2025-08-04 20:23:00' },
  { id: 13, author_id: 'akira', content: '本気でクライミングの選手になりたいなら\nやっぱり東京じゃないとって思って\nずっとそっちにばかり目が行っていたから\n\nなんの変哲もない地方都市だと思っていた沼津に\nあんな歴史があったなんて知らなかったな\n#いきづらい部', created_at: '2025-08-04 20:20:00' },
  { id: 14, author_id: 'akira', content: '帰省終了で東京帰着！\n海風を身体に感じて\n富士山を眺めて\n沼津に帰って来たなって感じる日々だった🗻\n#いきづらい部', created_at: '2025-08-04 20:17:00' },
  { id: 15, author_id: 'yukuri', content: 'せっかくみんなが来てくれるから、スケジュールが許す限り関西っぽいいろんなことをしたいなと思うけれど…\nやっぱり私は🎩✨\nあちこち遊びに行くよりも、みんなでスクールアイドルの活動をめいっぱい頑張りたいかな💘\n#いきづらい部', created_at: '2025-08-04 18:33:00' },
  { id: 16, author_id: 'yukuri', content: 'そうして…新大阪まで帰ってくると\nもう駅ナカでソースとお出汁の香りに出会って、またホッとしたりして🎩✨\n\n旅に出ると自分でも思ってる以上に\nHomeのありがたみを感じることを再発見🥰\n#いきづらい部', created_at: '2025-08-04 18:30:00' },
  { id: 17, author_id: 'yukuri', content: '地下街には全国各地のグルメがいっぱいあって\nそれも毎回楽しみなんだけど🎁✨\n\nその一角にじつは神戸でもお気に入りのチョコレート屋さんがあって、つい寄っちゃったり🩰✨\n遠い街で地元のお店に会ってちょっと嬉しい気持ちになるのかな🥰\n#いきづらい部', created_at: '2025-08-04 18:27:00' },
  { id: 18, author_id: 'yukuri', content: '私は東京駅に着くと、新幹線の改札を出たとたんに広がる駅の施設の大きさと、人の多さに毎回圧倒されちゃう👑\n分かってはいても、やっぱり大きい！\n東京駅🚉\n#いきづらい部', created_at: '2025-08-04 18:24:00' },
  { id: 19, author_id: 'yukuri', content: '私が新幹線に乗る時はたいてい東京に行くときだったから\n東京からのチケット相談はなんだか新鮮🎩🪄\nポルカちゃん無事に発券できたかな？\n#いきづらい部', created_at: '2025-08-04 18:21:00' },
  { id: 20, author_id: 'yukuri', content: 'これは2026年のテスト投稿です。\n#いきづらい部', created_at: '2026-08-04 18:21:00' },
  { id: 21, author_id: 'polka', content: 'これは2026年1月のテスト投稿です。\n#いきづらい部', created_at: '2026-01-15 10:00:00' },
  { id: 22, author_id: 'mai', content: 'これは2026年2月のテスト投稿です。\n#いきづらい部', created_at: '2026-02-15 11:00:00' },
  { id: 23, author_id: 'akira', content: 'これは2026年3月のテスト投稿です。\n#いきづらい部', created_at: '2026-03-15 12:00:00' },
  { id: 24, author_id: 'hanabi', content: 'これは2026年4月のテスト投稿です。\n#いきづらい部', created_at: '2026-04-15 13:00:00' },
  { id: 25, author_id: 'miracle', content: 'これは2026年5月のテスト投稿です。\n#いきづらい部', created_at: '2026-05-15 14:00:00' },
  { id: 26, author_id: 'noriko', content: 'これは2026年6月のテスト投稿です。\n#いきづらい部', created_at: '2026-06-15 15:00:00' },
  { id: 27, author_id: 'yukuri', content: 'これは2026年7月のテスト投稿です。\n#いきづらい部', created_at: '2026-07-15 16:00:00' },
  { id: 28, author_id: 'aurora', content: 'これは2026年8月のテスト投稿です。\n#いきづらい部', created_at: '2026-08-15 17:00:00' },
  { id: 29, author_id: 'midori', content: 'これは2026年9月のテスト投稿です。\n#いきづらい部', created_at: '2026-09-15 18:00:00' },
  { id: 30, author_id: 'shion', content: 'これは2026年10月のテスト投稿です。\n#いきづらい部', created_at: '2026-10-15 19:00:00' },
  { id: 31, author_id: 'polka', content: 'これは2026年11月のテスト投稿です。\n#いきづらい部', created_at: '2026-11-15 20:00:00' },
  { id: 32, author_id: 'mai', content: 'これは2026年12月のテスト投稿です。\n#いきづらい部', created_at: '2026-12-15 21:00:00' }
];

// 成員資料
const authors = reactive({...fallbackAuthors});
const characterOrder = ['polka','mai','akira','hanabi','miracle','noriko','yukuri','aurora','midori','shion'];

// 狀態管理
const prefs = reactive({ dark: false });
const allTweets = reactive([]);
const filters = reactive({ member: null, onlyLiked: false, search: '', year: null, month: null });
const ui = reactive({ 
  loaded: false, 
  overlay: false, 
  detail: false, 
  detailTweet: null, 
  showTop: false, 
  showSearchInput: false, 
  showMobileSearch: false, 
  isSharing: null, 
  dateNavModal: false, 
  profileModalAuthor: null 
});
const scroller = reactive({ activeDate: null });
const toast = reactive({ show: false, message: '', type: 'success' });

const searchInput = ref(null);
const mobileSearchInput = ref(null);
let intersectionObserver = null;
let toastTimeout = null;

// 翻譯函數
const t = (key) => translations['ja']?.[key] || key;

// 計算屬性
const tweetsBeforeMonthFilter = computed(() => {
  let result = [...allTweets];
  if (filters.year) result = result.filter(t => new Date(t.created_at).getFullYear() === filters.year);
  if (filters.onlyLiked) result = result.filter(t => t.liked);
  if (filters.member) result = result.filter(t => t.author_id === filters.member);
  if (filters.search) { 
    const query = filters.search.toLowerCase(); 
    result = result.filter(t => 
      t.content.toLowerCase().includes(query) || 
      (t.name_ja || authors[t.author_id]?.name_ja || '').toLowerCase().includes(query) || 
      (t.twitter_id || authors[t.author_id]?.id || '').toLowerCase().includes(query)
    ); 
  }
  return result;
});

const availableYears = computed(() => [...new Set(allTweets.map(t => new Date(t.created_at).getFullYear()))].sort((a, b) => b - a));

const availableMonths = computed(() => {
  if (!filters.year) return [];
  // 根據當前篩選條件（年份、成員、搜尋、喜歡）來計算可用的月份
  let filteredTweets = [...allTweets];
  if (filters.year) filteredTweets = filteredTweets.filter(t => new Date(t.created_at).getFullYear() === filters.year);
  if (filters.onlyLiked) filteredTweets = filteredTweets.filter(t => t.liked);
  if (filters.member) filteredTweets = filteredTweets.filter(t => t.author_id === filters.member);
  if (filters.search) { 
    const query = filters.search.toLowerCase(); 
    filteredTweets = filteredTweets.filter(t => 
      t.content.toLowerCase().includes(query) || 
      (t.name_ja || authors[t.author_id]?.name_ja || '').toLowerCase().includes(query) || 
      (t.twitter_id || authors[t.author_id]?.id || '').toLowerCase().includes(query)
    ); 
  }
  return [...new Set(filteredTweets.map(t => new Date(t.created_at).getMonth() + 1))];
});

const filteredTweets = computed(() => {
  if (!filters.month) return tweetsBeforeMonthFilter.value;
  return tweetsBeforeMonthFilter.value.filter(t => new Date(t.created_at).getMonth() + 1 === filters.month);
});

const dateGroups = computed(() => {
  if (filteredTweets.value.length === 0) return [];
  const groups = filteredTweets.value.reduce((acc, tweet) => { 
    const date = tweet.created_at.substring(0, 10); 
    if (!acc[date]) { 
      acc[date] = { date, count: 0, firstTweetId: tweet.id }; 
    } 
    acc[date].count++; 
    return acc; 
  }, {});
  return Object.values(groups).sort((a, b) => new Date(b.date) - new Date(a.date));
});

const brandColor = computed(() => (filters.member && authors[filters.member]) ? authors[filters.member].color : (projectInfo?.color || '#1d9bf0'));
const headerTitle = computed(() => { 
  if (filters.member) return authors[filters.member]?.name_ja || filters.member; 
  if (filters.onlyLiked) return t('filter_liked'); 
  return projectInfo?.name_ja || 'いきづらい部'; 
});

const currentBannerStyle = computed(() => {
  const current = filters.member ? authors[filters.member] : projectInfo;
  return current?.banner ? { backgroundImage: `url(${current.banner})` } : { backgroundColor: current?.color || '#1d9bf0' };
});

// 方法
const displayName = (author) => author?.name_ja || author?.id || '';
const tweetAuthorName = (author) => `${displayName(author)}@いきづらい部！`;
const avatarOf = (author) => author?.avatar_url || author?.avatar || '';
const linkify = (text) => (text || '').replace(/#([\w\u3000-\u9fff\u3040-\u30ff\uff00-\uffef!-]+)/g, '<a href="#" class="hashtag">#$1</a>');
const formatTime = (s) => new Intl.DateTimeFormat('ja-JP', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date(s));
const formatDateForScroller = (dateString) => new Intl.DateTimeFormat('ja-JP', { month: 'long', day: 'numeric' }).format(new Date(dateString));

const persistLikes = () => { 
  localStorage.setItem('bb_likes', JSON.stringify(allTweets.filter(t => t.liked).map(t => t.id))); 
};

const toggleLike = async (tweet) => { 
  tweet.liked = !tweet.liked; 
  if (tweet.liked) tweet._pop = true; 
  
  // 同步到後端（可選）
  try {
    const userIp = '127.0.0.1'; // 簡化處理，實際應該獲取真實IP
    await fetch('http://localhost:8787/api/likes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tweetId: tweet.id,
        userIp,
        action: tweet.liked ? 'like' : 'unlike'
      })
    });
  } catch (error) {
    console.warn('後端同步失敗，僅使用本地儲存:', error);
  }
  
  persistLikes(); 
};

const setMemberFilter = (key) => { filters.member = (filters.member === key) ? null : key; scrollToTop(); };
const setMonthFilter = (month) => { filters.month = (filters.month === month) ? null : month; };
const toggleLikedFilter = () => { filters.onlyLiked = !filters.onlyLiked; };
const resetFilters = () => { 
  filters.member = null; 
  filters.onlyLiked = false; 
  filters.search = ''; 
  if (availableYears.value.length > 0) filters.year = availableYears.value[0]; 
  filters.month = null; 
  scrollToTop(); 
};

const toggleOverlay = (show) => { ui.overlay = !!show; };
const openDetail = (tweet) => { 
  // 更新當前活動日期
  scroller.activeDate = tweet.created_at.substring(0, 10);
  console.log('點擊推文，更新活動日期:', scroller.activeDate);
  
  ui.detailTweet = tweet; 
  ui.detail = true; 
  toggleOverlay(true); 
};
const openProfileModal = (author) => { ui.profileModalAuthor = author; toggleOverlay(true); };
const openDateNavModal = () => { ui.dateNavModal = true; toggleOverlay(true); };
const closeAllModals = () => { ui.detail = ui.dateNavModal = false; ui.profileModalAuthor = null; toggleOverlay(false); };

const handleTweetTextClick = (e) => { 
  const a = e.target.closest('a.hashtag'); 
  if (!a) return; 
  e.preventDefault(); 
  filters.search = a.textContent; 
  scrollToTop(); 
};

const focusSearch = () => { 
  if (window.innerWidth <= 768) { 
    ui.showMobileSearch = true; 
    nextTick(() => mobileSearchInput.value?.focus()); 
  } else { 
    ui.showSearchInput = true; 
    nextTick(() => searchInput.value?.focus()); 
  } 
};

const onSearchBlur = () => { 
  if (filters.search === '') { 
    ui.showSearchInput = false; 
    ui.showMobileSearch = false; 
  } 
};

const shareTweet = async (tweet) => {
  if (ui.isSharing) return;
  ui.isSharing = tweet.id;
  
  try {
    const author = authors[tweet.author_id];
    const success = await shareTweetAsImage(tweet, author, prefs.dark);
    
    if (success) {
      showToast(t('image_gen_success'), 'success');
    } else {
      showToast(t('image_gen_fail'), 'error');
    }
  } catch (error) {
    console.error('分享功能失敗:', error);
    showToast(t('image_gen_fail'), 'error');
  } finally {
    ui.isSharing = null;
  }
};

const setupIntersectionObserver = () => {
  if (intersectionObserver) intersectionObserver.disconnect();
  const options = { rootMargin: "-40% 0px -60% 0px" };
  intersectionObserver = new IntersectionObserver(entries => { 
    const i = entries.find(e => e.isIntersecting); 
    if (i) { 
      const tw = allTweets.find(t => t.id == i.target.dataset.tweetId); 
      if (tw) {
        scroller.activeDate = tw.created_at.substring(0, 10);
        console.log('當前活動日期:', scroller.activeDate);
      }
    } 
  }, options);
  document.querySelectorAll('.tweet[data-tweet-id]').forEach(el => intersectionObserver.observe(el));
};

const scrollToDate = (tweetId) => { 
  const el = document.querySelector(`.tweet[data-tweet-id="${tweetId}"]`); 
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    // 更新當前活動日期
    const tweet = allTweets.find(t => t.id == tweetId);
    if (tweet) {
      scroller.activeDate = tweet.created_at.substring(0, 10);
    }
  }
};

const handleScroll = () => { ui.showTop = window.scrollY > 400; };

const showToast = (message, type = 'success') => { 
  if (toastTimeout) clearTimeout(toastTimeout); 
  toast.message = message; 
  toast.type = type; 
  toast.show = true; 
  toastTimeout = setTimeout(() => { toast.show = false; }, 3000); 
};

const applyTheme = () => { 
  document.documentElement.dataset.theme = prefs.dark ? 'dark' : 'light'; 
  localStorage.setItem('bb_theme', prefs.dark ? 'dark' : 'light'); 
};

const toggleTheme = () => { prefs.dark = !prefs.dark; };

// 初始化資料
const initData = async () => {
  prefs.dark = (localStorage.getItem('bb_theme') === 'dark');
  
  console.log('開始初始化資料...');
  
  // 嘗試從後端獲取資料
  try {
    // 獲取成員資料
    console.log('正在獲取成員資料...');
    const membersResponse = await fetch('http://localhost:8787/api/members');
    if (!membersResponse.ok) {
      throw new Error(`成員資料請求失敗: ${membersResponse.status} ${membersResponse.statusText}`);
    }
    const membersData = await membersResponse.json();
    console.log('成員資料:', membersData);
    
    // 清空現有資料並載入後端資料
    Object.keys(authors).forEach(key => delete authors[key]);
    membersData.forEach(member => {
      authors[member.id] = {
        ...member,
        avatar: getMemberAvatar(member.id), // 使用本地資源
        banner: getMemberBanner(member.id)  // 使用本地資源
      };
    });
    
    // 獲取推文資料
    console.log('正在獲取推文資料...');
    const tweetsResponse = await fetch('http://localhost:8787/api/tweets');
    if (!tweetsResponse.ok) {
      throw new Error(`推文資料請求失敗: ${tweetsResponse.status} ${tweetsResponse.statusText}`);
    }
    const tweetsData = await tweetsResponse.json();
    console.log('推文資料:', tweetsData);
    
    const processedTweets = tweetsData.map(tw => ({ 
      id: tw.id, 
      author_id: tw.author_id, 
      name_ja: tw.name_ja,
      twitter_id: tw.twitter_id,
      color: tw.color,
      avatar_url: getMemberAvatar(tw.author_id), // 使用本地資源
      created_at: tw.created_at, 
      content: tw.content, 
      image_url: tw.image_url || null, 
      liked: false, 
      _pop: false 
    })).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    // 清空現有推文並載入後端資料
    allTweets.length = 0;
    allTweets.push(...processedTweets);
    
    console.log('後端資料載入成功！');
    console.log('成員數量:', Object.keys(authors).length);
    console.log('推文數量:', allTweets.length);
    
  } catch (backendError) {
    console.warn('後端連接失敗，使用備用資料:', backendError);
    showToast('後端連接失敗，使用範例資料', 'warning');
    
    // 確保備用成員資料已載入
    if (Object.keys(authors).length === 0) {
      Object.assign(authors, fallbackAuthors);
      console.log('載入備用成員資料');
    }
    
    // 使用備用推文資料
    allTweets.length = 0;
    const processedFallbackTweets = fallbackTweets.map(tw => ({
      id: tw.id,
      author_id: tw.author_id,
      name_ja: authors[tw.author_id]?.name_ja || tw.author_id,
      twitter_id: authors[tw.author_id]?.id || `@${tw.author_id}`,
      color: authors[tw.author_id]?.color || '#1d9bf0',
      avatar_url: getMemberAvatar(tw.author_id), // 使用本地資源
      created_at: tw.created_at,
      content: tw.content,
      image_url: null,
      liked: false,
      _pop: false
    }));
    
    allTweets.push(...processedFallbackTweets);
    console.log('備用資料載入完成！');
    console.log('推文數量:', allTweets.length);
  }
  
  // 讀取本地喜歡狀態
  try { 
    const savedLikes = JSON.parse(localStorage.getItem('bb_likes') || '[]'); 
    const likeMap = new Set(savedLikes); 
    allTweets.forEach(tw => tw.liked = likeMap.has(tw.id)); 
  } catch (e) { 
    console.error("讀取 LocalStorage 中的 like 失敗", e); 
  }
  
  if (availableYears.value.length > 0) { filters.year = availableYears.value[0]; }
  
  console.log('資料初始化完成！');
};

// 生命週期
onMounted(async () => { 
  applyTheme(); 
  
  try {
    await initData(); 
    console.log('資料初始化成功');
  } catch (error) {
    console.error('資料初始化失敗，但繼續載入界面:', error);
    // 即使資料載入失敗，也要顯示界面
  }

  ui.loaded = true;
  
    nextTick(() => {
    if (allTweets.length > 0) {
      setupIntersectionObserver();
    }
  });
  
  window.addEventListener('scroll', handleScroll, { passive: true }); 
});

onBeforeUnmount(() => { 
  window.removeEventListener('scroll', handleScroll); 
  if (intersectionObserver) intersectionObserver.disconnect(); 
});

// 監聽器
watch(brandColor, (newColor) => {
  document.documentElement.style.setProperty('--brand-color', newColor);
}, { immediate: true });

watch(filteredTweets, () => nextTick(setupIntersectionObserver));
watch(() => [filters.year, filters.member], () => { 
  if (!availableMonths.value.includes(filters.month)) { 
    filters.month = null; 
  } 
});
watch(() => filters.member, (memberKey) => { 
  document.documentElement.dataset.memberTheme = !!(memberKey && authors[memberKey]); 
});
watch(() => prefs.dark, applyTheme);
</script>

<style scoped>
/* 這裡會包含所有CSS樣式，但為了簡潔，我只列出關鍵的樣式 */
/* 完整的樣式會在下一個檔案中提供 */

.app-container {
  display: flex;
  width: 100%;
  max-width: var(--main-max-width);
}

.sidebar-left, .sidebar-right {
  backdrop-filter: blur(12px);
}

.sidebar-left {
  width: 300px;
  padding: var(--spacing-unit);
  position: sticky;
  top: 0;
  height: 100vh;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  }

  .timeline {
  width: 100%;
  max-width: var(--timeline-width);
  min-width: 0;
  border-left: 1px solid var(--border-primary);
  border-right: 1px solid var(--border-primary);
  background-color: color-mix(in srgb, var(--bg-secondary) 85%, transparent);
  min-height: 100vh;
  backdrop-filter: blur(12px);
}

.sidebar-right {
  width: var(--sidebar-width);
  padding: calc(var(--spacing-unit) * 2);
  position: sticky;
  top: 0;
  height: 100vh;
}

/* 其他樣式會在CSS檔案中定義 */
</style>
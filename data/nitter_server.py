#!/usr/bin/env python3
"""
Nitter 推文爬蟲
從本地 Nitter 實例抓取 Twitter 數據
"""

import json
import sqlite3
import time
import random
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NitterScraper:
    def __init__(self, config_path='users.json', db_path='mydb.db'):
        self.config_path = config_path
        self.db_path = db_path
        self.config = self.load_config()
        self.instances = self.config['settings'].get('nitter_instances', ['localhost:8080'])
        self.current_instance_index = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.init_database()
        
    def load_config(self):
        """載入用戶配置"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def init_database(self, force_clear=False):
        """檢查並初始化資料庫結構 (force_clear=True 時清空推文)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if force_clear:
            logger.info("🗑️ 正在清空現有推文以進行全面重新抓取...")
            cursor.execute("DROP TABLE IF EXISTS tweets")
            conn.commit()
            table_exists = False
        else:
            # 檢查現有推文數
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tweets'")
            table_exists = cursor.fetchone() is not None
        
        if table_exists:
            cursor.execute('SELECT COUNT(*) FROM tweets')
            existing_count = cursor.fetchone()[0]
            logger.info(f"📊 資料庫已存在，目前有 {existing_count} 條推文")
            
            # 檢查是否需要添加引用相關欄位
            cursor.execute("PRAGMA table_info(tweets)")
            columns = [row[1] for row in cursor.fetchall()]
            # Ensure all quote columns exist
            quote_cols = {
                'quote_id': 'TEXT',
                'quote_text': 'TEXT',
                'quote_author_id': 'TEXT',
                'quote_author_name': 'TEXT',
                'quote_avatar': 'TEXT',
                'quote_image_url': 'TEXT'
            }
            for col, col_type in quote_cols.items():
                if col not in columns:
                    logger.info(f"🆕 添加引用欄位: {col}")
                    cursor.execute(f"ALTER TABLE tweets ADD COLUMN {col} {col_type}")
        else:
            logger.info("🆕 建立新資料庫")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tweets (
                tweet_id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                author_id TEXT NOT NULL,
                type TEXT,
                created_at TEXT,
                hashtags TEXT,
                urls TEXT,
                media_type TEXT,
                media_urls TEXT,
                quote_id TEXT,
                quote_text TEXT,
                quote_author_id TEXT,
                quote_author_name TEXT,
                quote_avatar TEXT,
                quote_image_url TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    
    def scrape_user(self, username, user_id, max_tweets=1000, incremental=True):
        """爬取單個用戶的推文
        incremental: 若為 True，當發現大量重複推文時自動停止 (預設)
        """
        cursor = None
        all_tweets = []
        page_count = 0
        
        failed_instances = set()
        
        deep_retries = 0
        max_deep_retries = 5  # Allow 5 deep retries (5 * 60s wait)

        # 用於判斷是否該停止爬取的計數器 (連續發現已存在推文的數量)
        consecutive_existing_count = 0
        stop_threshold = 20  # 連續 20 條已存在則停止 (約一頁)
        
        while len(all_tweets) < max_tweets:
            # Check if we exhausted all instances
            if len(failed_instances) >= len(self.instances):
                if deep_retries < max_deep_retries:
                    logger.warning(f"⚠️ 所有實例 ({len(self.instances)} 個) 皆失敗或被限制。Deep Retry {deep_retries+1}/{max_deep_retries}：暫停 60 秒後重試...")
                    time.sleep(60)
                    failed_instances = set()
                    deep_retries += 1
                    # Force instance rotation logic to pick a fresh one effectively
                    self.current_instance_index = (self.current_instance_index + 1) % len(self.instances)
                else:
                    logger.error("❌ 所有實例皆失敗且已達 Deep Retry 上限，停止爬取該用戶")
                    break

            instance = self.get_working_instance(exclude=failed_instances)
            protocol = 'http' if 'localhost' in instance or instance.split(':')[0].replace('.','').isdigit() else 'https'
            nitter_url = f"{protocol}://{instance}"
            
            url = f"{nitter_url}/{username}"
            if cursor:
                if '?' in url:
                    url += f"&cursor={cursor}"
                else:
                    url += f"?cursor={cursor}"
            
            logger.info(f"爬取 {username} 第 {page_count} 頁 (實例: {instance}) [已收錄: {len(all_tweets)}/{max_tweets}]: {url}")
            
            try:
                # 模擬真人延遲 (3-7秒)
                time.sleep(random.uniform(3, 7))
                
                response = requests.get(url, headers=self.headers, timeout=20)
                if response.status_code == 429:
                    logger.warning(f"⚠️ 實例 {instance} 速率限制 (429)，更換實例...")
                    failed_instances.add(instance)
                    continue
                
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Success! Reset deep retry counter
                deep_retries = 0
                
                # 找到推文
                timeline_items = soup.find_all('div', class_='timeline-item')
                # logger.info(f"找到 {len(timeline_items)} 個 timeline-item")
                
                if not timeline_items:
                    # 有時候實例返回空頁面但不報錯，切換試試
                    logger.warning(f"⚠️ 實例 {instance} 返回空頁面 (無 timeline-items)，標記為失敗並嘗試更換...")
                    failed_instances.add(instance)
                    continue
                
                # 成功後重置失敗名單 (因該實例證明可用)
                failed_instances = set()
                page_count += 1

                page_tweets = []
                # 檢查這一頁的推文有多少是數據庫裡已經有的
                existing_in_this_page = 0
                
                for item in timeline_items:
                    # 跳過公告等非推文內容
                    if 'timeline-item' not in item.get('class', []):
                        continue
                    # 跳過轉推 (可視需求調整)
                    if item.find('div', class_='retweet-header'):
                        continue
                        
                    tweet = self.parse_tweet(item, user_id, nitter_url)
                    if tweet:
                        # 檢查資料庫是否已存在
                        if incremental:
                            conn = sqlite3.connect(self.db_path)
                            cur = conn.cursor()
                            cur.execute('SELECT 1 FROM tweets WHERE tweet_id = ?', (tweet['tweet_id'],))
                            is_exist = cur.fetchone() is not None
                            conn.close()
                            
                            if is_exist:
                                consecutive_existing_count += 1
                                existing_in_this_page += 1
                            else:
                                consecutive_existing_count = 0  # 重置計數，因為發現了新推文
                        
                        page_tweets.append(tweet)
                
                if page_tweets:
                    all_tweets.extend(page_tweets)
                    logger.info(f"✅ 本頁解析出 {len(page_tweets)} 條推文 (其中 {existing_in_this_page} 條已存在)")
                
                # 判斷是否停止 (Incremental Mode)
                if incremental and consecutive_existing_count >= stop_threshold:
                    logger.info(f"🛑 已連續發現 {consecutive_existing_count} 條重複推文，判定已抓取至上次進度，停止抓取本用戶。")
                    break

                # 尋找下一頁的 cursor
                show_more_divs = soup.find_all('div', class_='show-more')
                show_more_div = None
                
                # 倒序尋找含有 "Load more" 的 div (模仿舊腳本邏輯)
                for div in reversed(show_more_divs):
                    link = div.find('a')
                    if link and 'Load more' in link.get_text():
                        show_more_div = div
                        break
                
                if not show_more_div:
                     # 嘗試尋找 more-replies 作為備案
                    show_more_div = soup.find('div', class_='more-replies') or soup.find('div', id='more')

                if show_more_div:
                    link = show_more_div.find('a')
                    if link:
                        href = link['href']
                        # 處理 href 為 "?cursor=..." 或 "username?cursor=..." 的情況
                        if 'cursor=' in href:
                            new_cursor = href.split('cursor=')[-1].split('&')[0]
                            if new_cursor == cursor:
                                logger.warning("⚠️ 檢測到重複 cursor，停止爬取以防止死循環")
                                break
                            cursor = new_cursor
                            # logger.info(f"➡️ 取得新 cursor: {cursor[:15]}...")
                        else:
                            logger.info(f"下一頁連結不含 cursor ({href})，視為結束")
                            break
                    else:
                        logger.warning("分頁按鈕容器內找不到 <a> 標籤，視為結束")
                        break
                else:
                    logger.info("沒有找到任何 'Load more' 按鈕，視為已達最底")
                    break
                
            except (requests.RequestException, Exception) as e:
                logger.error(f"實例 {instance} 出錯: {e}")
                failed_instances.add(instance)
                logger.info("🔄 更換實例重試...")
                time.sleep(2)
                continue
        return all_tweets

    def parse_tweet(self, item, author_id, nitter_url):
        """解析單條推文"""
        try:
            # Tweet ID
            tweet_link = item.find('a', class_='tweet-link')
            if not tweet_link:
                return None
            tweet_id = tweet_link['href'].split('/')[-1].replace('#m', '')
            
            # 推文內容
            content_div = item.find('div', class_='tweet-content')
            text = content_div.get_text(strip=True) if content_div else ''
            
            # Hashtags
            hashtags = []
            for tag in item.find_all('a', href=lambda x: x and '/search?q=%23' in x):
                hashtags.append(tag.get_text(strip=True))
            
            # URLs
            urls = []
            for link in content_div.find_all('a', href=True) if content_div else []:
                href = link['href']
                if not href.startswith('/') and 'http' in href:
                    urls.append(href)
            
            # Media
            media_urls = []
            media_type = None
            
            # 圖片
            for img in item.find_all('a', class_='still-image'):
                if 'href' in img.attrs:
                    media_url = img['href']
                    if media_url.startswith('/pic/'):
                        media_url = nitter_url + media_url
                    media_urls.append(media_url)
                    media_type = 'photo'
            
            # 影片
            video = item.find('video')
            if video and video.find('source'):
                video_url = video.find('source')['src']
                if video_url.startswith('/'):
                    video_url = nitter_url + video_url
                media_urls.append(video_url)
                media_type = 'video'
            
            # 時間
            tweet_date = item.find('span', class_='tweet-date')
            created_at = tweet_date.find('a')['title'] if tweet_date and tweet_date.find('a') else ''

            # 引用推文解析 (使用正確的 Nitter 結構)
            quote_data = {
                'quote_id': None,
                'quote_text': None,
                'quote_author_id': None,
                'quote_author_name': None,
                'quote_avatar': None,
                'quote_image_url': None
            }
            
            # 尋找 .quote 容器
            quote = item.find('div', class_='quote')
            if quote:
                # 1. 從 quote-link 或 href 取得推文 ID
                quote_link = quote.find('a', class_='quote-link')
                if quote_link and 'href' in quote_link.attrs:
                    href = quote_link['href']
                    # href 格式: /username/status/1234567890
                    parts = href.split('/')
                    if 'status' in parts:
                        status_idx = parts.index('status')
                        if status_idx + 1 < len(parts):
                            quote_data['quote_id'] = parts[status_idx + 1].split('#')[0]
                
                # 2. 取得引用推文文字
                quote_text_div = quote.find('div', class_='quote-text')
                if quote_text_div:
                    quote_data['quote_text'] = quote_text_div.get_text(strip=True)
                
                # 3. 取得作者資訊
                author_container = quote.find('div', class_='fullname-and-username') or quote
                
                username_link = author_container.find('a', class_='username')
                if username_link:
                    quote_data['quote_author_id'] = username_link.get_text(strip=True).lstrip('@')
                
                fullname_link = author_container.find('a', class_='fullname')
                if fullname_link:
                    quote_data['quote_author_name'] = fullname_link.get_text(strip=True)
                
                # 4. 取得引用者頭像
                quote_avatar_img = quote.find('img', class_='avatar')
                if quote_avatar_img and 'src' in quote_avatar_img.attrs:
                    avatar_src = quote_avatar_img['src']
                    if avatar_src.startswith('/pic/'):
                        avatar_src = nitter_url + avatar_src
                    quote_data['quote_avatar'] = avatar_src
                
                # 5. 取得引用推文中的圖片
                quote_media = quote.find('div', class_='quote-media-container') or quote.find('div', class_='attachments')
                if quote_media:
                    q_img = quote_media.find('a', class_='still-image')
                    if q_img and 'href' in q_img.attrs:
                        q_img_url = q_img['href']
                        if q_img_url.startswith('/pic/'):
                            q_img_url = nitter_url + q_img_url
                        quote_data['quote_image_url'] = q_img_url
            
            return {
                'tweet_id': tweet_id,
                'text': text,
                'author_id': str(author_id),
                'type': 'Quote' if quote_data['quote_id'] else 'Tweet',
                'created_at': created_at,
                'hashtags': ','.join(hashtags),
                'urls': ','.join(urls),
                'media_type': media_type or '',
                'media_urls': ','.join(media_urls),
                **quote_data
            }
            
        except Exception as e:
            logger.warning(f"解析推文失敗: {e}")
            return None
    
    def save_tweets(self, tweets, username):
        """保存推文到資料庫"""
        if not tweets:
            return 0, 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        new_count = 0
        update_count = 0
        
        for tweet in tweets:
            # 檢查是否已存在
            cursor.execute('SELECT tweet_id FROM tweets WHERE tweet_id = ?', 
                         (tweet['tweet_id'],))
            exists = cursor.fetchone()
            
            cursor.execute('''
                INSERT OR REPLACE INTO tweets 
                (tweet_id, text, author_id, type, created_at, hashtags, urls, media_type, media_urls,
                 quote_id, quote_text, quote_author_id, quote_author_name, quote_avatar, quote_image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tweet['tweet_id'],
                tweet['text'],
                tweet['author_id'],
                tweet['type'],
                tweet['created_at'],
                tweet['hashtags'],
                tweet['urls'],
                tweet['media_type'],
                tweet['media_urls'],
                tweet.get('quote_id'),
                tweet.get('quote_text'),
                tweet.get('quote_author_id'),
                tweet.get('quote_author_name'),
                tweet.get('quote_avatar'),
                tweet.get('quote_image_url')
            ))
            
            if exists:
                update_count += 1
            else:
                new_count += 1
        
        conn.commit()
        conn.close()
        
        return new_count, update_count
    
    def get_working_instance(self, exclude=None):
        """獲取下一個可用的實例"""
        if exclude is None:
            exclude = set()
            
        # 嘗試目前實例
        current = self.instances[self.current_instance_index]
        if current not in exclude:
            return current
            
        # 輪詢尋找下一個
        for _ in range(len(self.instances)):
            self.current_instance_index = (self.current_instance_index + 1) % len(self.instances)
            candidate = self.instances[self.current_instance_index]
            if candidate not in exclude:
                return candidate
        
        # 如果全部都排除過，清空重來
        return self.instances[0]

    def scrape_all(self, force_reclean=False, limit=1000, incremental=True):
        """批量抓取所有用戶"""
        if force_reclean:
            # 強制重爬 => 不進行 incremental 判斷
            incremental = False
            self.init_database(force_clear=True)
            
        logger.info("🚀 開始批量抓取")
        logger.info(f"模式: {'全部重爬 (Full/Rescrape)' if not incremental else '增量更新 (Incremental)'}")
        logger.info(f"已加載實例: {len(self.instances)} 個")
        logger.info(f"用戶數: {len(self.config['users'])}")
        logger.info(f"單用戶上限 (Max): {limit}")
        
        total_tweets = 0
        
        for user in self.config['users']:
            username = user['username']
            user_id = user['id']
            
            tweets = self.scrape_user(username, user_id, max_tweets=limit, incremental=incremental)
            new_c, up_c = self.save_tweets(tweets, username)
            total_tweets += (new_c + up_c)
            logger.info(f"✨ {username} 完成：新增 {new_c} 條，更新 {up_c} 條")
            
            # 每個用戶之間暫停 10-20 秒 (模擬真人)
            if user != self.config['users'][-1]:
                delay = random.uniform(10, 20)
                logger.info(f"\n⏸ 暫停 {delay:.1f} 秒...\n")
                time.sleep(delay)
        
        logger.info(f"\n{'='*50}")
        logger.info(f"🎉 全部完成！共抓取 {total_tweets} 條推文")
        logger.info(f"{'='*50}")


def main():
    import sys
    
    # 預設行為
    force = False
    limit = 1000
    incremental = True  # 預設為增量更新
    
    for arg in sys.argv:
        if arg == '--force' or arg == '--rescrape' or arg == '--full':
            force = True
            incremental = False  # 強制重爬時關閉增量判斷
        if arg.startswith('--limit='):
            try:
                limit = int(arg.split('=')[-1])
            except ValueError:
                logger.warning(f"無效的 --limit 參數: {arg}. 使用預設值 {limit}")
                
    scraper = NitterScraper(
        config_path='users.json',
        db_path='mydb.db'
    )
    
    # 若有 --full / --rescrape / --force 則 incremental=False
    # 否則 incremental=True
    
    scraper.scrape_all(force_reclean=force, limit=limit, incremental=incremental)


if __name__ == '__main__':
    main()

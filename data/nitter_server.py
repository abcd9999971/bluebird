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
        self.nitter_url = f"http://{self.config['settings']['nitter_instances'][0]}"
        self.init_database()
        
    def load_config(self):
        """載入用戶配置"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def init_database(self):
        """檢查並初始化資料庫結構（保留現有資料）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 檢查現有推文數
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tweets'")
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            cursor.execute('SELECT COUNT(*) FROM tweets')
            existing_count = cursor.fetchone()[0]
            logger.info(f"📊 資料庫已存在，目前有 {existing_count} 條推文")
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
                media_urls TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def scrape_user(self, username, user_id, skip_pages=0, max_pages=12):
        """抓取單個用戶的推文"""
        logger.info(f"\n{'='*50}")
        logger.info(f"開始抓取: @{username} (ID: {user_id})")
        logger.info(f"跳過前 {skip_pages} 頁，抓取第 {skip_pages+1}-{skip_pages+max_pages} 頁")
        logger.info(f"{'='*50}")
        
        tweets = []
        page = 1
        cursor = None
        total_pages = skip_pages + max_pages
        
        while page <= total_pages:
            url = f"{self.nitter_url}/{username}"
            if cursor:
                url += f"?cursor={cursor}"
            
            is_skip_page = page <= skip_pages
            status = "⏩ 跳過" if is_skip_page else "📄 抓取"
            logger.info(f"{status} 第 {page} 頁: {url[:80]}...")
            
            try:
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    logger.error(f"HTTP {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 解析推文（只有非跳過頁才保存）
                timeline_items = soup.find_all('div', class_='timeline-item')
                page_tweets = 0
                
                if not is_skip_page:
                    for item in timeline_items:
                        tweet_data = self.parse_tweet(item, user_id)
                        if tweet_data:
                            tweets.append(tweet_data)
                            page_tweets += 1
                
                if is_skip_page:
                    logger.info(f"  ⏭ 跳過 {len(timeline_items)} 條推文")
                else:
                    logger.info(f"  → 保存 {page_tweets} 條推文")
                
                # 查找下一頁 - 找最後一個 show-more (排除 "Load newest")
                show_more_divs = soup.find_all('div', class_='show-more')
                show_more = None
                for div in reversed(show_more_divs):
                    link = div.find('a')
                    if link and 'Load more' in link.get_text():
                        show_more = div
                        break
                
                if show_more and show_more.find('a'):
                    href = show_more.find('a')['href']
                    if 'cursor=' in href:
                        new_cursor = href.split('cursor=')[-1]
                        if new_cursor and new_cursor != cursor:  # 確保 cursor 有變化
                            cursor = new_cursor
                            page += 1
                            
                            # 隨機延遲 2-5 秒
                            delay = random.uniform(2, 5)
                            logger.debug(f"  等待 {delay:.1f} 秒...")
                            time.sleep(delay)
                        else:
                            logger.info("  cursor 未變化，停止")
                            break
                    else:
                        logger.info("  連結無 cursor，停止")
                        break
                else:
                    logger.info("  已到最後一頁")
                    break
                    
            except Exception as e:
                logger.error(f"抓取失敗: {e}")
                break
        
        # 保存到資料庫
        new_count, update_count = self.save_tweets(tweets, username)
        logger.info(f"✓ 完成: 新增 {new_count} 條，更新 {update_count} 條")
        
        return len(tweets)
    
    def parse_tweet(self, item, author_id):
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
                        media_url = self.nitter_url + media_url
                    media_urls.append(media_url)
                    media_type = 'photo'
            
            # 影片
            video = item.find('video')
            if video and video.find('source'):
                video_url = video.find('source')['src']
                if video_url.startswith('/'):
                    video_url = self.nitter_url + video_url
                media_urls.append(video_url)
                media_type = 'video'
            
            # 時間
            tweet_date = item.find('span', class_='tweet-date')
            created_at = tweet_date.find('a')['title'] if tweet_date and tweet_date.find('a') else ''
            
            return {
                'tweet_id': tweet_id,
                'text': text,
                'author_id': str(author_id),
                'type': 'Tweet',
                'created_at': created_at,
                'hashtags': ','.join(hashtags),
                'urls': ','.join(urls),
                'media_type': media_type or '',
                'media_urls': ','.join(media_urls)
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
                (tweet_id, text, author_id, type, created_at, hashtags, urls, media_type, media_urls)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tweet['tweet_id'],
                tweet['text'],
                tweet['author_id'],
                tweet['type'],
                tweet['created_at'],
                tweet['hashtags'],
                tweet['urls'],
                tweet['media_type'],
                tweet['media_urls']
            ))
            
            if exists:
                update_count += 1
            else:
                new_count += 1
        
        conn.commit()
        conn.close()
        
        return new_count, update_count
    
    def scrape_all(self):
        """批量抓取所有用戶"""
        logger.info("🚀 開始批量抓取")
        logger.info(f"Nitter: {self.nitter_url}")
        logger.info(f"用戶數: {len(self.config['users'])}")
        
        total_tweets = 0
        
        # 從第4個用戶開始（跳過前3個）
        start_index = 0
        logger.info(f"⏭ 跳過前 {start_index} 個用戶，從第 {start_index + 1} 個開始")
        
        for user in self.config['users'][start_index:]:
            username = user['username']
            user_id = user['id']
            
            count = self.scrape_user(username, user_id)
            total_tweets += count
            
            # 每個用戶之間暫停 5-10 秒
            if user != self.config['users'][-1]:
                delay = random.uniform(5, 10)
                logger.info(f"\n⏸ 暫停 {delay:.1f} 秒...\n")
                time.sleep(delay)
        
        logger.info(f"\n{'='*50}")
        logger.info(f"🎉 全部完成！共抓取 {total_tweets} 條推文")
        logger.info(f"{'='*50}")


def main():
    scraper = NitterScraper(
        config_path='users.json',
        db_path='mydb.db'
    )
    scraper.scrape_all()


if __name__ == '__main__':
    main()

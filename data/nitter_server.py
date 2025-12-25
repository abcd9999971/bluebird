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
    
    
    def scrape_user(self, username, user_id):
        """爬取單個用戶的推文"""
        cursor = None
        all_tweets = []
        page_count = 0
        
        while True:
            page_count += 1
            url = f"{self.nitter_url}/{username}"
            if cursor:
                url += f"?cursor={cursor}"
            
            logger.info(f"爬取 {username} 第 {page_count} 頁: {url}")
            
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 找到推文
                timeline_items = soup.find_all('div', class_='timeline-item')
                if not timeline_items:
                    logger.info(f"沒有找到推文，停止爬取 {username}")
                    break
                
                page_tweets = []
                for item in timeline_items:
                    # 跳過公告等非推文內容
                    if 'timeline-item' not in item.get('class', []):
                        continue
                    # 跳過轉推 (可視需求調整)
                    if item.find('div', class_='retweet-header'):
                        continue
                        
                    tweet = self.parse_tweet(item, user_id)
                    if tweet:
                        page_tweets.append(tweet)
                
                if page_tweets:
                    all_tweets.extend(page_tweets)
                    logger.info(f"本頁爬取 {len(page_tweets)} 條推文，目前累計 {len(all_tweets)} 條")
                
                # 尋找下一頁的 cursor
                show_more = soup.find('div', class_='show-more')
                if show_more and show_more.find('a'):
                    href = show_more.find('a')['href']
                    if 'cursor=' in href:
                        cursor = href.split('cursor=')[-1]
                    else:
                        logger.info("未找到下一頁 cursor，結束")
                        break
                else:
                    logger.info("沒有 'Show more' 按鈕，結束")
                    break
                
                time.sleep(2)  # 延遲避免請求過快
                
            except Exception as e:
                logger.error(f"爬取過程出錯: {e}")
                break
        
        return all_tweets

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
                        avatar_src = self.nitter_url + avatar_src
                    quote_data['quote_avatar'] = avatar_src
                
                # 5. 取得引用推文中的圖片
                quote_media = quote.find('div', class_='quote-media-container') or quote.find('div', class_='attachments')
                if quote_media:
                    q_img = quote_media.find('a', class_='still-image')
                    if q_img and 'href' in q_img.attrs:
                        q_img_url = q_img['href']
                        if q_img_url.startswith('/pic/'):
                            q_img_url = self.nitter_url + q_img_url
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
            
            tweets = self.scrape_user(username, user_id)
            new_c, up_c = self.save_tweets(tweets, username)
            total_tweets += (new_c + up_c)
            logger.info(f"✨ {username} 完成：新增 {new_c} 條，更新 {up_c} 條")
            
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

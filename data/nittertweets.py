#!/usr/bin/env python3
"""
Nitter 推文爬蟲 - 自動爬取推文並寫入資料庫
使用 Nitter 實例避免 Twitter API 限制
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
import re
import json
from urllib.parse import urljoin

class NitterScraper:
    def __init__(self, db_path='../dump.sql', nitter_instances=None):
        """
        初始化 Nitter 爬蟲
        
        Args:
            db_path: SQLite 資料庫路徑
            nitter_instances: Nitter 實例列表
        """
        self.db_path = db_path
        
        # 可用的 Nitter 實例列表 (按優先順序)
        if nitter_instances is None:
            self.nitter_instances = [
                'nitter.poast.org',
                'nitter.privacydev.net',
                'nitter.net',
                'nitter.it',
                'nitter.unixfox.eu',
            ]
        else:
            self.nitter_instances = nitter_instances
        
        self.current_instance = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _test_instance(self, instance):
        """測試 Nitter 實例是否可用"""
        try:
            url = f"https://{instance}"
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _get_working_instance(self):
        """獲取可用的 Nitter 實例"""
        if self.current_instance and self._test_instance(self.current_instance):
            return self.current_instance
        
        for instance in self.nitter_instances:
            print(f"測試 Nitter 實例: {instance}")
            if self._test_instance(instance):
                print(f"✓ 使用實例: {instance}")
                self.current_instance = instance
                return instance
        
        raise Exception("沒有可用的 Nitter 實例")
    
    def scrape_tweets(self, username, max_tweets=100, delay=2):
        """
        爬取指定用戶的推文
        
        Args:
            username: Twitter 用戶名 (不含 @)
            max_tweets: 最大爬取推文數
            delay: 請求延遲 (秒)
        
        Returns:
            推文列表
        """
        instance = self._get_working_instance()
        tweets = []
        cursor = None
        
        while len(tweets) < max_tweets:
            url = f"https://{instance}/{username}"
            if cursor:
                url += f"?cursor={cursor}"
            
            print(f"爬取: {url}")
            
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 找到推文項目
                timeline_items = soup.find_all('div', class_='timeline-item')
                
                if not timeline_items:
                    print("未找到推文")
                    break
                
                for item in timeline_items:
                    if len(tweets) >= max_tweets:
                        break
                    
                    # 跳過轉推或回覆 (可選)
                    if item.find('div', class_='retweet-header'):
                        continue
                    
                    tweet_data = self._parse_tweet(item, username)
                    if tweet_data:
                        tweets.append(tweet_data)
                        print(f"  已爬取 {len(tweets)} 條推文")
                
                # 查找下一頁
                show_more = soup.find('div', class_='show-more')
                if show_more and show_more.find('a'):
                    href = show_more.find('a').get('href', '')
                    if 'cursor=' in href:
                        cursor = href.split('cursor=')[-1]
                    else:
                        break
                else:
                    break
                
                time.sleep(delay)
                
            except Exception as e:
                print(f"錯誤: {e}")
                break
        
        print(f"\n總共爬取 {len(tweets)} 條推文")
        return tweets
    
    def _parse_tweet(self, item, username):
        """解析單條推文"""
        try:
            tweet_data = {}
            
            # 推文內容
            content_div = item.find('div', class_='tweet-content')
            if content_div:
                tweet_data['text'] = content_div.get_text(strip=True)
            else:
                return None
            
            # 推文連結 (獲取 tweet_id)
            tweet_link = item.find('a', class_='tweet-link')
            if tweet_link:
                href = tweet_link.get('href', '')
                # 從 /username/status/1234567890 提取 ID
                match = re.search(r'/status/(\d+)', href)
                if match:
                    tweet_data['tweet_id'] = match.group(1)
            
            # 時間
            tweet_date = item.find('span', class_='tweet-date')
            if tweet_date:
                date_link = tweet_date.find('a')
                if date_link:
                    date_str = date_link.get('title', '')
                    try:
                        # 解析日期格式: "Aug 13, 2025 · 10:39 AM UTC"
                        tweet_data['created_at'] = self._parse_date(date_str)
                    except:
                        tweet_data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Hashtags
            hashtags = []
            for hashtag in content_div.find_all('a', class_='hashtag'):
                hashtags.append(hashtag.get_text())
            tweet_data['hashtags'] = ','.join(hashtags)
            
            # URLs
            urls = []
            for link in content_div.find_all('a', class_='tweet-link'):
                url = link.get('href', '')
                if url and not url.startswith('#'):
                    urls.append(url)
            tweet_data['urls'] = ','.join(urls)
            
            # 媒體
            attachments = item.find('div', class_='attachments')
            media_urls = []
            media_type = ''
            
            if attachments:
                # 圖片
                images = attachments.find_all('a', class_='still-image')
                if images:
                    media_type = 'photo'
                    for img in images:
                        img_url = img.get('href', '')
                        if img_url:
                            media_urls.append(img_url)
                
                # 影片
                video = attachments.find('video')
                if video:
                    media_type = 'video'
                    video_source = video.find('source')
                    if video_source:
                        media_urls.append(video_source.get('src', ''))
            
            tweet_data['media_type'] = media_type
            tweet_data['media_urls'] = ','.join(media_urls)
            tweet_data['author_id'] = username
            tweet_data['type'] = 'Tweet'
            
            return tweet_data
            
        except Exception as e:
            print(f"解析推文時出錯: {e}")
            return None
    
    def _parse_date(self, date_str):
        """解析 Nitter 的日期格式"""
        # Nitter 日期格式: "Aug 13, 2025 · 10:39 AM UTC"
        try:
            # 移除 UTC 和多餘空格
            date_str = date_str.replace(' UTC', '').replace('·', '').strip()
            dt = datetime.strptime(date_str, '%b %d, %Y %I:%M %p')
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            # 備用解析方式
            try:
                dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def save_to_database(self, tweets, table_name='test_tweets'):
        """
        將推文保存到 SQLite 資料庫
        
        Args:
            tweets: 推文列表
            table_name: 資料表名稱
        """
        if not tweets:
            print("沒有推文需要保存")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 創建表 (如果不存在)
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
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
            
            # 插入數據
            inserted = 0
            skipped = 0
            
            for tweet in tweets:
                try:
                    cursor.execute(f'''
                        INSERT OR REPLACE INTO {table_name} 
                        (tweet_id, text, author_id, type, created_at, hashtags, urls, media_type, media_urls)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        tweet.get('tweet_id', ''),
                        tweet.get('text', ''),
                        tweet.get('author_id', ''),
                        tweet.get('type', 'Tweet'),
                        tweet.get('created_at', ''),
                        tweet.get('hashtags', ''),
                        tweet.get('urls', ''),
                        tweet.get('media_type', ''),
                        tweet.get('media_urls', '')
                    ))
                    inserted += 1
                except sqlite3.IntegrityError:
                    skipped += 1
                except Exception as e:
                    print(f"插入失敗: {e}")
                    skipped += 1
            
            conn.commit()
            conn.close()
            
            print(f"\n✓ 成功保存 {inserted} 條推文")
            if skipped > 0:
                print(f"  跳過 {skipped} 條重複推文")
            
        except Exception as e:
            print(f"保存到資料庫時出錯: {e}")
    
    def export_to_sql(self, tweets, output_file='tweets_export.sql', table_name='test_tweets'):
        """
        將推文匯出為 SQL 檔案
        
        Args:
            tweets: 推文列表
            output_file: 輸出檔案路徑
            table_name: 資料表名稱
        """
        if not tweets:
            print("沒有推文需要匯出")
            return
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # 寫入表結構
                f.write(f'''CREATE TABLE IF NOT EXISTS {table_name}(
tweet_id TEXT PRIMARY KEY,
text TEXT NOT NULL,
author_id TEXT NOT NULL,
type TEXT,
created_at TEXT,
hashtags TEXT,
urls TEXT,
media_type TEXT,
media_urls TEXT
);

''')
                
                # 寫入數據
                f.write(f"\nINSERT INTO {table_name} (tweet_id,text,author_id,type,created_at,hashtags,urls,media_type,media_urls) VALUES \n")
                
                for i, tweet in enumerate(tweets):
                    # 轉義單引號
                    text = tweet.get('text', '').replace("'", "''")
                    
                    comma = ',' if i < len(tweets) - 1 else ';'
                    
                    f.write(f'''("{tweet.get('tweet_id', '')}",'{text}','{tweet.get('author_id', '')}','{tweet.get('type', 'Tweet')}','{tweet.get('created_at', '')}','{tweet.get('hashtags', '')}','{tweet.get('urls', '')}','{tweet.get('media_type', '')}','{tweet.get('media_urls', '')}'){comma}
''')
            
            print(f"\n✓ 已匯出到 {output_file}")
            
        except Exception as e:
            print(f"匯出 SQL 時出錯: {e}")


def main():
    """主函數 - 範例使用"""
    
    # 設定要爬取的帳號
    accounts = [
        'Yukuri_talk',      # 春宮ゆかり
        'G_Akky304250',     # 五桐玲
        'My_Mai_Eld',       # 麻布麻衣
        'ShaunTheBunny',    # 佐々木翔音
    ]
    
    # 初始化爬蟲
    scraper = NitterScraper(db_path='../dump.sql')
    
    for account in accounts:
        print(f"\n{'='*60}")
        print(f"開始爬取 @{account} 的推文")
        print(f"{'='*60}\n")
        
        # 爬取推文
        tweets = scraper.scrape_tweets(
            username=account,
            max_tweets=50,  # 每個帳號爬取 50 條
            delay=2         # 每次請求間隔 2 秒
        )
        
        if tweets:
            # 保存到資料庫
            scraper.save_to_database(tweets, table_name='test_tweets')
            
            # 也可以匯出為 SQL 檔案
            output_file = f'{account}_tweets_{datetime.now().strftime("%Y_%m_%d")}.sql'
            scraper.export_to_sql(tweets, output_file=output_file)
        
        print(f"\n完成 @{account} 的爬取\n")
        
        # 帳號之間間隔稍長
        if account != accounts[-1]:
            time.sleep(5)
    
    print("\n" + "="*60)
    print("所有帳號爬取完成!")
    print("="*60)


if __name__ == '__main__':
    main()

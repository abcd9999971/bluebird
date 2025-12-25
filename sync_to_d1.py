#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
資料同步腳本
將 Nitter 爬取的推文資料同步到 Cloudflare D1 資料庫格式
並匯出為 JSON 格式供前端使用
"""

import sqlite3
import json
import os
from datetime import datetime

# 資料庫路徑
NITTER_DB = 'data/mydb.db'
D1_LOCAL_DB = 'backend/worker/.wrangler/state/v3/d1/miniflare-D1DatabaseObject/db.sqlite'
JSON_OUTPUT = 'frontend/page/src/data/tweets.json'

# 成員 ID 映射
AUTHOR_ID_MAP = {
    '1': 'polka',
    '2': 'mai',
    '3': 'akira',
    '4': 'hanabi',
    '5': 'miracle',
    '6': 'noriko',
    '7': 'yukuri',
    '8': 'aurora',
    '9': 'midori',
    '10': 'shion'
}

# 成員資料（從 member.json 提取）
MEMBERS_DATA = {
    'polka': {'name_ja': '高橋ポルカ', 'twitter_id': '@polka_lion', 'color': '#ccb12e', 'grade': '1年生', 'birthday': '8月18日', 'blood_type': '不明', 'height': '157cm'},
    'mai': {'name_ja': '麻布麻衣', 'twitter_id': '@My_Mai_Eld', 'color': '#009fdf', 'grade': '1年生', 'birthday': '2月13日', 'blood_type': 'B型', 'height': '154cm'},
    'akira': {'name_ja': '五桐玲', 'twitter_id': '@G_Akky304250', 'color': '#88d66e', 'grade': '1年生', 'birthday': '7月9日', 'blood_type': 'O型', 'height': '164cm'},
    'hanabi': {'name_ja': '駒形花火', 'twitter_id': '@hanabistarmine', 'color': '#ff2021', 'grade': '1年生', 'birthday': '6月11日', 'blood_type': 'A型', 'height': '160cm'},
    'miracle': {'name_ja': '金澤奇跡', 'twitter_id': '@MiracleGoldSP', 'color': '#ffb7f1', 'grade': '2年生', 'birthday': '3月2日', 'blood_type': 'AB型', 'height': '152cm'},
    'noriko': {'name_ja': '調布のりこ', 'twitter_id': '@Noricco_U', 'color': '#ae62ff', 'grade': '1年生', 'birthday': '4月4日', 'blood_type': 'B型', 'height': '153cm'},
    'yukuri': {'name_ja': '春宮ゆかり', 'twitter_id': '@Yukuri_talk', 'color': '#5ecbd1', 'grade': '1年生', 'birthday': '9月22日', 'blood_type': 'B型', 'height': '165cm'},
    'aurora': {'name_ja': '此花輝夜', 'twitter_id': '@Rollie_twinkle', 'color': '#fd589e', 'grade': '2年生', 'birthday': '1月3日', 'blood_type': 'O型', 'height': '162cm'},
    'midori': {'name_ja': '山田真緑', 'twitter_id': '@LittlegreenCom', 'color': '#16b500', 'grade': '1年生', 'birthday': '5月7日', 'blood_type': 'A型', 'height': '155cm'},
    'shion': {'name_ja': '佐々木翔音', 'twitter_id': '@ShaunTheBunny', 'color': '#9b9b9b', 'grade': '1年生', 'birthday': '11月11日', 'blood_type': '？', 'height': '？'}
}

def convert_media_url(nitter_url):
    """
    將 Nitter 本地 URL 轉換為 Twitter CDN URL
    例如: http://localhost:8080/pic/orig/media%2FG8wY1l-bwAAMPp1.jpg
    轉為: https://pbs.twimg.com/media/G8wY1l-bwAAMPp1.jpg
    """
    if not nitter_url or nitter_url == '':
        return None
    
    # 檢查是否為 Nitter URL
    if 'localhost' in nitter_url or 'nitter' in nitter_url:
        import re
        from urllib.parse import unquote
        
        # 提取檔案名 /pic/orig/media%2F{filename}
        match = re.search(r'/pic/orig/media%2F(.+?)(?:\?|$)', nitter_url)
        if not match:
            match = re.search(r'/pic/orig/media/(.+?)(?:\?|$)', nitter_url)
        
        if match:
            filename = unquote(match.group(1))
            return f'https://pbs.twimg.com/media/{filename}'
    
    return nitter_url



def parse_nitter_date(date_str):
    """解析 Nitter 日期格式"""
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        date_part = date_str.split(' · ')[0]
        time_part = date_str.split(' · ')[1].replace(' UTC', '') if ' · ' in date_str else '12:00 AM'
        datetime_str = f"{date_part} {time_part}"
        dt = datetime.strptime(datetime_str, '%b %d, %Y %I:%M %p')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"日期解析錯誤: {date_str} - {e}")
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def export_to_json():
    """匯出推文資料為 JSON 格式"""
    print('\n📝 匯出推文資料為 JSON...')
    
    # 確保輸出目錄存在
    os.makedirs(os.path.dirname(JSON_OUTPUT), exist_ok=True)
    
    # 連接 D1 資料庫
    d1_conn = sqlite3.connect(D1_LOCAL_DB)
    d1_conn.row_factory = sqlite3.Row
    d1_cursor = d1_conn.cursor()
    
    # 查詢所有推文，按時間倒序
    d1_cursor.execute('''
        SELECT id, tweet_id, author_id, content, type, created_at, 
               hashtags, urls, image_url, media_type
        FROM tweets
        ORDER BY created_at DESC
    ''')
    
    # 轉換為 JSON 格式
    tweets_list = []
    for row in d1_cursor.fetchall():
        tweet = {
            'id': row['id'],
            'tweet_id': str(row['tweet_id']),  # 確保是字串格式
            'author_id': row['author_id'],
            'content': row['content'],
            'type': row['type'],
            'created_at': row['created_at'],
            'hashtags': row['hashtags'],
            'urls': row['urls'],
            'image_url': row['image_url'],
            'media_type': row['media_type']
        }
        tweets_list.append(tweet)
    
    # 寫入 JSON 檔案
    with open(JSON_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(tweets_list, f, ensure_ascii=False, indent=2)
    
    print(f'✓ 已匯出 {len(tweets_list)} 筆推文至 {JSON_OUTPUT}')
    
    # 統計各成員的推文資料
    print('\n📊 成員推文統計:')
    print('=' * 80)
    
    for member_id in MEMBERS_DATA.keys():
        d1_cursor.execute('''
            SELECT 
                COUNT(*) as total,
                MIN(created_at) as earliest,
                MAX(created_at) as latest,
                SUM(CASE WHEN hashtags IS NOT NULL AND hashtags != '' THEN 1 ELSE 0 END) as with_hashtags,
                SUM(CASE WHEN image_url IS NOT NULL AND image_url != '' THEN 1 ELSE 0 END) as with_media
            FROM tweets
            WHERE author_id = ?
        ''', (member_id,))
        
        stats = d1_cursor.fetchone()
        
        if stats['total'] > 0:
            member_name = MEMBERS_DATA[member_id]['name_ja']
            twitter_id = MEMBERS_DATA[member_id]['twitter_id']
            
            print(f"\n{member_name} ({twitter_id}):")
            print(f"  推文總數: {stats['total']} 筆")
            print(f"  最早推文: {stats['earliest']}")
            print(f"  最新推文: {stats['latest']}")
            print(f"  含標籤數: {stats['with_hashtags']} 筆 ({stats['with_hashtags']/stats['total']*100:.1f}%)")
            print(f"  含媒體數: {stats['with_media']} 筆 ({stats['with_media']/stats['total']*100:.1f}%)")
    
    print('\n' + '=' * 80)
    
    # 全域統計
    d1_cursor.execute('''
        SELECT 
            COUNT(*) as total,
            COUNT(DISTINCT author_id) as unique_authors,
            SUM(CASE WHEN hashtags IS NOT NULL AND hashtags != '' THEN 1 ELSE 0 END) as total_with_hashtags,
            SUM(CASE WHEN image_url IS NOT NULL AND image_url != '' THEN 1 ELSE 0 END) as total_with_media,
            MIN(created_at) as earliest,
            MAX(created_at) as latest
        FROM tweets
    ''')
    
    global_stats = d1_cursor.fetchone()
    print('\n📈 全域統計:')
    print(f"  總推文數: {global_stats['total']} 筆")
    print(f"  成員人數: {global_stats['unique_authors']} 位")
    print(f"  含標籤數: {global_stats['total_with_hashtags']} 筆 ({global_stats['total_with_hashtags']/global_stats['total']*100:.1f}%)")
    print(f"  含媒體數: {global_stats['total_with_media']} 筆 ({global_stats['total_with_media']/global_stats['total']*100:.1f}%)")
    print(f"  時間範圍: {global_stats['earliest']} 至 {global_stats['latest']}")
    
    d1_conn.close()
    
    return len(tweets_list)


def sync_data():
    """同步資料"""
    print('='*60)
    print('資料同步工具 - Nitter DB → Cloudflare D1')
    print('='*60)
    
    # 檢查來源資料庫
    if not os.path.exists(NITTER_DB):
        print(f'✗ 錯誤: 找不到 Nitter 資料庫: {NITTER_DB}')
        return
    
    # 確保目標資料庫目錄存在
    os.makedirs(os.path.dirname(D1_LOCAL_DB), exist_ok=True)
    
    # 連接資料庫
    print(f'\n📊 連接資料庫...')
    nitter_conn = sqlite3.connect(NITTER_DB)
    nitter_conn.row_factory = sqlite3.Row
    d1_conn = sqlite3.connect(D1_LOCAL_DB)
    
    print('✓ 資料庫連接成功')
    
    # 初始化 D1 資料庫結構
    print('\n📝 初始化 D1 資料庫結構...')
    d1_cursor = d1_conn.cursor()
    
    # 建立 members 表
    d1_cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id TEXT PRIMARY KEY,
            name_ja TEXT NOT NULL,
            twitter_id TEXT NOT NULL,
            color TEXT NOT NULL,
            avatar_url TEXT,
            banner_url TEXT,
            grade TEXT,
            birthday TEXT,
            blood_type TEXT,
            height TEXT,
            hobby TEXT,
            skill TEXT,
            likes TEXT,
            description TEXT
        )
    ''')
    
    # 建立 tweets 表
    d1_cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_id TEXT UNIQUE,
            author_id TEXT NOT NULL,
            content TEXT NOT NULL,
            type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            hashtags TEXT,
            urls TEXT,
            image_url TEXT,
            media_type TEXT,
            FOREIGN KEY (author_id) REFERENCES members(id)
        )
    ''')
    
    # 建立 likes 表
    d1_cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_id INTEGER NOT NULL,
            user_ip TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tweet_id) REFERENCES tweets(id),
            UNIQUE(tweet_id, user_ip)
        )
    ''')
    
    d1_conn.commit()
    print('✓ 資料庫結構初始化完成')
    
    # 同步成員資料
    print('\n👥 同步成員資料...')
    d1_cursor.execute('DELETE FROM members')
    
    for member_id, member_data in MEMBERS_DATA.items():
        avatar_url = f'https://www.lovelive-anime.jp/lovehigh/img/member_{list(MEMBERS_DATA.keys()).index(member_id) + 1}.png'
        
        d1_cursor.execute('''
            INSERT INTO members (id, name_ja, twitter_id, color, avatar_url, banner_url, 
                               grade, birthday, blood_type, height, hobby, skill, likes, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            member_id,
            member_data['name_ja'],
            member_data['twitter_id'],
            member_data['color'],
            avatar_url,
            '',  # banner_url
            member_data['grade'],
            member_data['birthday'],
            member_data['blood_type'],
            member_data['height'],
            '', '', '', ''  # hobby, skill, likes, description
        ))
    
    d1_conn.commit()
    print(f'✓ 已同步 {len(MEMBERS_DATA)} 位成員')
    
    # 同步推文資料
    print('\n💬 同步推文資料...')
    nitter_cursor = nitter_conn.cursor()
    nitter_cursor.execute('SELECT * FROM tweets ORDER BY created_at DESC')
    
    # 完全清空推文表並重置 ID (解決 AUTOINCREMENT 累積問題)
    d1_cursor.execute('DROP TABLE IF EXISTS tweets')
    d1_cursor.execute('''
        CREATE TABLE tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_id TEXT UNIQUE,
            author_id TEXT NOT NULL,
            content TEXT NOT NULL,
            type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            hashtags TEXT,
            urls TEXT,
            image_url TEXT,
            media_type TEXT,
            FOREIGN KEY (author_id) REFERENCES members(id)
        )
    ''')
    d1_conn.commit()
    
    synced_count = 0
    skipped_count = 0
    
    for row in nitter_cursor.fetchall():
        # 轉換 author_id
        numeric_author_id = str(row['author_id'])
        author_id = AUTHOR_ID_MAP.get(numeric_author_id)
        
        if not author_id:
            skipped_count += 1
            continue
        
        # 解析日期
        created_at = parse_nitter_date(row['created_at'])
        
        # 處理圖片
        image_url = None
        if row['media_urls']:
            media_urls = row['media_urls'].split(',')
            if media_urls:
                # 轉換 Nitter URL 為 Twitter CDN URL
                image_url = convert_media_url(media_urls[0].strip())
        
        # 插入推文
        d1_cursor.execute('''
            INSERT INTO tweets (tweet_id, author_id, content, type, created_at, 
                               hashtags, urls, image_url, media_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['tweet_id'],
            author_id,
            row['text'],
            row['type'],
            created_at,
            row['hashtags'],
            row['urls'],
            image_url,
            row['media_type']
        ))
        
        synced_count += 1
    
    d1_conn.commit()
    print(f'✓ 已同步 {synced_count} 筆推文')
    if skipped_count > 0:
        print(f'⚠ 跳過 {skipped_count} 筆無效推文')
    
    # 關閉連接
    nitter_conn.close()
    d1_conn.close()
    
    # 匯出為 JSON
    json_count = export_to_json()
    
    print('\n' + '='*60)
    print('✅ 同步完成！')
    print('='*60)
    print(f'成員數: {len(MEMBERS_DATA)}')
    print(f'推文數: {synced_count}')
    print(f'JSON 匯出: {json_count} 筆')
    print(f'JSON 檔案: {JSON_OUTPUT}')
    print('\n提示:')
    print('  1. 執行 "cd backend/worker && npm run dev" 啟動本地開發伺服器')
    print('  2. 前端將使用 D1 API 或 JSON fallback 資料')

if __name__ == '__main__':
    sync_data()


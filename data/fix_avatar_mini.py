#!/usr/bin/env python3
"""
臨時腳本: 修正資料庫和 JSON 中的頭貼網址，移除 _mini 後綴
"""
import sqlite3
import json

def fix_avatars():
    # 1. 修正 SQLite 資料庫
    print("🔧 修正 mydb.db...")
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    
    # 獲取所有包含 _mini.jpg 的頭貼
    cursor.execute("SELECT tweet_id, quote_avatar FROM tweets WHERE quote_avatar LIKE '%_mini.jpg'")
    rows = cursor.fetchall()
    
    fixed_db_count = 0
    for tweet_id, old_url in rows:
        new_url = old_url.replace('_mini.jpg', '.jpg')
        cursor.execute("UPDATE tweets SET quote_avatar = ? WHERE tweet_id = ?", (new_url, tweet_id))
        fixed_db_count += 1
    
    conn.commit()
    conn.close()
    print(f"✅ 資料庫修正完成：{fixed_db_count} 筆")
    
    # 2. 修正 tweets.json
    print("\n🔧 修正 tweets.json...")
    json_path = '../frontend/page/src/data/tweets.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_json_count = 0
    for tweet in data:
        if tweet.get('quote_avatar') and '_mini.jpg' in tweet['quote_avatar']:
            tweet['quote_avatar'] = tweet['quote_avatar'].replace('_mini.jpg', '.jpg')
            fixed_json_count += 1
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON 修正完成：{fixed_json_count} 筆")
    print(f"\n🎉 總計修正 {fixed_db_count + fixed_json_count} 筆頭貼網址")

if __name__ == '__main__':
    fix_avatars()

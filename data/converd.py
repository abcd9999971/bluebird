import pandas as pd
import sqlite3

# 讀取 CSV
df = pd.read_csv('G_Akky304250_tweets_2025_08_19.csv')

# 假設 CSV 有很多欄位，但只想要 'id', 'name', 'age'
df = df[['tweet_id', 'text', 'created_at']]
df['author_id'] = '1'


# 建立 SQLite DB
conn = sqlite3.connect('mydb.db')

# 匯入選擇的欄位到 my_table
df.to_sql('my_table', conn, if_exists='replace', index=False)

conn.close()

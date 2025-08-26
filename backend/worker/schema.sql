CREATE TABLE posts (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    author_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reply_to TEXT,                -- 回覆的推文 ID (可為 NULL)
    quote_of TEXT                 -- 被引用的推文 ID (可為 NULL)
)
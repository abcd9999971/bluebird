/**
 * いきづらい部！ 部員日誌 API
 * Cloudflare Workers 後端服務
 */

export interface Env {
	DB : DB;
}

export default {
  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // 處理 CORS 預檢請求
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        }
      });
    }

    try {
      // 獲取所有成員資訊
      if (path === '/api/members') {
    const { results } = await env.DB.prepare(
          `SELECT id, name_ja, twitter_id, color, avatar_url, banner_url, 
                  grade, birthday, blood_type, height, hobby, skill, likes, description
           FROM members
           ORDER BY id`
        ).all();
        
        return new Response(JSON.stringify(results), {
          headers: { 
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*'
          }
        });
      }

      // 獲取推文列表
      if (path === '/api/tweets') {
        const searchParams = url.searchParams;
        const authorId = searchParams.get('author');
        const year = searchParams.get('year');
        const month = searchParams.get('month');
        const search = searchParams.get('search');
        const limit = parseInt(searchParams.get('limit') || '50');
        const offset = parseInt(searchParams.get('offset') || '0');

        let query = `
          SELECT t.id, t.author_id, t.content, t.created_at, t.image_url,
                 m.name_ja, m.twitter_id, m.color, m.avatar_url
          FROM tweets t
          JOIN members m ON t.author_id = m.id
          WHERE 1=1
        `;
        
        const params: any[] = [];
        
        if (authorId) {
          query += ` AND t.author_id = ?`;
          params.push(authorId);
        }
        
        if (year) {
          query += ` AND strftime('%Y', t.created_at) = ?`;
          params.push(year);
        }
        
        if (month) {
          query += ` AND strftime('%m', t.created_at) = ?`;
          params.push(month.padStart(2, '0'));
        }
        
        if (search) {
          query += ` AND (t.content LIKE ? OR m.name_ja LIKE ?)`;
          const searchTerm = `%${search}%`;
          params.push(searchTerm, searchTerm);
        }
        
        query += ` ORDER BY t.created_at DESC LIMIT ? OFFSET ?`;
        params.push(limit, offset);

        const { results } = await env.DB.prepare(query).bind(...params).all();

    return new Response(JSON.stringify(results), {
          headers: { 
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*'
          }
        });
      }

      // 獲取推文統計資訊
      if (path === '/api/stats') {
        const { results: yearStats } = await env.DB.prepare(`
          SELECT strftime('%Y', created_at) as year, COUNT(*) as count
          FROM tweets
          GROUP BY strftime('%Y', created_at)
          ORDER BY year DESC
        `).all();
        
        const { results: monthStats } = await env.DB.prepare(`
          SELECT strftime('%Y', created_at) as year, 
                 strftime('%m', created_at) as month, 
                 COUNT(*) as count
          FROM tweets
          GROUP BY strftime('%Y', created_at), strftime('%m', created_at)
          ORDER BY year DESC, month DESC
        `).all();
        
        return new Response(JSON.stringify({
          years: yearStats,
          months: monthStats
        }), {
          headers: { 
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*'
          }
        });
      }

      // 處理喜歡/取消喜歡
      if (path === '/api/likes' && request.method === 'POST') {
        const body = await request.json();
        const { tweetId, userIp, action } = body;
        
        if (action === 'like') {
          try {
            await env.DB.prepare(`
              INSERT INTO likes (tweet_id, user_ip) VALUES (?, ?)
            `).bind(tweetId, userIp).run();
          } catch (e) {
            // 如果已經喜歡過了，忽略錯誤
          }
        } else if (action === 'unlike') {
          await env.DB.prepare(`
            DELETE FROM likes WHERE tweet_id = ? AND user_ip = ?
          `).bind(tweetId, userIp).run();
        }
        
        return new Response(JSON.stringify({ success: true }), {
          headers: { 
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*'
          }
        });
      }

      // 獲取喜歡狀態
      if (path === '/api/likes/status') {
        const tweetIds = url.searchParams.get('tweetIds');
        const userIp = url.searchParams.get('userIp');
        
        if (!tweetIds || !userIp) {
          return new Response(JSON.stringify({ error: 'Missing parameters' }), {
            status: 400,
            headers: { 
              "Content-Type": "application/json",
              'Access-Control-Allow-Origin': '*'
            }
          });
        }
        
        const ids = tweetIds.split(',').map(id => parseInt(id));
        const placeholders = ids.map(() => '?').join(',');
        
        const { results } = await env.DB.prepare(`
          SELECT tweet_id FROM likes 
          WHERE tweet_id IN (${placeholders}) AND user_ip = ?
        `).bind(...ids, userIp).all();
        
        const likedIds = results.map((r: any) => r.tweet_id);
        
        return new Response(JSON.stringify({ likedIds }), {
          headers: { 
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*'
          }
        });
      }

      // 新增推文
      if (path === '/api/tweets' && request.method === 'POST') {
        const body = await request.json();
        const { authorId, content, imageUrl } = body;
        
        if (!authorId || !content) {
          return new Response(JSON.stringify({ error: 'Missing required fields' }), {
            status: 400,
            headers: { 
              "Content-Type": "application/json",
              'Access-Control-Allow-Origin': '*'
            }
          });
        }
        
        const { results } = await env.DB.prepare(`
          INSERT INTO tweets (author_id, content, image_url) 
          VALUES (?, ?, ?) 
          RETURNING id, author_id, content, created_at, image_url
        `).bind(authorId, content, imageUrl || null).run();
        
        return new Response(JSON.stringify(results[0]), {
          status: 201,
          headers: { 
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*'
          }
        });
      }

      // 預設路由 - 返回基本資訊
      return new Response(JSON.stringify({
        message: 'いきづらい部！ 部員日誌 API',
        version: '1.0.0',
        endpoints: [
          'GET /api/members - 獲取所有成員資訊',
          'GET /api/tweets - 獲取推文列表',
          'GET /api/stats - 獲取統計資訊',
          'POST /api/tweets - 新增推文',
          'POST /api/likes - 處理喜歡/取消喜歡',
          'GET /api/likes/status - 獲取喜歡狀態'
        ]
      }), {
        headers: { 
          "Content-Type": "application/json",
          'Access-Control-Allow-Origin': '*'
        }
      });

    } catch (error) {
      console.error('API Error:', error);
      return new Response(JSON.stringify({ 
        error: 'Internal server error',
        message: error instanceof Error ? error.message : 'Unknown error'
      }), {
        status: 500,
        headers: { 
          "Content-Type": "application/json",
          'Access-Control-Allow-Origin': '*'
        }
      });
    }
  }
}


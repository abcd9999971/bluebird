/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Bind resources to your worker in `wrangler.jsonc`. After adding bindings, a type definition for the
 * `Env` object can be regenerated with `npm run cf-typegen`.
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

import { deserializeJsonResponse } from "@prisma/client/runtime/library";

export interface Env {
	DB : DB;
}

export default {
  async fetch(request, env) {
    const { results } = await env.DB.prepare(
      `SELECT text, author_id, created_at 
       FROM test_tweets
       ORDER BY created_at DESC 
       LIMIT 20`
    ).all()

    return new Response(JSON.stringify(results), {
      headers: { "Content-Type": "application/json" }
    })
  }
}

